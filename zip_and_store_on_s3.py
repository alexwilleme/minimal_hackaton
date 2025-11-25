"""A script to zip all relevant files of the project and store in to S3. They are used to setup the EC2 API."""
import zipfile
from io import BytesIO
from pathlib import Path

from app.config import ConfigManager, find_project_root
from app.tools.aws import Aws

if __name__ == "__main__":
    CONFIG = ConfigManager().get_config()

    root_path = find_project_root(start_path=Path(__file__))
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for folder in ["app", "api"]:
            app_path = root_path / folder
            for file_path in app_path.rglob('*'):
                # Exclude folders starting with __
                if any((part.startswith("__") and part != "__init__.py") for part in file_path.parts):
                    continue
                if file_path.is_file():  # Only include files
                    zipf.write(file_path, file_path.relative_to(root_path))

        # Add pyproject.toml and poetry.lock if they exist
        for file_name in ["main.py", "pyproject.toml", "scripts/ec2_first_install.sh", "scripts/install_and_run_api_on_ec2.sh", "poetry.lock", "scripts/run_api_on_ec2.sh"]:
            file_path = root_path / file_name
            if file_path.exists():
                zipf.write(file_path, file_path.relative_to(root_path))

        file_path = root_path / "scripts/.env_for_ec2"
        target_path = root_path / ".env"
        zipf.write(file_path, target_path.relative_to(root_path))

    zip_buffer.seek(0)

    ZIP_PATH = "backend.zip"
    Aws().s3.upload_fileobj(zip_buffer, CONFIG.S3_BUCKET, ZIP_PATH)
