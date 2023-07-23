import pytest
from flagbuddy.flagbuddy import validate_ip, load_advice

def test_validate_ip():
    assert validate_ip('192.168.1.1')  # valid IP
    with pytest.raises(ValueError):
        validate_ip('999.999.999.999')  # invalid IP

def test_load_advice():
    advice = load_advice('port_advice.json')
    assert isinstance(advice, dict)
    assert '22' in advice
