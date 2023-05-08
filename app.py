async def on_startup(dp):
    import filters
    filters.setup(dp)
    import middlewares
    middlewares.setup(dp)
    from loader import db
    from utils.db_api.db_jelebot import on_startup

    await on_startup(dp)
    await db.gino.create_all()
    print('Готово')

    from utils.notify_admin import on_startup_notify
    await on_startup_notify(dp)

    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)
    print('Bot started...')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup)
