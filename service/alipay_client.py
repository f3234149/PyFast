from functools import lru_cache

from alipay import DCAliPay

from config.alipay_conf import AlipaySettings


@lru_cache(maxsize=1)
def get_alipay_client() -> DCAliPay:
    cert_materials = AlipaySettings.load_cert_materials()
    return DCAliPay(
        appid=AlipaySettings.app_id,
        app_notify_url=AlipaySettings.notify_url,
        sign_type=AlipaySettings.sign_type,
        debug=AlipaySettings.debug,
        app_private_key_string=cert_materials["app_private_key_string"],
        app_public_key_cert_string=cert_materials["app_public_key_cert_string"],
        alipay_public_key_cert_string=cert_materials["alipay_public_key_cert_string"],
        alipay_root_cert_string=cert_materials["alipay_root_cert_string"],
    )
