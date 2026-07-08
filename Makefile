install:
	pip install -r requirements.txt

test:
	pytest

clean:
	rm -rf __pycache__