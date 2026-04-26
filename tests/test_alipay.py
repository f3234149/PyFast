import asyncio
import json
import pprint

from sqlalchemy import text

from config.db_conf import AsyncSessionLocal
from service.alipay_client import get_alipay_client


async def _run_case() -> None:
    # 1) 查询 company_info(id=2523)，拿税号字段 licenseNumber
    async with AsyncSessionLocal() as db:
        row_result = await db.execute(
            text(
                "SELECT id, companyName, licenseNumber "
                "FROM company_info WHERE id=:id LIMIT 1"
            ),
            {"id": 2523},
        )
        company_row = row_result.mappings().first()
        assert company_row is not None, "company_info 未找到 id=2523 的记录"

        tax_no = company_row["licenseNumber"]
        assert tax_no, "company_info.id=2523 的 licenseNumber 为空"
        print("\n【1】数据库查询结果：")
        pprint.pprint(dict(company_row), indent=2)
        print("税号：",tax_no)
        # 2) 调用支付宝反向企业查询接口
        try:
            from alipay.aop.api.request.AlipayCommerceEcRecyclinginvoiceCompanyQueryRequest import (
                AlipayCommerceEcRecyclinginvoiceCompanyQueryRequest,
            )
            from alipay.aop.api.response.AlipayCommerceEcRecyclinginvoiceCompanyQueryResponse import (
                AlipayCommerceEcRecyclinginvoiceCompanyQueryResponse,
            )
        except ImportError as exc:
            raise RuntimeError(
                "当前 alipay-sdk-python 版本缺少 "
                "AlipayCommerceEcRecyclinginvoiceCompanyQuery* 类，请升级 SDK。"
            ) from exc

        client = get_alipay_client()

        request = AlipayCommerceEcRecyclinginvoiceCompanyQueryRequest()
        # request.biz_content = json.dumps({"tax_no": tax_no}, ensure_ascii=False)
        request.biz_content = {"tax_no": tax_no}
        print("\n【2】请求体：")
        pprint.pprint(request.biz_content.__dict__, indent=2)
        # return
        response_content = client.execute(request)
        response = AlipayCommerceEcRecyclinginvoiceCompanyQueryResponse()
        response.parse_response_content(response_content)

        api_result = {
            "is_success": response.is_success(),
            "code": response.code,
            "msg": response.msg,
            "sub_code": response.sub_code,
            "sub_msg": response.sub_msg,
            "body": response.body,
            "company_name": getattr(response, "company_name", None),
        }
        print("\n【2】支付宝接口返回：")
        pprint.pprint(api_result, indent=2)
        assert response.is_success(), f"支付宝接口调用失败: {api_result}"

        # 3) 用查询到的 company_name 回写 company_info.companyName
        company_name = getattr(response, "company_name", None)
        assert company_name, "支付宝返回中不存在 company_name，无法回写 company_info.companyName"

        await db.execute(
            text("UPDATE company_info SET companyName=:company_name WHERE id=:id"),
            {"company_name": company_name, "id": 2523},
        )
        await db.commit()

        verify_result = await db.execute(
            text("SELECT id, companyName FROM company_info WHERE id=:id"),
            {"id": 2523},
        )
        updated_row = verify_result.mappings().first()
        print("\n【3】数据库回写后结果：")
        pprint.pprint(dict(updated_row) if updated_row else None, indent=2)


def test_alipay_company_query_and_update_company_name():
    asyncio.run(_run_case())
