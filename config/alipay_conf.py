from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent


class AlipaySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    gateway: str = Field(
        default="https://openapi.alipay.com/gateway.do",
        alias="ALIPAY_GATEWAY",
    )
    app_id: str = Field(..., alias="ALIPAY_APP_ID")
    private_key: str = Field(
        ...,
        validation_alias=AliasChoices("ALIPAY_APP_PRIVATE_KEY_PATH", "ALIPAY_APP_PRIVATE_KEY_PATH"),
    )
    app_cert_path: str = Field(
        ...,
        validation_alias=AliasChoices("ALIPAY_APP_PUBLIC_CERT_PATH", "ALIPAY_APP_PUBLIC_CERT_PATH"),
    )
    alipay_public_cert_path: str = Field(
        ...,
        alias="ALIPAY_PUBLIC_CERT_PATH",
    )
    root_cert_path: str = Field(..., alias="ALIPAY_ROOT_CERT_PATH")

    charset: str = Field(default="utf-8", alias="ALIPAY_CHARSET")
    sign_type: str = Field(default="RSA2", alias="ALIPAY_SIGN_TYPE")
    encrypt_key: str | None = Field(default=None, alias="ALIPAY_ENCRYPT_KEY")
    notify_url: str | None = Field(default=None, alias="ALIPAY_NOTIFY_URL")


@lru_cache(maxsize=1)
def get_alipay_settings() -> AlipaySettings:
    return AlipaySettings()
