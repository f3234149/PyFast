"""
Central configuration loader.

The ONLY file you need to change to switch active environment/tenant/database is .env:

    APP_ENV=prod
    APP_TENANT=xinnong
    APP_DB=nongyuebao

All actual configuration values (credentials, hosts, certs, pool params) live in
config/settings.yaml, organized as:

    <env> -> <tenant> -> alipay / databases -> <db_name>
"""
from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_YAML = Path(__file__).resolve().parent / "settings.yaml"


# ---------------------------------------------------------------------------
# Active profile selector — this is the ONE file you change: .env
# ---------------------------------------------------------------------------

class ActiveProfile(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_env: str = Field(default="dev", alias="APP_ENV")
    app_tenant: str = Field(default="qingdaoegong", alias="APP_TENANT")
    app_db: str = Field(default="nongyuebao", alias="APP_DB")


# ---------------------------------------------------------------------------
# Typed config models
# ---------------------------------------------------------------------------

@dataclass
class AlipayConfig:
    gateway: str
    app_id: str
    private_key: str
    app_cert_path: str
    alipay_public_cert_path: str
    root_cert_path: str
    charset: str = "utf-8"
    sign_type: str = "RSA2"
    encrypt_key: Optional[str] = None
    notify_url: Optional[str] = None


@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    name: str
    charset: str = "utf8mb4"
    pool_size: int = 20
    max_overflow: int = 30
    pool_timeout: int = 30
    pool_recycle: int = 1800
    echo: bool = False
    connect_timeout: int = 10
    read_timeout: int = 30
    write_timeout: int = 30

    @property
    def async_url(self) -> str:
        password = quote_plus(self.password)
        return (
            f"mysql+aiomysql://{self.user}:{password}"
            f"@{self.host}:{self.port}/{self.name}"
            f"?charset={self.charset}"
        )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _load_yaml() -> dict:
    if not SETTINGS_YAML.exists():
        raise FileNotFoundError(
            f"Config file not found: {SETTINGS_YAML}\n"
            "Copy config/settings.yaml.example to config/settings.yaml and fill in real values."
        )
    with SETTINGS_YAML.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


@lru_cache(maxsize=1)
def _active() -> ActiveProfile:
    return ActiveProfile()


def _resolve(p: str) -> str:
    """Resolve relative path against PROJECT_ROOT."""
    path = Path(p)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    return str(path)


def _read_pem(path: str) -> str:
    return Path(_resolve(path)).read_text(encoding="utf-8")


def _tenant_section(data: dict, env: str, tenant: str) -> dict:
    if env not in data:
        raise KeyError(f"APP_ENV='{env}' not found in settings.yaml. Available: {list(data)}")
    if tenant not in data[env]:
        raise KeyError(
            f"APP_TENANT='{tenant}' not found under env '{env}'. "
            f"Available: {list(data[env])}"
        )
    return data[env][tenant]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def get_alipay_config() -> AlipayConfig:
    profile = _active()
    section = _tenant_section(_load_yaml(), profile.app_env, profile.app_tenant)["alipay"]

    private_key_path = section.get("private_key_path")
    private_key = _read_pem(private_key_path) if private_key_path else section["private_key"]

    return AlipayConfig(
        gateway=section.get("gateway", "https://openapi.alipay.com/gateway.do"),
        app_id=section["app_id"],
        private_key=private_key,
        app_cert_path=_resolve(section["app_cert_path"]),
        alipay_public_cert_path=_resolve(section["alipay_public_cert_path"]),
        root_cert_path=_resolve(section["root_cert_path"]),
        charset=section.get("charset", "utf-8"),
        # sign_type=section.get("sign_type", "RSA2"),
        encrypt_key=section.get("encrypt_key"),
        notify_url=section.get("notify_url"),
    )


@lru_cache(maxsize=1)
def get_db_config() -> DBConfig:
    profile = _active()
    data = _load_yaml()
    tenant = _tenant_section(data, profile.app_env, profile.app_tenant)
    databases = tenant.get("databases", {})
    if profile.app_db not in databases:
        raise KeyError(
            f"APP_DB='{profile.app_db}' not found under "
            f"env='{profile.app_env}' tenant='{profile.app_tenant}'. "
            f"Available: {list(databases)}"
        )
    s = databases[profile.app_db]
    return DBConfig(
        host=s.get("host", "127.0.0.1"),
        port=int(s.get("port", 3306)),
        user=s.get("user", "root"),
        password=s.get("password", ""),
        name=s["name"],
        charset=s.get("charset", "utf8mb4"),
        pool_size=int(s.get("pool_size", 20)),
        max_overflow=int(s.get("max_overflow", 30)),
        pool_timeout=int(s.get("pool_timeout", 30)),
        pool_recycle=int(s.get("pool_recycle", 1800)),
        echo=bool(s.get("echo", False)),
        connect_timeout=int(s.get("connect_timeout", 10)),
        read_timeout=int(s.get("read_timeout", 30)),
        write_timeout=int(s.get("write_timeout", 30)),
    )
