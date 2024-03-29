import hashlib
import sqlite3 as sl
import asyncio


async def get_hash(key: int) -> str:
    print((int(hashlib.sha256(str(key).encode()).hexdigest(),16)))
    # print(len(str(int(hashlib.sha256(str(key).encode()).hexdigest(),16))))
    return (int(hashlib.sha256(str(key).encode()).hexdigest(),16))%1000000000


# async def get_user(primary_key: int, additional_key: str):
#     users = sl.connect('core/users.db')
#     cursor = users.cursor()
#     exists = cursor.execute("SELECT 1 FROM users use WHERE id = ?", [primary_key]).fetchone()
#     print(exists)
#     if not exists:
#         return False
#     additional_key_user = cursor.execute("SELECT additional_key FROM users WHERE id=?", [primary_key]).fetchone()
#     if additional_key_user == additional_key:
#         return primary_key
#     return get_user(get_hash(primary_key))



