#!/usr/bin/env python3
import os
import subprocess
import sys
import yaml

def detect_pip_dependencies(project_dir):
    """Extract installed pip dependencies and update config/requirements.txt."""
    config_dir = os.path.join(project_dir, "config")
    os.makedirs(config_dir, exist_ok=True)  # Ensure config directory exists

    requirements_path = os.path.join(config_dir, "requirements.txt")
    try:
        output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
        with open(requirements_path, "w") as f:
            f.write(output)
        print(f"✅ Updated pip dependencies in {requirements_path}")
    except Exception as e:
        print(f"❌ Error updating {requirements_path}: {e}")

def detect_conda_dependencies(project_dir):
    """Extract installed Conda dependencies and update config/environment.yml."""
    config_dir = os.path.join(project_dir, "config")
    os.makedirs(config_dir, exist_ok=True)  # Ensure config directory exists

    env_path = os.path.join(config_dir, "environment.yml")
    try:
        output = subprocess.check_output(["conda", "env", "export"], text=True)
        env_data = yaml.safe_load(output)

        # Remove build numbers for cleaner output
        if "dependencies" in env_data:
            env_data["dependencies"] = [dep.split("=")[0] if isinstance(dep, str) else dep for dep in env_data["dependencies"]]

        # Save YAML file
        with open(env_path, "w") as f:
            yaml.dump(env_data, f, default_flow_style=False)

        print(f"✅ Updated Conda dependencies in {env_path}")
    except Exception as e:
        print(f"❌ Error updating {env_path}: {e}")

if __name__ == "__main__":
    # Get the current directory as the project directory
    project_directory = os.getcwd()

    print(f"🔍 Updating dependencies in {project_directory}/config/...")

    # Detect and update pip packages
    detect_pip_dependencies(project_directory)

    # Detect and update conda packages (if conda is available)
    if "CONDA_PREFIX" in os.environ:
        detect_conda_dependencies(project_directory)
    else:
        print("⚠️ Conda not detected. Skipping environment.yml update.")

    print("🎯 Dependencies successfully updated in config/!")

