.PHONY: check site-build site-serve todo tree

check:
	python3 scripts/check_markdown.py

site-build: check
	uv run zensical build --clean --strict

site-serve:
	uv run zensical serve

todo:
	@rg --line-number 'TODO\(' --glob '*.md' . || true

tree:
	@find docs guides experiments decisions references assets templates scripts -maxdepth 2 -type f | sort
