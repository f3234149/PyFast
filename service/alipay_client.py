from functools import lru_cache

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from config.app_conf import get_alipay_config


@lru_cache(maxsize=1)
def get_alipay_client() -> DefaultAlipayClient:
    cfg = get_alipay_config()

    client_config = AlipayClientConfig()
    client_config.server_url = cfg.gateway
    client_config.app_id = cfg.app_id
    client_config.app_private_key = cfg.private_key
    client_config.charset = cfg.charset
    client_config.sign_type = cfg.sign_type
    client_config.app_cert_path = cfg.app_cert_path
    client_config.alipay_public_cert_path = cfg.alipay_public_cert_path
    client_config.root_cert_path = cfg.root_cert_path
    client_config.timeout = 30

    if cfg.encrypt_key:
        client_config.encrypt_key = cfg.encrypt_key

    return DefaultAlipayClient(alipay_client_config=client_config)
