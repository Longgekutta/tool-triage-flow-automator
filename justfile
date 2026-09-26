# justfile for tool-triage-flow-automator

default: run

setup:
    python main.py setup

run:
    python main.py run

test:
    python main.py test

health:
    python main.py health

clean:
    python main.py clean
