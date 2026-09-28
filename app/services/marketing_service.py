import pandas as pd


def get_marketing_campaigns():
    df = pd.read_csv("data/marketing_campaigns.csv")

    return df.to_dict(orient="records")

def get_channel_performance():
    df = pd.read_csv("data/marketing_campaigns.csv")

    performance = (
        df.groupby("channel")
        .agg({
            "spend": "sum",
            "leads": "sum",
            "conversions": "sum"
        })
        .reset_index()
    )

    performance["conversion_rate"] = (
        performance["conversions"] /
        performance["leads"] * 100
    )

    performance["cost_per_conversion"] = (
        performance["spend"] /
        performance["conversions"]
    )

    return performance.to_dict(orient="records")