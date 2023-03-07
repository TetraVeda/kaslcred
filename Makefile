build:
	rm -rfv dist/*
	python -m build

release: build
	python -m twine upload --repository kaslcred dist/*
