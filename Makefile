dev-setup:
	pip install -r requirements.txt
	npm install

check:
	python3 -m unittest discover -s ./tests  -p 'test_*.py'


doc:
	mkdir -p build
	sphinx-apidoc -o documentation/docs ./src
	sphinx-build -b html documentation/ build/html
	

doc_clean:
	rm -rf build/html
	rm -rf docs 