from app.data_sources.csv_adapter import CSVDataSource
from app.data_sources.excel_adapter import ExcelDataSource
from app.data_sources.postgres_adapter import PostgreSQLDataSource


DATASETS = {
    "orders": {
        "type": "postgres",
        "query": """
            SELECT
                order_id,
                order_date,
                customer_id,
                product_id,
                quantity,
                revenue,
                cost
            FROM orders;
        """
    },

    "marketing_campaigns": {
        "type": "csv",
        "file_path": "data/marketing_campaigns.csv"
    },

    "monthly_targets": {
        "type": "excel",
        "file_path": "data/monthly_targets.xlsx"
    }
}


def get_source(dataset_name: str):

    if dataset_name not in DATASETS:
        raise ValueError(
            f"Unknown dataset: {dataset_name}"
        )

    config = DATASETS[dataset_name]

    if config["type"] == "postgres":
        return PostgreSQLDataSource(
            config["query"]
        )

    if config["type"] == "csv":
        return CSVDataSource(
            config["file_path"]
        )

    if config["type"] == "excel":
        return ExcelDataSource(
            config["file_path"]
        )

    raise ValueError(
        f"Unsupported source type: {config['type']}"
    )

# the previous code below:
# from app.data_sources.csv_adapter import CSVDataSource
# from app.data_sources.excel_adapter import ExcelDataSource
# from app.data_sources.postgres_adapter import PostgreSQLDataSource


# def get_source(source_type: str, **kwargs):
#     if source_type == "csv":
#         return CSVDataSource(kwargs["file_path"])

#     if source_type == "excel":
#         return ExcelDataSource(kwargs["file_path"])

#     if source_type == "postgres":
#         return PostgreSQLDataSource(kwargs["query"])

#     raise ValueError(f"Unsupported data source: {source_type}")