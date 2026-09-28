import pandas as pd

from app.data_sources.base import DataSource
from app.db.database import engine


class PostgreSQLDataSource(DataSource):

    def __init__(self, query: str):
        self.query = query

    def load(self) -> pd.DataFrame:
        with engine.connect() as connection:
            return pd.read_sql(
                self.query,
                connection
            )