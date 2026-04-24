from pydantic import BaseModel, Field


class ReverseInvoiceRequest(BaseModel):
    biz_content: dict = Field(..., description="支付宝 alipay.ebpp.invoice.info.send 的业务参数")
