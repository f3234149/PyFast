"""
Alipay configuration — thin re-export from app_conf.

All actual values live in config/settings.yaml.
Active profile is selected via .env (APP_ENV / APP_TENANT).
"""
from config.app_conf import AlipayConfig, get_alipay_config

__all__ = ["AlipayConfig", "get_alipay_config"]
