#!/usr/bin/env python3
import os
import sys
from datetime import datetime

# Standard boilerplate for `src/` scripts
SRC_TEMPLATE = """\"\"\"
TITLE: [Module Name]
AUTHOR: [Your Name]
DATE: {date}
DESCRIPTION: [Brief description of what this module does]
\"\"\"

#!/usr/bin/env python3
import os
import sys

# Get project directory dynamically
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(PROJECT_DIR)

# Ensure PROJECT_DIR is in sys.path for imports
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

# Append src/ to Python's module search path
sys.path.append(os.path.join(PROJECT_DIR, "src"))

# Import logging
from logging_setup import setup_logging
logger = setup_logging(log_dir="logs", log_filename=)
logger.info(f"Module initialized: {{os.path.basename(__file__)}}")

# Your module functions here...
"""

def create_src_script(script_name, title="Script Name", description="Contains functions related to this module"):
    """Creates a new Python script inside the `src/` directory with the standard boilerplate."""

    project_root = os.getcwd()

    file_path = os.path.join(project_root, f"{script_name}.py")

    if os.path.exists(file_path):
        print(f"⚠️ File '{file_path}' already exists. Skipping...")
        return

    template = SRC_TEMPLATE.format(
        title=title,
        date=datetime.today().strftime('%Y-%m-%d'),
        description=description
    )

    with open(file_path, "w") as f:
        f.write(template)

    print(f"✅ Created /{script_name}.py` with standard structure.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python initialize_src.py <script_name> [title] [description]")
    else:
        script_name = sys.argv[1]
        title = sys.argv[2] if len(sys.argv) > 2 else "Script Name"
        description = sys.argv[3] if len(sys.argv) > 3 else "Contains functions related to this module"
        create_src_script(script_name, title, description)

