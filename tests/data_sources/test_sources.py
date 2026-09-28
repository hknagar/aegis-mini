from app.data_sources.csv_adapter import CSVDataSource
from app.data_sources.excel_adapter import ExcelDataSource


csv_source = CSVDataSource(
    "data/marketing_campaigns.csv"
)

excel_source = ExcelDataSource(
    "data/monthly_targets.xlsx"
)


csv_df = csv_source.load()
excel_df = excel_source.load()


print("CSV:")
print(csv_df)

print("\nExcel:")
print(excel_df)

# test code below:
# from app.data_sources.csv_adapter import CSVDataSource
# from app.data_sources.excel_adapter import ExcelDataSource
# from app.data_sources.postgres_adapter import PostgreSQLDataSource


# csv_source = CSVDataSource(
#     "data/marketing_campaigns.csv"
# )

# excel_source = ExcelDataSource(
#     "data/monthly_targets.xlsx"
# )

# postgres_source = PostgreSQLDataSource(
#     """
#     SELECT
#         order_id,
#         order_date,
#         customer_id,
#         product_id,
#         quantity,
#         revenue,
#         cost
#     FROM orders;
#     """
# )


# csv_df = csv_source.load()
# excel_df = excel_source.load()
# postgres_df = postgres_source.load()


# print("\n--- CSV ---")
# print(csv_df)

# print("\n--- EXCEL ---")
# print(excel_df)

# print("\n--- POSTGRESQL ---")
# print(postgres_df)