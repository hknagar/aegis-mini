from app.data_sources.registry import get_source


class DataAgent:

    def load_dataset(self, dataset_name: str):

        source = get_source(dataset_name)

        return source.load()

    def total_revenue(self):

        df = self.load_dataset("orders")

        return float(df["revenue"].sum())

    def monthly_revenue(self):

        df = self.load_dataset("orders")

        df["order_date"] = df["order_date"].astype(str)

        df["month"] = df["order_date"].str[:7]

        result = (
            df.groupby("month")["revenue"]
            .sum()
            .reset_index()
        )

        return result.to_dict(
            orient="records"
        )

    def monthly_profit(self):

        df = self.load_dataset("orders")

        df["order_date"] = df["order_date"].astype(str)

        df["month"] = df["order_date"].str[:7]

        df["profit"] = (
            df["revenue"] - df["cost"]
        )

        result = (
            df.groupby("month")["profit"]
            .sum()
            .reset_index()
        )

        return result.to_dict(
            orient="records"
        )


# the previous code below:
# from app.data_sources.registry import get_source


# class DataAgent:

#     def load_dataset(self, dataset_name: str):

#         source = get_source(dataset_name)

#         return source.load()