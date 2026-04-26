from fastapi import APIRouter, HTTPException

from schemas.invoice import ReverseInvoiceRequest
from service import invoice as invoice_service

router = APIRouter(prefix="/api/invoice", tags=["invoice"])


@router.post("/reverse/sign")
async def reverse_invoice_sign(req: ReverseInvoiceRequest):
    try:
        result = invoice_service.send_reverse_invoice(req.biz_content)
        return {
            "code": 200,
            "message": "success",
            "method": "alipay.ebpp.invoice.info.send",
            "result": result,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"alipay reverse invoice request failed: {exc}") from exc
