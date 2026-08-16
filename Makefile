generate:
	uv run python main.py

build: generate
	cd output && pdflatex main.tex
