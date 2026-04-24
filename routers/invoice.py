from fastapi import APIRouter, HTTPException

from schemas.invoice import ReverseInvoiceRequest
from service import invoice as invoice_service

router = APIRouter(prefix="/api/invoice", tags=["invoice"])


@router.post("/reverse/sign")
async def reverse_invoice_sign(req: ReverseInvoiceRequest):
    try:
        signed_request = invoice_service.build_reverse_invoice_signed_request(req.biz_content)
        return {
            "code": 200,
            "message": "success",
            "method": "alipay.ebpp.invoice.info.send",
            "signed_request": signed_request,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"alipay reverse invoice sign failed: {exc}") from exc
