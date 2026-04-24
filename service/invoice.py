from service.alipay_client import get_alipay_client


def build_reverse_invoice_signed_request(biz_content: dict) -> str:
    client = get_alipay_client()
    payload = client.build_body("alipay.ebpp.invoice.info.send", biz_content)
    return client.sign_data(payload)
