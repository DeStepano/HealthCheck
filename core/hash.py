import hashlib
import sqlite3 as sl

async def get_hash(key: int) -> str:
    return (int(hashlib.sha256(str(key).encode()).hexdigest(),16))%1000000000


# def get_user(user_id: int, current_add_key:str):
#     users = sl.connect('core/users.db')
#     cur = users.cursor()
#     print("Текущее id и add_key:")
#     print(current_add_key)
#     print(user_id)
#     exists = cur.execute("SELECT 1 FROM users use WHERE id = ?", [user_id]).fetchone()
#     # print("EXISTS:")
#     # print(exists)
#     if not exists:
#         return False
#     add_key = cur.execute("SELECT additional_key FROM users WHERE id=?", [user_id]).fetchone()
#     add_key = add_key[0]
#     print("add_key in bd:")
#     print(add_key)
#     if(add_key == current_add_key):
#         return user_id
#     new_id, new_add_key = get_hash(user_id)
#     return get_user(new_id, new_add_key)

