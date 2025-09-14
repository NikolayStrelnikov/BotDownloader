from database.models import async_session
from database.models import User, Downloads
from sqlalchemy import select


async def set_user(user_id: int, nick: str, name: str, surname: str, locale: str, date: str) -> None:
    async with async_session() as session:
        async with session.begin():
            stmt = select(User).where(User.USER_ID == user_id)
            user = await session.scalar(stmt)

            if user is None:
                user = User(USER_ID=user_id,
                            USER_NICK=nick,
                            USER_STATUS='free',
                            DATE_EXP_STATUS='2099-12-31 23:59:59',
                            USER_NAME=name,
                            USER_SURNAME=surname,
                            USER_LOCALE=locale,
                            DATE_REG=date,
                            DATE_USE=date,
                            COUNT_USE=1)
                session.add(user)
                await session.commit()


async def set_link(user_id: int, file_url: str, v_format: str, file_id: str, date: str) -> None:
    async with async_session() as session:
        async with session.begin():
            # Ищем существующую запись по file_url
            stmt = select(Downloads).where(Downloads.URL == file_url and Downloads.FORMAT == v_format)
            link = await session.scalar(stmt)

            if link is None:
                # Если записи нет, создаем новую
                link = Downloads(USER_ID=user_id, URL=file_url, FORMAT=v_format, FILE_ID=file_id, DATE=date)
                session.add(link)
            else:
                # Если запись существует, обновляем её поля
                link.USER_ID = user_id
                link.FORMAT = v_format
                link.FILE_ID = file_id
                link.DATE = date
            # Сохраняем изменения в базе данных
            await session.commit()

async def get_file_id(file_url: str) -> str:
    async with async_session() as session:
        async with session.begin():
            # Выполните запрос, чтобы получить объект строки
            stmt = select(Downloads).where(Downloads.URL == file_url)
            result = await session.execute(stmt)
            # Извлеките объект строки
            download = result.scalars().first()
            # Верните File_id из объекта строки, если он существует
            if download:
                return download.FILE_ID
            return ''
