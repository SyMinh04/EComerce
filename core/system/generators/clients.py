import uuid
import hashlib


class BaseHashGenerator:
    def hash(self):
        raise NotImplementedError("Subclasses must implement the hash() method")


class ClientIdGenerator(BaseHashGenerator):
    def hash(self):
        return str(uuid.uuid4())


class ClientSecretGenerator(BaseHashGenerator):
    def hash(self):
        random_uuid = uuid.uuid4()
        return hashlib.sha256(str(random_uuid).encode()).hexdigest()
