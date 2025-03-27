#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime

# Define the standard boilerplate with docstring
PYTHON_TEMPLATE = """\"\"\"
TITLE: [Script Name]
AUTHOR: [Your Name]
DATE: {date}
DESCRIPTION: [Brief description of what this script does]
\"\"\"

#!/usr/bin/env python3
import os
import sys

# Set project directory dynamically
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(PROJECT_DIR)

# Ensure PROJECT_DIR is in sys.path for module imports
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Append src/ to Python's module search path
sys.path.append(os.path.join(PROJECT_DIR, "src"))

# Define subdirectories
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
FIGURE_DIR = os.path.join(PROJECT_DIR, 'outputs', 'figures')

# Import logging
from logging_setup import setup_logging
logger = setup_logging(log_dir="logs", log_filename=)
logger.info(f"Script initialized: {{os.path.basename(__file__)}}")

# Your code here...
"""
# Define Jupyter Notebook structure with Markdown and Code cells
JUPYTER_TEMPLATE_MARKDOWN = """## TITLE: [Notebook Name]
### AUTHOR: [Your Name]
### DATE: {date}
##### DESCRIPTION: [Brief description of what this notebook does]
"""

JUPYTER_TEMPLATE_CODE = """import os
import logging


# Project directory structure
PROJECT_DIR = os.path.dirname(os.path.abspath(''))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
FIGURE_DIR = os.path.join(PROJECT_DIR, 'outputs', 'figures')
os.chdir(PROJECT_DIR)

# Append src/ to Python's module search path
sys.path.append(os.path.join(PROJECT_DIR, "src"))


# Setup logging
from logging_setup import setup_logging
logger = setup_logging(log_dir="logs", log_filename=)
logger.info("Notebook initialized")

# Your code here...
"""

def create_new_script(script_name, script_type="py"):
    """Creates a new Python script or Jupyter notebook with pre-filled boilerplate."""
    
    project_dir = os.getcwd()

    if script_type == "py":
        file_path = os.path.join(project_dir, f"{script_name}.py")
        template = PYTHON_TEMPLATE.format(date=datetime.today().strftime('%Y-%m-%d'))
    elif script_type == "ipynb":
        file_path = os.path.join(project_dir, f"{script_name}.ipynb")
        template = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": JUPYTER_TEMPLATE_MARKDOWN.format(date=datetime.today().strftime('%Y-%m-%d')).split("\n")
                },
                {
                    "cell_type": "code",
                    "metadata": {},
                    "source": JUPYTER_TEMPLATE_CODE.split("\n")
                }
            ],
            "metadata": {},
            "nbformat": 4,
            "nbformat_minor": 2
        }
    else:
        print("Invalid script type! Choose 'py' or 'ipynb'.")
        return

    if os.path.exists(file_path):
        print(f"File '{file_path}' already exists. Skipping...")
        return

    with open(file_path, "w") as f:
        if script_type == "py":
            f.write(template)
        else:
            f.write(json.dumps(template, indent=4))

    print(f"Created {script_type.upper()} file: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python initialize_script.py <script_name> <py|ipynb>")
    else:
        create_new_script(sys.argv[1], sys.argv[2])

