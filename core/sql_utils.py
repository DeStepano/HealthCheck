import asyncpg
import asyncio
import pytest
import time
import pytest_asyncio
import hashlib
import sqlite3 as sl
from core.config import config
from core.hash import get_hash
import json
import random


async def connect_to_postgres():
    conn = await asyncpg.connect(
        host=config.users_db_host,
        port=config.user_db_port,
        user=config.user_db_user,
        password=config.users_db_password,
        database=config.users_db_database
    )
    return conn


async def create_users_table(conn):
    async with conn.transaction():
        await conn.execute(
                    '''CREATE TABLE IF NOT EXISTS users
                	(key INTEGER,
                    additional_key TEXT,
                    name TEXT,
                    age INTEGER,
                    sex TEXT,
                    hypertension INTEGER,
                    heart_disease INTEGER,
                    bmi NUMERIC,
                    smoking_status INTEGER,
                    HbА1С NUMERIC,
                    sugar NUMERIC,
                    fullcheck JSONB,
                    brain_image TEXT,
                    brain_result TEXT,
                    xray_image TEXT,
                    xray_result TEXT,
                    first_check_result TEXT,
                    second_check_result TEXT,
                    fullcheck_result TEXT,
                    PRIMARY KEY(key, additional_key)
                    )'''
        )


async def create_doctors_table(conn):
    async with conn.transaction():
        await conn.execute(
            '''CREATE TABLE IF NOT EXISTS doctors(
                    key SERIAL PRIMARY KEY,
                    username TEXT,
                    firstname TEXT,
                    surname TEXT,
                    city TEXT,
                    work_address TEXT,
                    name_organization TEXT,
                    disease TEXT
                    )'''
        )

async def get_doctor_by_disease(name_disease):
    conn = await connect_to_postgres()
    async with conn.transaction():
        cursor = await conn.cursor(f"SELECT COUNT(*) FROM doctors WHERE disease = '{name_disease}'")
        number_lines = await cursor.fetchrow()
        cursor = await conn.cursor(f"SELECT * FROM doctors where disease = '{name_disease}' ")
        ans = await cursor.fetch(number_lines[0])
        number = random.randint(0, number_lines[0] - 1)
        ans = {'username': ans[number]['username'],'surename': ans[number]['surname'],'firstname': ans[number]['firstname']}
        return ans
    

# async def show_table():
#     conn = await connect_to_postgres()
#     async with conn.transaction():
#         cursor = await conn.cursor("SELECT COUNT(*) FROM doctors WHERE disease = 'diabetes'")
#         number_lines = await cursor.fetchrow()
#         cursor = await conn.cursor("SELECT * FROM doctors where disease = 'diabetes' ")
#         ans = await cursor.fetch(number_lines[0])
#         print(ans)


    await conn.close()



async def insert_doctor(data):
    conn = await connect_to_postgres()
    async with conn.transaction():
       for i in data:
            await conn.execute(
                "INSERT INTO doctors (username, firstname, surname, city, work_address, name_organization, disease) VALUES ($1, $2, $3, $4, $5, $6, $7)", 
                 *i
            )


async def insert_data(query, data, user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        await conn.execute(
            query,
            key, additional_key, *data
        )


async def get_data_by_id( query, user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        row = await conn.fetchrow(query, key, additional_key)
        return row
    

async def check_user( user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        row = await conn.fetchrow("SELECT name FROM users WHERE key = $1 and additional_key = $2", key, additional_key)
        if row:
            return True
        else:
            return False
        
async def check_data(query, user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        res = await conn.fetchrow(query, key, additional_key)
        if res[0]:
            return True
        else:
            return False
        
async def delete_user(user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        await conn.execute(
            "DELETE FROM users WHERE key = $1 AND additional_key = $2",
            key, additional_key
        )


async def drop_table(conn):
    """Удаляет таблицу."""
    async with conn.transaction():
        await conn.execute(f"DROP TABLE IF EXISTS users")


async def drop_doctors_table(conn):
    """Удаляет таблицу."""
    async with conn.transaction():
        await conn.execute(f"DROP TABLE IF EXISTS doctors")


async def insert_array(array, user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    json_array = json.dumps({"numbers": array})
    await conn.execute(
            "UPDATE users SET fullcheck = $1 WHERE key = $2 and additional_key = $3",
            json_array,
            key, additional_key
        )


async def get_array(user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        res = await conn.fetchrow("SELECT fullcheck FROM users WHERE key = $1 and additional_key = $2", key, additional_key)
        # print(res[0])
        array = json.loads(res[0])["numbers"]
        # print(array)
        return array
# async def fill_array(user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     async with conn.transaction():
#         data = [0]*986
#         json_data = f'{{"numbers": {data}}}'
#         await conn.execute("UPDATE users SET fullcheck = $1 WHERE key = $2 AND additional_key = $3", json_data, key, additional_key)


# async def insert_data_by_index(index, data, user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     async with conn.transaction():
#         await conn.execute(
#             """
#             UPDATE users 
#             SET fullcheck = jsonb_set(fullcheck, '{numbers, ' || ($1 + 1) || '}', $2, create_missing := true) 
#             WHERE key = $3 and additional_key = $4
#             """,
#             index, data, key, additional_key
#         )

# async def insert_data_by_index(index, data, user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     async with conn.transaction():
#         await conn.execute("UPDATE users SET fullcheck = jsonb_set(fullcheck, '{numbers, 2}', '10', create_missing := true) WHERE key = $1 and additional_key = $2", key, additional_key)


# async def insert_data_by_index(index, data, user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     async with conn.transaction():
#         string = await get_data_by_id("SELECT fullcheck FROM user WHERE key = $1 and additional_key = $2", user_id)
#         string = str(string[0])
#         string[index] = data
#         print(string)
#         await insert_data("UPDATE users SET fullcheck = $1 WHERE key = $2 AND additional_key = $3", string, user_id)
    

# async def fill_string(user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     data = "0"*986
#     async with conn.transaction():
#         await conn.execute(
#             "UPDATE users SET fullcheck = $1 WHERE key = $2 AND additional_key = $3",
#             data, key, additional_key
#         )

# async def get_data_by_index(index, user_id):

# async def insert_data_by_index(index, data, user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     async with conn.transaction():
#         await conn.execute(
#             f"UPDATE users SET fullcheck[{index}] = $1 WHERE key = $2 AND additional_key = $3",
#             data, key, additional_key
#         )


# async def fill_array(user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     async with conn.transaction():
#         await conn.execute("UPDATE users SET fullcheck = ARRAY(SELECT 0 FROM generate_series(1, 986)) WHERE key = $1 AND additional_key = $2",
#             key, additional_key
#         )


# async def get_data_by_index(index, user_id):
#     conn = await connect_to_postgres()
#     key, additional_key = await get_hash(user_id)
#     async with conn.transaction():
#         async with conn.cursor(query=f"SELECT fullcheck[{index + 1}] FROM users WHERE key = $1 AND additional_key = $2") as cur:
#             await cur.execute(key, additional_key)
#             row = await cur.fetchone()
#             if row:
#                 return row[0]  # Возвращаем значение из массива
#             else:
#                 return None  # Возвращаем None, если запись не найдена
        
    