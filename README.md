# PyFast
python、fastapi

## Alipay reverse invoice (certificate mode)

This project provides a certificate-mode Alipay client for reverse invoice integration.

1. Install dependencies:
   - `pip install -r requirements.txt`
2. Configure environment variables:
   - `ALIPAY_APP_ID`
   - `ALIPAY_APP_PRIVATE_KEY_PATH`
   - `ALIPAY_APP_PUBLIC_CERT_PATH`
   - `ALIPAY_PUBLIC_CERT_PATH`
   - `ALIPAY_ROOT_CERT_PATH`
   - optional: `ALIPAY_NOTIFY_URL`, `ALIPAY_SIGN_TYPE`, `ALIPAY_DEBUG`
3. Call endpoint:
   - `POST /api/invoice/reverse/sign`
   - body:
     - `{"biz_content": {...}}`

The endpoint signs request parameters for method `alipay.ebpp.invoice.info.send`.
