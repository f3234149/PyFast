import json

from alipay.aop.api.response.AlipayEbppInvoiceInfoSendResponse import (
    AlipayEbppInvoiceInfoSendResponse,
)

from service.alipay_client import get_alipay_client


def send_reverse_invoice(biz_content: dict) -> dict:
    try:
        from alipay.aop.api.request.AlipayEbppInvoiceInfoSendRequest import (
            AlipayEbppInvoiceInfoSendRequest,
        )
    except ImportError as exc:
        raise RuntimeError(
            "Current alipay-sdk-python version does not expose "
            "AlipayEbppInvoiceInfoSendRequest. Please upgrade SDK."
        ) from exc

    client = get_alipay_client()
    request = AlipayEbppInvoiceInfoSendRequest()
    request.biz_content = json.dumps(biz_content, ensure_ascii=False)

    response_content = client.execute(request)
    response = AlipayEbppInvoiceInfoSendResponse()
    response.parse_response_content(response_content)
    return {
        "is_success": response.is_success(),
        "code": response.code,
        "msg": response.msg,
        "sub_code": response.sub_code,
        "sub_msg": response.sub_msg,
        "body": response.body,
    }
