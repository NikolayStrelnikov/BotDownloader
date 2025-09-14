from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
import os
engine = create_async_engine(url=f"sqlite+aiosqlite:///{os.getenv('DATABASE')}")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'USERS'

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    USER_ID: Mapped[int] = mapped_column(BigInteger, nullable=False)  # USER_ID не может быть NULL
    USER_NICK: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    USER_STATUS: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    DATE_EXP_STATUS: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    USER_NAME: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    USER_SURNAME: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    USER_LOCALE: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    DATE_REG: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    DATE_USE: Mapped[str] = mapped_column(String, nullable=True)  # Может быть NULL
    COUNT_USE: Mapped[int] = mapped_column(nullable=True)  # Может быть NULL


class Downloads(Base):
    __tablename__ = 'DOWNLOADS'

    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)
    USER_ID: Mapped[int] = mapped_column(BigInteger, nullable=False)
    URL: Mapped[str] = mapped_column(String, nullable=False)
    FORMAT: Mapped[str] = mapped_column(String, nullable=True)
    FILE_ID: Mapped[str] = mapped_column(String, nullable=False)
    DATE_INS: Mapped[str] = mapped_column(String(32), nullable=True)
    DATE_GET: Mapped[str] = mapped_column(String, nullable=True)
    COUNT_GET: Mapped[int] = mapped_column(nullable=True)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)