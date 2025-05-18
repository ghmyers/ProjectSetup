#!/usr/bin/env python3
import os
import subprocess
import sys

# Define paths to Utility scripts
UTILS_DIR = os.path.expanduser("~/Utilities")  # Adjust if necessary

CREATE_PROJECT_SCRIPT = os.path.join(UTILS_DIR, "create_project.py")
GENERATE_DEPENDENCIES_SCRIPT = os.path.join(UTILS_DIR, "generate_dependencies.py")
GIT_SETUP_SCRIPT = os.path.join(UTILS_DIR, "setup_github.sh")
GIT_AUTO_SCRIPT = os.path.join(UTILS_DIR, "git_auto.sh")

# Define Logging Function Content
LOGGING_SETUP_CONTENT = """
import logging
import os

def setup_logging(log_dir="logs", log_filename="project.log"):

    # Dynamically determine the project root
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    except NameError:
        project_root = os.getcwd()  # Fallback if __file__ is not available

    # Ensure logs directory exists
    log_dir = os.path.join(project_root, log_dir)
    os.makedirs(log_dir, exist_ok=True)

    # Define log file path
    log_path = os.path.join(log_dir, log_filename)

    # Prevent duplicate handlers
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            filename=log_path,
            filemode="a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.INFO
        )

    return logging.getLogger("project")

# Example usage
if __name__ == "__main__":
    logger = setup_logging()
    logger.info("Logging setup is working!")

"""

# def run_script(script, args=None):
#     """Executes a script (Python or Bash) with optional arguments."""
#     try:
#         if script.endswith(".py"):
#             cmd = ["python3", script] + (args if args else [])
#         elif script.endswith(".sh"):
#             cmd = ["bash", script] + (args if args else [])
#         else:
#             print(f"⚠️ Unsupported script format: {script}")
#             return

#         subprocess.run(cmd, check=True)
#         print(f"✅ Successfully ran {script}")
def run_script(script, args=None, *, cwd=None):
    """Execute a Python or Bash script with optional args and working dir."""
    try:
        if script.endswith(".py"):
            cmd = ["python3", script]
        elif script.endswith(".sh"):
            cmd = ["bash", script]
        else:
            print(f"⚠️ Unsupported script format: {script}")
            return
        cmd += args or []

        subprocess.run(cmd, check=True, cwd=cwd)   # <-- key change
        
        print(f"✅ Successfully ran {script}")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script}: {e}")

def write_logging_script(project_path):
    """Writes logging_setup.py to src/utils/ inside the new project."""
    src_utils_path = os.path.join(project_path, "src")
    os.makedirs(src_utils_path, exist_ok=True)

    logging_file_path = os.path.join(src_utils_path, "logging_setup.py")

    with open(logging_file_path, "w") as f:
        f.write(LOGGING_SETUP_CONTENT)

    print(f"✅ Created logging_setup.py in {logging_file_path}")

def setup_project(project_name):
    """Runs the entire project setup process."""
    if not project_name:
        print("❌ Error: Please provide a project name.")
        sys.exit(1)

    # Compute absolute project path dynamically
    project_path = os.path.abspath(project_name)
    config_path = os.path.join(project_path, 'config')
    print(f"🚀 Setting up project at: {project_path}")

    # Step 1: Create project structure
    run_script(CREATE_PROJECT_SCRIPT, [project_name])

    # Step 2: Generate dependency files
    run_script(GENERATE_DEPENDENCIES_SCRIPT, [config_path])

    # Step 3: Initialize GitHub repository (Pass Absolute Project Path)
    # run_script(GIT_SETUP_SCRIPT, [project_name, project_path])
    run_script(
    GIT_SETUP_SCRIPT,
    ["Initial project scaffold", "main"],      # commit msg, branch
    cwd=project_path                           # <-- must be inside repo
    )

    # Step 4: Set up logging inside src/utils/
    write_logging_script(project_path)

    # Step 5: Automate Git commits
    print("✅ Initial commit setup complete. Run the following to start your first commit:")
    print(f"  cd \"{project_path}\" && bash {GIT_AUTO_SCRIPT} \"Initial project setup\"")

    print(f"🎉 Project {project_name} is fully set up!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python setup_project.py <project_name>")
    else:
        setup_project(sys.argv[1])

