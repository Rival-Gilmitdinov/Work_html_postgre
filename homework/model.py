from sqlalchemy import create_engine, MetaData, select, Column, Integer, String, inspect
import psycopg2
from CONFIG import user,password,host, port, db
from sqlalchemy.orm import declarative_base, relationship, Session
import pandas as pd


engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
Base = declarative_base()


class Data(Base):
    """Этот класс по созданию таблицы с двумя колонками """
    __tablename__ = 'data_of_html'
    id = Column(Integer, primary_key=True)
    text = Column(String)


inspector = inspect(engine)
if not inspector.has_table('data_of_html'):
    Base.metadata.create_all(bind=engine)

def add(text):
    """Функция по добавлению в таблицу постгресса значений"""
    with Session(engine) as session:
        value = Data(text=f'{text}')
        session.add(value)
        session.commit()


def conn(table):
    """Функция по выборке значений из таблицы
    Return: results.fetchall() - список данных из postgresql"""
    metadata = MetaData()
    metadata.reflect(bind=engine, only=[f'{table}'])
    sufps_table = metadata.tables[f'{table}']
    with Session(engine) as session:
        stmt = select(sufps_table)
        results = session.execute(stmt)
    return results.fetchall()


def create_table():
    """Функция по добавлению значений в таблицу html
    Return: преобразованная в html код таблица"""
    df = pd.DataFrame({'text': []})
    for value in conn('data_of_html'):
        df.loc[len(df)] = [value[1]]
    return df.to_html(index=True)


data = Data()


