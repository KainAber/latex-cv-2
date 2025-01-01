import logging
import shutil
import subprocess  # nosec
from pathlib import Path

from PIL import Image

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def get_latest_file(folder_path: Path, ext="") -> Path:
    # Check that path is a directory
    if not folder_path.is_dir():
        raise ValueError(f"The path {folder_path} is not a directory.")

    # Get all files in the directory
    files = [file for file in folder_path.iterdir() if file.is_file()]

    # Filter by file extension
    if ext:
        files = [f for f in files if f.suffix == ext]

    # Throw error if no path was found
    if not files:
        raise FileNotFoundError(
            f"No file found in {folder_path}{' with extension ' + ext if ext else ''}"
        )

    # Find the file with the latest change date
    latest_file = max(files, key=lambda f: f.stat().st_mtime, default=None)

    # Return latest path to file
    return latest_file


def read_template(template_name: str) -> str:
    # Construct path to template
    template_path = Path(__file__).parent / "templates" / (template_name + ".tex")

    # Read template
    with open(template_path, "r") as f:
        template = f.read()

    # Return template
    return template


def save_icons(output_folder_path: Path, icons_color: str) -> None:
    # Construct img folder path
    img_folder_path = Path(__file__).parent / "templates" / "img"

    # Get the list of files in the input folder
    icon_file_paths = [f for f in img_folder_path.iterdir() if f.suffix == ".png"]

    # Iterate through each icon file path
    for icon_file_path in icon_file_paths:
        # Define new icon name
        new_icon_name = f"_{icons_color}_" + icon_file_path.name

        # Create output path
        colored_icon_file_path = output_folder_path / "img" / new_icon_name

        # Generate new icon
        create_colored_icon(icon_file_path, colored_icon_file_path, icons_color)


def create_colored_icon(
    input_icon_path: Path, output_icon_path: Path, html_color: str
) -> None:
    # Convert HTML to RGB
    r_new, g_new, b_new = tuple(
        int(html_color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)
    )

    # Load pixels
    img = Image.open(input_icon_path).convert("RGBA")

    # Load pixel data
    pixels = img.load()

    # Iterate through each pixel
    for y in range(img.height):
        for x in range(img.width):
            # Get RGBA values
            _, _, _, a = pixels[x, y]

            # Replace values
            pixels[x, y] = (r_new, g_new, b_new, a)

    # Save the image
    img.save(output_icon_path)


def create_img_folder(output_folder_path: Path) -> None:
    # Create path
    img_folder_path = output_folder_path / "img"

    # Create folder
    if not img_folder_path.is_dir():
        img_folder_path.mkdir(parents=True)


def update_and_save_photo(
    cfg: dict, input_folder_path: Path, output_folder_path: Path
) -> dict:
    # Extract photo path
    photo_path_str = cfg["personal info"]["photo"]

    # Construct photo path
    photo_path = (input_folder_path / photo_path_str).resolve()

    # Extract name
    photo_file_name = Path(photo_path).name

    # Clean photo file name
    photo_file_name_clean = photo_file_name.replace(" ", "_")

    # Construct new photo path
    new_photo_path = output_folder_path / "img" / photo_file_name_clean

    # Copy file
    shutil.copy(photo_path, new_photo_path)

    # Update location in config
    cfg["personal info"]["photo"] = Path("img") / photo_file_name_clean

    return cfg


def compile_tex(tex_file_path: Path) -> None:
    # Get tex folder
    tex_folder_path = Path(tex_file_path).parent

    # Log the compilation
    logger.info(f"Compiling pdf to folder {tex_folder_path}")

    # Compile the tex file
    subprocess.run(
        [
            "latexmk",
            "-quiet",
            "-pdf",
            f"-output-directory={str(tex_folder_path)}",
            f"{str(tex_file_path)}",
        ]
    )  # nosec

    # Log the compilation
    logger.info(f"Compiled pdf to folder {tex_folder_path}")

    # Log cleanup
    logger.info("Cleaning compilation directory")

    # Cleaning up auxilliary files
    subprocess.run(
        [
            "latexmk",
            "-quiet",
            "-c",
            f"-output-directory={str(tex_folder_path)}",
            f"{str(tex_file_path)}",
        ]
    )  # nosec

    # Logging cleanup
    logger.info("Finsihed cleanup")


def open_pdf(cv_path: Path) -> None:
    subprocess.run(
        [
            "open",
            str(cv_path).replace(".tex", ".pdf"),
        ]
    )  # nosec
