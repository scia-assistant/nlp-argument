dev-setup:
	pip install -r requirements.txt
	npm install

lint:
	flake8 --ignore E203 src/

format:
	black -l 79 src/

check:
	python3 -m unittest discover -s ./tests  -p 'test_*.py'
