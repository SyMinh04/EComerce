from faker import Faker
from nanoid import generate
from .uuidv7 import uuid7

ALPHANUMERIC = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
ALPHABET_ONLY = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def generate_uuid():
    """
    Generate uuid
    @return:
    """
    return uuid7()


def generate_public_id(size=15):
    """
    Generate public id
    @param size:
    @return:
    """
    return generate_nano_id(size=size)


def generate_nano_id(alphabet: str = ALPHANUMERIC, size=15):
    """
    Generate nano id
    @param alphabet:
    @param size:
    @return:
    """
    return generate(alphabet=alphabet, size=size)


def generate_sonyflake_id(size: int):
    """
    Generate sonyflake id
    @param size:
    @return:
    """
    faker = Faker()
    flake_id = faker.uuid4()
    code = str(flake_id)

    if len(code) < size:
        code = code.zfill(size)

    return code


__all__ = (
    'generate_uuid',
    'generate_nano_id',
    'generate_public_id',
    'generate_sonyflake_id',
    'ALPHABET_ONLY',
    'ALPHANUMERIC'
)
