from pathlib import Path

from pydantic import BaseSettings

project_dir = Path(__file__).parent.parent


class Settings(BaseSettings):
    """Class for managing settings"""

    DATA: Path = project_dir / "data"
    BOT_TOKEN: str
    URL: str
    TIME: int = 600
    CHANNEL_ID: int

    class Config:
        """Class for managing settings config"""

        env_file = ".env"
        case_sensitive = True


settings = Settings()  # type: ignore
