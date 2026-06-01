from auth.utils import hash_password, verify_password

# from tests.utils import sample_user
import pytest
@pytest.fixture
def sample_user():
    return {"id":1, "name":"Alice", "password": "secret123"}




def test_verify_password_accepts_correct_password(sample_user):
    hashed = hash_password(sample_user["password"])
    assert verify_password(sample_user["password"], hashed) is True


def test_verify_password_rejects_wrong_password(sample_user):
    hashed = hash_password(sample_user["password"])
    assert verify_password("wrong-pass", hashed) is False


def test_verify_password_reject_empty_string(sample_user):
    hashed = hash_password(sample_user["password"])
    assert verify_password("", hashed) is False