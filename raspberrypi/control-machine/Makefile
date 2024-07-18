program = main.py
astar = astar.py

# linux/macOS
linux: env/bin/activate
	./env/bin/python3 $(program)
	./env/bin/python3 -m black $(program)
	./env/bin/python3 -m black $(astar)

env/bin/activate: requirements.txt
	python3 -m venv env
	./env/bin/pip install -r requirements.txt
	./env/bin/python3 -m black $(program)
	./env/bin/python3 -m black $(astar)

# windows
win: env/scripts/activate
	./env/scripts/python $(program)
	./env/scripts/python -m black $(program)
	./env/scripts/python -m black $(astar)

env/scripts/activate: requirements.txt
	python -m venv env	
	./env/scripts/pip install -r requirements.txt
	./env/scripts/python -m black $(program)
	./env/scripts/python -m black $(astar)

# delete pycache and virtual env
clean:
	rm -rf __pycache__
	rm -rf env