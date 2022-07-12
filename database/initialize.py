from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url="sqlite://database/database.sqlite3",
        modules={"models": ["database.models"]},
    )
    await Tortoise.generate_schemas()
