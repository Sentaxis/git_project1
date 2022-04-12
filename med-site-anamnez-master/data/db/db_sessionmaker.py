import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as declarative

SqlAlchemyBase = declarative.declarative_base()

__factory = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    db_file = db_file.strip()
    if not db_file:
        raise RuntimeError('Необходимо указать файл базы данных.')

    conn_str = f'sqlite:///{db_file}?check_same_thread=False'
    print(f'Подключение к базе данных по адресу {conn_str}')

    engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> orm.Session:
    global __factory
    return __factory()
