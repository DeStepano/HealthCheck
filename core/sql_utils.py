import asyncpg
import asyncio
import pytest
import time
import pytest_asyncio
import hashlib
import sqlite3 as sl
from core.config import config
from core.hash import get_hash



async def connect_to_postgres():
    conn = await asyncpg.connect(
        host=config.users_db_host,
        port=config.user_db_port,
        user=config.user_db_user,
        password=config.users_db_password,
        database=config.users_db_database
    )
    return conn


async def create_table(conn):
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

                    brain_image TEXT,
                    brain_result TEXT,
                    xray_image TEXT,
                    xray_result TEXT,
                    first_check_result TEXT,
                    second_check_result TEXT,
                    PRIMARY KEY(key, additional_key)
                    )'''
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


async def insert_data_by_index(index, user_id):
    conn = await connect_to_postgres()
    key, additional_key = await get_hash(user_id)

