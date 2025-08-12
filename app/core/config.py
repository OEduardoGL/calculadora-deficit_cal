from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "CalCalc API"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    BACKEND_CORS_ORIGINS: Union[List[str], str, dict] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = SettingsConfigDict(
        env_file=".env.app",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v):
        if isinstance(v, dict):
            try:
                return [v[k] for k in sorted(v.keys(), key=lambda x: int(x))]
            except Exception:
                return list(v.values())

        if isinstance(v, list):
            return v

        if isinstance(v, str):
            s = v.strip()
            if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
                s = s[1:-1].strip()
            if s.startswith("["):
                try:
                    return json.loads(s)
                except Exception:
                    pass
            return [item.strip() for item in s.split(",") if item.strip()]
        # fallback
        return v

settings = Settings()
