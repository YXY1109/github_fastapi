import asyncio
import aiomysql

async def test_example(loop):
    pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
                                      user='root', password='root',
                                      db='tools', loop=loop)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("select * from api_article limit 1;")
            print(cur.description)
            r = await cur.fetchone()
            print(f"r:{r}")
    pool.close()
    await pool.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))
