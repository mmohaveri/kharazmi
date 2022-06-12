help: ## Display this help screen
	@grep -h -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

type_check: *.py ## Type check the package using pyright type checker.
	@pyright src/kharazmi

build: *.py ## Builds the package's wheel file
	@python setup.py sdist bdist_wheel

cspell: ## Spell checks the entire codebase
	@cspell -e "*.pyo" -e "*.pyc"  -e "./build/**" -e "./dist/**" -e "./src/kharazmi.egg-info/**" "./**/**"

upload: build ## Uploads the package to pypi
	@twine upload dist/*

clean: ## to remove generated files
	rm -r build dist .mypy_cache

.PHONY: help clean type_check build upload  