export PYTHONPATH := src

.PHONY: install sample data test app

install:
	pip install -r requirements.txt

sample:
	python -m observatoire.pipeline --sample

data:
	python -m observatoire.pipeline

test:
	python -m pytest

app:
	streamlit run app/app.py
