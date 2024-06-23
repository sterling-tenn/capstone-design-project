program = main.py

# linux/macOS
linux: env/bin/activate
	./env/bin/python3 $(program)
env/bin/activate: requirements.txt
	python3 -m venv env
	./env/bin/pip install -r requirements.txt

# windows
win: env/scripts/activate
	./env/scripts/python $(program)
env/scripts/activate: requirements.txt
	python -m venv env	
	./env/scripts/pip install -r requirements.txt

# delete pycache and virtual env
clean:
	rm -rf __pycache__
	rm -rf env