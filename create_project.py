#!/usr/bin/env python3
import os
import sys
import subprocess

# Define project structure
PROJECT_STRUCTURE = {
    "data": ["raw", "processed", "metadata"],
    "notebooks": [],
    "scripts": [],
    "src": [],
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
.env
"""

README_TEMPLATE = """# {project_name}

Short 1-2 sentence summary describing what this project does and why it matters.

---

## 🌍 Motivation

Why this problem is important, and what real-world context it fits into.

> Example: "Rising turbidity affects aquatic ecosystems and drinking water. This model estimates river turbidity from satellite data to support monitoring and management."

---

## 🧠 Methods

- Describe the ML/DS approach (e.g., CNN, GNN, LSTM)
- Mention the data sources and preprocessing strategy
- If applicable, explain geospatial or time-series aspects

---

## ⚙️ Tech Stack

- Python, PyTorch, TensorFlow  
- SQL (SQLite/PostgreSQL), FastAPI, Docker  
- Planet Imagery, Google Earth Engine  
- SLURM, Shell scripting, scikit-learn  

---

## 📈 Results

- Evaluation metrics (R², MAE, accuracy, etc.)
- Benchmarks or comparisons
- Visuals or plots if available

---

## 🚀 Deployment (if applicable)

- FastAPI endpoint (e.g., `/predict`)
- Deployed on [Heroku/Render/HuggingFace Spaces](#)
- Dockerized application  
- How to test the API:  
  ```bash
  curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{{"input": "example"}}'
  ```

## 🗃️ Data & Figures

- Input datasets or access instructions  
- Visual diagrams or conceptual figures  
  ![Conceptual Diagram](./figures/example_figure.png)  
- Example input/output pairs or result snapshots

---

## 🔍 How to Run

```bash
git clone https://github.com/ghmyers/your-repo-name.git
cd your-repo-name
conda create -n myenv python=3.10
conda activate myenv
pip install -r requirements.txt
python src/train.py

---

## 📚 References

- [Link to publication or preprint](#)
- [Relevant research papers, tools, or datasets](#)

---

## 📂 Project Structure

### **🔹 Directory Breakdown**
📌 **`data/`** → Stores all datasets for the project.
- **`raw/`** → Unprocessed data as received from the source.
- **`processed/`** → Data that has been cleaned and preprocessed.
- **`metadata/`** → Configuration files, data dictionaries, or metadata about datasets.

📌 **`notebooks/`** → Jupyter notebooks for analysis, data exploration, and experimentation.

📌 **`scripts/`** → Python scripts for automation, data preprocessing, and model training.

📌 **`src/`** → Source code for the project.

📌 **`outputs/`** → Stores generated reports, plots, visualizations, and final results.

📌 **`logs/`** → Logging files for tracking the execution of scripts.

📌 **`config/`** → Configuration files (e.g., `.yaml`, `.json`) for model and script settings.

📌 **`tests/`** → Unit tests to validate scripts and model performance.

---

## 🧠 Author

**George Harrison Myers**  
PhD Student | Machine Learning Engineer | Environmental Data Scientist
[LinkedIn](https://www.linkedin.com/in/harrison-myers-eit-b37156181/) • [Email](mailto:ghmyers96@gmail.com) • [GitHub](https://github.com/ghmyers)

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

