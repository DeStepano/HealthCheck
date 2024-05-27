import asyncpg
import asyncio
import pytest
import time
import pytest_asyncio
from core.sql_utils import connect_to_postgres, insert_data, create_table, get_data_by_id

@pytest.mark.asyncio
async def test_stress(benchmark):
    async def run():
        async with connect_to_postgres() as conn:
            tasks = [
                (
                asyncio.create_task(insert_data(conn, "INSERT INTO users (key, additional_key, name, age) VALUES ($1, $2, $3, $4)",  {'name': f'User {i}', 'age': i}, i)),
                asyncio.create_task(get_data_by_id(conn, "SELECT * FROM users WHERE key = $1 and additional_key = $2",  i))
                )
                for i in range(100)
            ]
            await asyncio.gather(*tasks)

    benchmark(run)


# @pytest.mark.asyncio
# async def test_unit():
#     async with connect_to_postgres() as conn:
#         tasks = [
#             (
#             asyncio.create_task(insert_data(conn, "INSERT INTO users (key, additional_key, name, age) VALUES ($1, $2, $3, $4)",  {'name': f'User {i}', 'age': i}, i)),
#             asyncio.create_task(insert_data(conn, "INSERT INTO users (key, additional_key, name, age) VALUES ($1, $2, $3, $4)",  {'name': f'User {100-i}', 'age':100-i}, 100-i))
#             )
#             for i in range(0,50)
#             ]
#         await asyncio.gather(*tasks)