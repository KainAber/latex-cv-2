from pathlib import Path

import yaml

from src.io_utils import (
    compile_tex,
    create_img_folder,
    get_latest_file,
    open_pdf,
    read_template,
    save_icons,
    update_and_save_photo,
)
from src.latex_cv import clean_unused_tags, fill_template


def run_engine(input_folder_path: Path, output_folder_path: Path) -> None:

    # Get latest config path
    cfg_path = get_latest_file(input_folder_path, ext=".yml")

    # Read config
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)

    # Create img folder
    create_img_folder(output_folder_path)

    # Update photo
    cfg = update_and_save_photo(cfg, input_folder_path, output_folder_path)

    # Extract icons color
    icons_color = str(cfg["colors"]["icons"])

    # Save icons
    save_icons(output_folder_path, icons_color)

    # Extract template name
    template_name = cfg["template"]

    # Read template
    template = read_template(template_name)

    # Fill template
    template_filled = fill_template(cfg, template)

    # Clean CV
    template_filled_clean = clean_unused_tags(template_filled)

    # Construct output path
    cv_output_path = output_folder_path / (cfg_path.stem + ".tex")

    # Save CV
    with open(cv_output_path, "w") as f:
        f.write(template_filled_clean)

    # Compile CV
    compile_tex(cv_output_path)

    # Open pdf
    open_pdf(cv_output_path)


if __name__ == "__main__":
    # Get project root path
    project_root_folder_path = Path(__file__).parent

    # Read the main config
    with open(project_root_folder_path / "config.yml", "r") as f:
        config = yaml.safe_load(f)

    # Extract input and output paths
    input_folder = config["input_folder"]
    output_folder = config["output_folder"]

    # Construct absolute input and output paths
    input_path = (project_root_folder_path / input_folder).resolve()
    output_path = (project_root_folder_path / output_folder).resolve()

    # Run engine
    run_engine(input_path, output_path)
