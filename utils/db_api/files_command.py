from utils.db_api.db_jelebot import db
from utils.db_api.schemes.files import Files


async def select_all_files():
    events = await Files.query.gino.all()
    return events


async def count_files():
    count = await db.func.count(Files.id).gino.scalar()
    return count


async def select_file(file_id):
    files = await Files.query.where(Files.id == file_id).gino.first()
    return files


async def add_files(file: str):
    try:
        file = Files(
            path=file,
        )
        return await file.create()
    except Exception as ex:
        print(ex)
        print('Файл не создан')
        return
