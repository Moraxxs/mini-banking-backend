import asyncio


async def get_profile (id: int):
    await asyncio.sleep (2)
    return "Профиль загружен"

async def get_transaction (id: int):
    await asyncio.sleep(3)
    return "Транзакции загружены"


async def main():
    results = await asyncio.gather(
        get_profile (1),
        get_transaction (2)
    )

    print(results)


asyncio.run(main())
