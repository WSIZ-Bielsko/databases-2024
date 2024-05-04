from uuid import uuid4

from src.kudos.model import Kudo


def test_abra_kadabra():
    a = 10
    b = 12
    assert a + b == 22


def test_use_app_modules():
    z = Kudo(id=uuid4(), purpose="test", owner_id="s4444")
    assert z.purpose.startswith("test")
    s = z.model_dump()
    assert isinstance(s, dict)
    assert "owner_id" in s
