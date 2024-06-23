program = main.py

# main run target, depends on virtual environment existing
run: env/bin/activate
	./env/scripts/python $(program)

# automatically reinstall the dependencies whenever the requirements.txt file changes
env/bin/activate: requirements.txt
	python -m venv env	
	./env/scripts/pip install -r requirements.txt

# delete pycache and virtual env
clean:
	rm -rf __pycache__
	rm -rf env