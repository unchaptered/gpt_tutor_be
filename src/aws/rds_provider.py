from mysql.connector import connect, MySQLConnection
from contextlib import contextmanager
from typing import Generator

# Modules
from utilities.config_provider import configProvider

envInstance = configProvider.getConfig()


conf = {
    'host': envInstance['RDS']['HOST'],
    'port': 3306,
    'user': envInstance['RDS']['USER'],
    'password': envInstance['RDS']['PWD'],
    'database': envInstance['RDS']['DB_NAME']
}


class RdsProvider():

    @contextmanager
    def getConnection(self) -> Generator[MySQLConnection, None, None]:
        connection: MySQLConnection = connect(**conf)  # type: ignore

        try:
            yield connection
        except Exception as e:
            raise e
        finally:
            connection.close()
