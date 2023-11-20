import asyncio

from aiomysql.sa import create_engine


async def go(loop):
    engine = await create_engine(user='root', db='tools', port=3306,
                                 host='127.0.0.1', password='root', loop=loop)
    async with engine.acquire() as conn:
        data = await conn.execute("select * from api_article limit 1;")
        print(data)
        # async for row in conn.execute("select * from api_article limit 1;"):
        #     print(row)

    engine.close()
    await engine.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(go(loop))
