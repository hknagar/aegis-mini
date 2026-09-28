import pandas as pd

from app.data_sources.base import DataSource


class ExcelDataSource(DataSource):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path)