import pandas as pd

from app.data_sources.base import DataSource


class CSVDataSource(DataSource):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)