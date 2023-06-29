SOURCE_FILES=when

# 代码检查
check:
	pdm run black --check ${SOURCE_FILES}
	pdm run mypy --show-error-codes ${SOURCE_FILES}
	pdm run isort --check --diff ${SOURCE_FILES}

# 格式化代码
format:
	pdm run isort ${SOURCE_FILES}
	pdm run black ${SOURCE_FILES}

.PHONY: clean  ## Clear local caches and build artifacts
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -rf site
	rm -rf coverage.xml