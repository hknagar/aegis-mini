import pandas as pd


def get_monthly_targets():
    df = pd.read_excel("data/monthly_targets.xlsx")

    return df.to_dict(orient="records")