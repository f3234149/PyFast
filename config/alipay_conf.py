import os


def _read_text_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        return file.read().strip()


class AlipaySettings:
    gateway: str = os.getenv("ALIPAY_GATEWAY", "https://openapi.alipay.com/gateway.do")
    app_id: str = os.getenv("ALIPAY_APP_ID", "")
    sign_type: str = os.getenv("ALIPAY_SIGN_TYPE", "RSA2")
    notify_url: str | None = os.getenv("ALIPAY_NOTIFY_URL")
    debug: bool = os.getenv("ALIPAY_DEBUG", "false").lower() == "true"

    app_private_key_path: str = os.getenv("ALIPAY_APP_PRIVATE_KEY_PATH", "")
    app_public_cert_path: str = os.getenv("ALIPAY_APP_PUBLIC_CERT_PATH", "")
    alipay_public_cert_path: str = os.getenv("ALIPAY_PUBLIC_CERT_PATH", "")
    alipay_root_cert_path: str = os.getenv("ALIPAY_ROOT_CERT_PATH", "")

    @classmethod
    def validate(cls) -> None:
        required_values = {
            "ALIPAY_APP_ID": cls.app_id,
            "ALIPAY_APP_PRIVATE_KEY_PATH": cls.app_private_key_path,
            "ALIPAY_APP_PUBLIC_CERT_PATH": cls.app_public_cert_path,
            "ALIPAY_PUBLIC_CERT_PATH": cls.alipay_public_cert_path,
            "ALIPAY_ROOT_CERT_PATH": cls.alipay_root_cert_path,
        }
        missing = [key for key, value in required_values.items() if not value]
        if missing:
            raise ValueError(f"Missing Alipay settings: {', '.join(missing)}")

    @classmethod
    def load_cert_materials(cls) -> dict[str, str]:
        cls.validate()
        return {
            "app_private_key_string": _read_text_file(cls.app_private_key_path),
            "app_public_key_cert_string": _read_text_file(cls.app_public_cert_path),
            "alipay_public_key_cert_string": _read_text_file(cls.alipay_public_cert_path),
            "alipay_root_cert_string": _read_text_file(cls.alipay_root_cert_path),
        }
