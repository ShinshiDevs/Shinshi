import os
from pathlib import Path

root_dir: Path = Path(os.getcwd())
dotenv_file = root_dir / "secrets" / "app.env"
logging_dir: Path = root_dir / "logging"
resources_dir: Path = root_dir / "resources"
images_dir: Path = resources_dir / "images"
