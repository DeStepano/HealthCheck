import asyncpg
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


async def get_doctor_by_disease(name_disease: str) -> dict:
    conn = await connect_to_postgres()
    async with conn.transaction():
        cursor = await conn.cursor(f"SELECT COUNT(*) FROM doctors WHERE disease = '{name_disease}'")
        number_lines = await cursor.fetchrow()
        cursor = await conn.cursor(f"SELECT * FROM doctors where disease = '{name_disease}' ")
        ans = await cursor.fetch(number_lines[0])
        number = random.randint(0, number_lines[0] - 1)
        ans = {'username': ans[number]['username'],'surename': ans[number]['surname'],'firstname': ans[number]['firstname']}
        return ans


async def insert_data(query: str, data: tuple , user_id: int):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        await conn.execute(
            query,
            key, additional_key, *data
        )


async def get_data_by_id(query: str, user_id: int):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        row = await conn.fetchrow(query, key, additional_key)
        return row
    

async def check_user(user_id: int) -> bool:
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        row = await conn.fetchrow("SELECT name FROM users WHERE key = $1 and additional_key = $2", key, additional_key)
        if row:
            return True
        else:
            return False
        

async def check_data(query: str, user_id: int) -> bool:
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        res = await conn.fetchrow(query, key, additional_key)
        if res[0]:
            return True
        else:
            return False
        

async def delete_user(user_id: int):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        await conn.execute(
            "DELETE FROM users WHERE key = $1 AND additional_key = $2",
            key, additional_key
        )


async def drop_table(conn):
    async with conn.transaction():
        await conn.execute(f"DROP TABLE IF EXISTS users")


async def insert_array(array: list, user_id: int):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    json_array = json.dumps({"numbers": array})
    await conn.execute(
            "UPDATE users SET fullcheck = $1 WHERE key = $2 and additional_key = $3",
            json_array,
            key, additional_key
        )


async def get_array(user_id: int) -> list:
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)
    async with conn.transaction():
        res = await conn.fetchrow("SELECT fullcheck FROM users WHERE key = $1 and additional_key = $2", key, additional_key)
        array = json.loads(res[0])["numbers"]
        return array

        
    
        
    
