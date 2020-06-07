
clean:
	@echo "--> Cleaning pyc files"
	find . -name "*.pyc" -delete

init: clean
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
