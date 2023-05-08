from utils.db_api.schemes.event_files import EventsFiles


async def select_event_files(event_id):
    files = await EventsFiles.query.where(
        EventsFiles.events_id == event_id,
    ).gino.all()
    return files


async def add_events_files(files_id: int, events_id: int):
    try:
        request = EventsFiles(
            events_id=events_id,
            files_id=files_id,
        )

        await request.create()
    except Exception as ex:
        print('Файл для мероприятие не создан')
        print(ex)
        return
