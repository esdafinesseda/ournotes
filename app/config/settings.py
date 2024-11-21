from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # Database settings
    DB_URL: str

    # Pinecone settings
    PC_API_KEY: str
    PC_CLOUD: str
    PC_REGION: str
    PC_METRIC: str
    PC_INDEX_NAME: str

    # Embedding settings
    HF_MODEL: str
    EMB_DIM: int

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Our Notes"

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_settings() -> Settings:
    return Settings()
