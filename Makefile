dev-setup:
	pip install -r requirements.txt
	npm install

check:
	python3 -m unittest discover -s ./tests  -p 'test_*.py'
