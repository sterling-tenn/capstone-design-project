# Variables
VENV_NAME=venv
PYTHON=$(VENV_NAME)/bin/python
PIP=$(VENV_NAME)/bin/pip
UVICORN=$(VENV_NAME)/bin/uvicorn
APP=main:app

# Create virtual environment and install FastAPI and Uvicorn
setup:
	python3 -m venv $(VENV_NAME)
	$(PIP) install --upgrade pip
	$(PIP) install fastapi uvicorn

# Install additional dependencies (if required)
install:
	$(PIP) install -r requirements.txt

# Run the FastAPI server using Uvicorn from the virtual environment
run:
	$(UVICORN) $(APP) --reload

# Clean virtual environment
clean:
	rm -rf $(VENV_NAME)

# Format the code using black (optional, if you want to add code formatting)
format:
	$(PIP) install black
	$(VENV_NAME)/bin/black .

# Lint the code using flake8 (optional, if you want linting)
lint:
	$(PIP) install flake8
	$(VENV_NAME)/bin/flake8 .
