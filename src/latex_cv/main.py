import yaml
from pathlib import Path

from .latex_cv import run_latex_yaml

if __name__ == "__main__":
    project_root_folder_path = Path(__file__).parent.parent.parent

    with open(project_root_folder_path / "config.yml", "r") as f:
        config = yaml.safe_load(f)

    input_folder = config["input_folder"]
    output_folder = config["output_folder"]

    input_path = (project_root_folder_path / input_folder).resolve()
    output_path = (project_root_folder_path / output_folder).resolve()

    run_latex_yaml(input_folder_path=input_path, output_folder_path=output_path)