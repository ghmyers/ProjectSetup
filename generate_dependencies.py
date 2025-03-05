#!/usr/bin/env python3
import subprocess
import sys
import os
import yaml

def detect_pip_dependencies(project_dir):
    """Extract installed pip dependencies and save to the project's requirements.txt."""
    requirements_path = os.path.join(project_dir, "requirements.txt")
    try:
        output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"], text=True)
        with open(requirements_path, "w") as f:
            f.write(output)
        print(f"✅ Saved pip dependencies to {requirements_path}")
    except Exception as e:
        print(f"❌ Error generating {requirements_path}: {e}")

def detect_conda_dependencies(project_dir):
    """Extract installed Conda dependencies and save to the project's environment.yml."""
    env_path = os.path.join(project_dir, "environment.yml")
    try:
        output = subprocess.check_output(["conda", "env", "export"], text=True)
        env_data = yaml.safe_load(output)
        
        # Remove version numbers for cleaner output
        env_data["dependencies"] = [dep.split("=")[0] if isinstance(dep, str) else dep for dep in env_data["dependencies"]]

        # Save YAML
        with open(env_path, "w") as f:
            yaml.dump(env_data, f, default_flow_style=False)
        
        print(f"✅ Saved Conda dependencies to {env_path}")
    except Exception as e:
        print(f"❌ Error generating {env_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_dependencies.py <project_directory>")
        sys.exit(1)
    
    project_directory = sys.argv[1]

    if not os.path.exists(project_directory):
        print(f"❌ Error: Project directory {project_directory} does not exist!")
        sys.exit(1)

    print("🔍 Detecting dependencies...")

    # Detect pip packages
    detect_pip_dependencies(project_directory)

    # Detect conda packages (if conda is available)
    if "CONDA_PREFIX" in os.environ:
        detect_conda_dependencies(project_directory)
    else:
        print("⚠️ Conda not detected. Skipping environment.yml generation.")

    print("🎯 Dependency files created successfully!")

