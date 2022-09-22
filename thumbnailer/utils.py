import random
import string
import hmac
import hashlib
from config import conf
def generateRandomString(length: int = 13) -> str:
	return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def hmacSign(data) -> str:
	if not isinstance(data, bytes):
		data = str(data).encode("UTF-8")
	return hmac.new(conf["hmackey"], msg=data, digestmod=hashlib.sha3_384).hexdigest()


def hmacVerify(data, signature: str) -> bool:
	return hmac.compare_digest(hmacSign(data), signature)


