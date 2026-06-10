from pathlib import Path

import yaml

from .io import (
    compile_tex_and_clean_up,
    create_img_folder,
    get_latest_file,
    read_template,
    save_icons,
    update_and_save_photo,
)
from .fill import clean_unused_tags, fill_template


def run_latex_yaml(input_folder_path: Path = None, config_path: Path = None, output_folder_path: Path = None) -> None:
    if not input_folder_path and not config_path:
        raise ValueError("Either input_folder_path or config_path must be provided")

    if input_folder_path:
        if not output_folder_path:
            output_folder_path = input_folder_path

        config_path_from_input_folder = get_latest_file(input_folder_path, ext=".yml")

        run_latex_yaml_from_cfg(config_path_from_input_folder, output_folder_path)

    if config_path:
        if not output_folder_path:
            output_folder_path = config_path.parent

        run_latex_yaml_from_cfg(config_path, output_folder_path)


def run_latex_yaml_from_cfg(cfg_path: Path, output_folder_path: Path) -> None:
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)

    create_img_folder(output_folder_path)

    cfg = update_and_save_photo(cfg, cfg_path.parent, output_folder_path)

    icons_color = str(cfg["colors"]["accent"])

    save_icons(output_folder_path, icons_color)

    template_path = cfg["template"]

    template = read_template(template_path)

    template_filled = fill_template(cfg, template)

    template_filled_clean = clean_unused_tags(template_filled)

    cv_output_path = output_folder_path / (cfg_path.stem + ".tex")

    with open(cv_output_path, "w") as f:
        f.write(template_filled_clean)

    compile_tex_and_clean_up(cv_output_path)
