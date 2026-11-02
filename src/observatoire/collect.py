"""Téléchargement des sources déclarées dans sources.yaml.

Chaque téléchargement est tracé dans data/raw/manifest.json (date, taille, empreinte
SHA-256) : on peut ainsi prouver quelle version des données a produit quel résultat.
"""

from __future__ import annotations

import hashlib
import json
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from observatoire.config import RAW, load_sources


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def download(source: dict, dest_dir: Path = RAW, force: bool = False) -> Path:
    """Télécharge une source si elle n'est pas déjà présente dans data/raw/."""
    url = (source.get("url") or "").strip()
    if not url:
        raise ValueError(
            f"La source « {source.get('id')} » n'a pas d'url dans sources.yaml. "
            "Renseignez le lien direct vers le fichier."
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source["fichier"]
    if dest.exists() and not force:
        print(f"[collect] {dest.name} déjà présent, téléchargement ignoré (force=True pour refaire).")
        return dest

    print(f"[collect] Téléchargement de {source['id']} depuis {url}")
    request = urllib.request.Request(url, headers={"User-Agent": "observatoire-prj450"})
    with urllib.request.urlopen(request, timeout=120) as response, open(dest, "wb") as out:
        out.write(response.read())

    _update_manifest(dest_dir, source, dest)
    return dest


def _update_manifest(dest_dir: Path, source: dict, dest: Path) -> None:
    manifest_path = dest_dir / "manifest.json"
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest[source["id"]] = {
        "fichier": dest.name,
        "url": source.get("url"),
        "telecharge_le": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "octets": dest.stat().st_size,
        "sha256": sha256(dest),
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


def collect_all(force: bool = False) -> dict[str, Path]:
    """Télécharge toutes les sources ; retourne {id: chemin local}."""
    return {s["id"]: download(s, force=force) for s in load_sources()}
