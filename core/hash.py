import hashlib
import sqlite3 as sl

async def get_hash(key: int) -> list:
    hash_id = int(hashlib.sha256(str(key).encode()).hexdigest(),16)
    key = hash_id%1000000000
    additional_key = str(hash_id//1000000000)
    return [key, additional_key]


async def get_hash_string(name):
    hash_name = hashlib.sha256(str(name).encode()).hexdigest()
    return hash_name