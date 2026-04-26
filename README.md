# PyFast

Python + FastAPI service.

## Dependency management (Poetry)

1. Install Poetry:
   - [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)
2. Install project dependencies:
   - `poetry install`
3. Run service:
   - `poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

## MySQL production baseline

1. Copy env template:
   - `copy .env.example .env` (Windows)
2. Update DB variables in `.env`:
   - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
3. Tune pool and timeout in production:
   - `DB_POOL_SIZE`, `DB_MAX_OVERFLOW`, `DB_POOL_RECYCLE`, `DB_POOL_TIMEOUT`
   - `DB_CONNECT_TIMEOUT`, `DB_READ_TIMEOUT`, `DB_WRITE_TIMEOUT`
4. Application startup now checks DB connectivity with `SELECT 1`, and shutdown disposes the engine.

## Alipay reverse invoice (certificate mode)

This project uses the official `alipay-sdk-python` and constructs `DefaultAlipayClient`
in certificate mode for reverse invoice integration.

1. Install dependencies:
   - `poetry install`
2. Configure environment variables:
   - `ALIPAY_APP_ID`
   - `ALIPAY_PRIVATE_KEY` (app private key content)
   - `ALIPAY_APP_CERT_PATH`
   - `ALIPAY_PUBLIC_CERT_PATH`
   - `ALIPAY_ROOT_CERT_PATH`
   - optional: `ALIPAY_GATEWAY`, `ALIPAY_CHARSET`, `ALIPAY_SIGN_TYPE`, `ALIPAY_ENCRYPT_KEY`
   - The project now loads these by `pydantic-settings` from `.env` automatically.

Example `.env`:

```env
ALIPAY_APP_ID=2021000000000000
ALIPAY_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----...-----END PRIVATE KEY-----
ALIPAY_APP_CERT_PATH=D:/certs/appCertPublicKey.crt
ALIPAY_PUBLIC_CERT_PATH=D:/certs/alipayCertPublicKey_RSA2.crt
ALIPAY_ROOT_CERT_PATH=D:/certs/alipayRootCert.crt
ALIPAY_GATEWAY=https://openapi.alipay.com/gateway.do
ALIPAY_CHARSET=utf-8
ALIPAY_SIGN_TYPE=RSA2
```
3. Call endpoint:
   - `POST /api/invoice/reverse/sign`
   - body:
     - `{"biz_content": {...}}`

The endpoint sends request for method `alipay.ebpp.invoice.info.send` via official SDK.
