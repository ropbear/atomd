build:
	python3 -m pip install pip wheel setuptools
	python3 setup.py sdist bdist_wheel --plat-name=any
	python3 -m pip wheel -r requirements.txt --wheel-dir=./whl/
	mv dist/* ./whl/
	rm -rf *.egg-info build dist venv