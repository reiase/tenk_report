.PHONY: check todo tree

check:
	python3 scripts/check_markdown.py

todo:
	@rg --line-number 'TODO\(' --glob '*.md' . || true

tree:
	@find docs guides experiments decisions references assets templates scripts -maxdepth 2 -type f | sort
