from functools import lru_cache

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient

from config.alipay_conf import get_alipay_settings


@lru_cache(maxsize=1)
def get_alipay_client() -> DefaultAlipayClient:
    settings = get_alipay_settings()

    client_config = AlipayClientConfig()
    client_config.server_url = settings.gateway
    client_config.app_id = settings.app_id
    client_config.app_private_key = settings.private_key
    client_config.charset = settings.charset
    client_config.sign_type = settings.sign_type

    # Certificate mode config.
    client_config.app_cert_path = settings.app_cert_path
    client_config.alipay_public_cert_path = settings.alipay_public_cert_path
    client_config.root_cert_path = settings.root_cert_path

    if settings.encrypt_key:
        client_config.encrypt_key = settings.encrypt_key

    return DefaultAlipayClient(alipay_client_config=client_config)
