.PHONY: install ask eval

install:
	pip install -r requirements.txt

ask:
	python -m portfolio_ask "$(Q)"

eval:
	python evals/run_evals.py
