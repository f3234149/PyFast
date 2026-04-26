import pprint

from config.db_conf import get_db
from service.alipay_client import get_alipay_client

def test_alipay_client():
    client = get_alipay_client()

    # 打印顶层属性
    print("\n【1】客户端顶层属性：")
    pprint.pprint(client.__dict__, indent=2)

    # 打印内部 config 完整内容（关键！）
    print("\n【2】支付宝完整配置信息：")
    config = client._DefaultAlipayClient__config
    pprint.pprint(config.__dict__, indent=2)

    # 最终断言
    assert client is not None
    print("\n✅ alipay client创建成功！")
