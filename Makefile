VENV		= venv
PYTHON		= $(VENV)/bin/python3
PIP			= $(VENV)/bin/pip
SRC			= src

# ─── Setup ────────────────────────────────────────────────────────────────────

all: $(VENV)

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# ─── Data Analysis ──────────────────────────────────────────────────────────────

train: dossier
	$(PYTHON) $(SRC)/main.py -sessions 1000 -save agents/agent_1000.json

visualize: dossier
	$(PYTHON) $(SRC)/main.py -load agents/agent_500000.json -visual -step_by_step


dossier:
	mkdir -p agents



# ─── Norme ────────────────────────────────────────────────────────────────────

flake8: 
	flake8 $(SRC)/*.py

# ─── Nettoyage ────────────────────────────────────────────────────────────────

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -delete

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all clean fclean re dossier