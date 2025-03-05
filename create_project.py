#!/usr/bin/env python3
import os
import sys
import subprocess

# Define project structure
PROJECT_STRUCTURE = {
    "data": ["raw", "processed", "metadata"],
    "notebooks": [],
    "scripts": [],
    "src": ["utils", "models"],
    "tests": [],
    "logs": [],
    "outputs": [],
    "config": [],
    "models": []
}

GITIGNORE_CONTENT = """
# Ignore virtual environments
venv/
__pycache__/
.ipynb_checkpoints/
.DS_Store/
cache
logs/
outputs/
data/
"""

README_TEMPLATE = """# {project_name}
## Overview
This project is structured for efficient data science and machine learning workflows. It includes well-organized directories for raw and processed data, notebooks, scripts, models, and outputs.

## 📂 Project Structure


### **🔹 Directory Breakdown**
📌 **`data/`** → Stores all datasets for the project.
- **`raw/`** → Unprocessed data as received from the source.
- **`processed/`** → Data that has been cleaned and preprocessed.
- **`metadata/`** → Configuration files, data dictionaries, or metadata about datasets.

📌 **`notebooks/`** → Jupyter notebooks for analysis, data exploration, and experimentation.

📌 **`scripts/`** → Python scripts for automation, data preprocessing, and model training.

📌 **`src/`** → Source code for the project.
- **`utils/`** → Helper functions such as logging, preprocessing utilities, and feature engineering.

📌 **`models/`** → Saved machine learning models and model checkpoints.

📌 **`outputs/`** → Stores generated reports, plots, visualizations, and final results.

📌 **`logs/`** → Logging files for tracking the execution of scripts.

📌 **`config/`** → Configuration files (e.g., `.yaml`, `.json`) for model and script settings.

📌 **`tests/`** → Unit tests to validate scripts and model performance.

---
"""

def create_directories(project_name):
    """Creates project directories based on the defined structure."""
    os.makedirs(project_name, exist_ok=True)

    for folder, subfolders in PROJECT_STRUCTURE.items():
        base_path = os.path.join(project_name, folder)
        os.makedirs(base_path, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(base_path, subfolder), exist_ok=True)

def create_readme(project_name):
    """Generates README.md with project structure."""
    structure_text = "\n".join([f"│── {key}/" + (("\n│   ├── " + "\n│   ├── ".join(subs)) if subs else "") for key, subs in PROJECT_STRUCTURE.items()])
    readme_content = README_TEMPLATE.format(project_name=project_name, structure=structure_text)
    
    with open(os.path.join(project_name, "README.md"), "w") as f:
        f.write(readme_content)

def create_gitignore(project_name):
    """Creates a .gitignore file to exclude unnecessary files."""
    with open(os.path.join(project_name, ".gitignore"), "w") as f:
        f.write(GITIGNORE_CONTENT)

def initialize_git_repo(project_name):
    """Initializes a Git repository in the project directory."""
    subprocess.run(["git", "init", project_name], check=True)

def create_project(project_name):
    """Orchestrates project creation."""
    if not project_name:
        print("❌ Error: Please provide a project name.")
        sys.exit(1)
    
    print(f"🚀 Creating project: {project_name}")
    create_directories(project_name)
    create_readme(project_name)
    create_gitignore(project_name)
    initialize_git_repo(project_name)
    
    print(f"✅ Project '{project_name}' initialized successfully!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_project.py <project_name>")
    else:
        create_project(sys.argv[1])

