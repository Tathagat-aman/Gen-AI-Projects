import pandas as pd

DATA_PATH = "sales_data.csv"

def get_df():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


# ---------------------------------------------------
# TREND ANALYSIS
# ---------------------------------------------------

def analyze_trend(sku_id=None, store_id=None, category=None, region=None,
                  promo_flag=None, promo_type=None, store_size=None, holiday_flag=None,
                  start_date=None, end_date=None, group_by=None):

    df = get_df()

    if sku_id:
        df = df[df["sku_id"] == sku_id]

    if store_id:
        df = df[df["store_id"] == store_id]

    if category:
        df = df[df["category"] == category]

    if region:
        df = df[df["store_region"] == region]

    if promo_flag is not None:
        df = df[df["promo_flag"] == promo_flag]

    if promo_type:
        df = df[df["promo_type"] == promo_type]

    if store_size:
        df = df[df["store_size"] == store_size]

    if holiday_flag is not None:
        df = df[df["holiday_flag"] == holiday_flag]

    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]

    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]

    # ---------------- GROUP BY MODE ----------------

    if group_by:

        trend = df.groupby(group_by).agg(
            total_units=("units_sold", "sum"),
            total_revenue=("revenue", "sum")
        ).reset_index()

        trend = trend.sort_values("total_units", ascending=False)

        return {
            "group_by": group_by,
            "breakdown": trend.head(20).to_dict("records")
        }

    # ---------------- TIME TREND ----------------

    trend = df.groupby("date").agg(
        total_units=("units_sold", "sum"),
        total_revenue=("revenue", "sum")
    ).reset_index().sort_values("date")

    first_week = trend.head(7)["total_units"].sum()
    last_week = trend.tail(7)["total_units"].sum()

    growth = ((last_week - first_week) / first_week * 100) if first_week > 0 else 0

    return {
        "total_sales": int(trend["total_units"].sum()),
        "avg_daily_sales": float(trend["total_units"].mean()),
        "growth_pct": round(growth, 2)
    }


# ---------------------------------------------------
# ANOMALY DETECTION
# ---------------------------------------------------

def detect_anomalies(sku_id=None, store_id=None, category=None, region=None,
                     promo_flag=None, promo_type=None, store_size=None, holiday_flag=None,
                     start_date=None, end_date=None, threshold=2.0):

    df = get_df()

    if sku_id:
        df = df[df["sku_id"] == sku_id]

    if store_id:
        df = df[df["store_id"] == store_id]

    if category:
        df = df[df["category"] == category]

    if region:
        df = df[df["store_region"] == region]

    if promo_flag is not None:
        df = df[df["promo_flag"] == promo_flag]

    if promo_type:
        df = df[df["promo_type"] == promo_type]

    if store_size:
        df = df[df["store_size"] == store_size]

    if holiday_flag is not None:
        df = df[df["holiday_flag"] == holiday_flag]

    if start_date:
        df = df[df["date"] >= pd.to_datetime(start_date)]

    if end_date:
        df = df[df["date"] <= pd.to_datetime(end_date)]

    daily = df.groupby("date")["units_sold"].sum().reset_index(name="daily_sales")

    mean = daily["daily_sales"].mean()
    std = daily["daily_sales"].std()

    if std == 0:
        daily["z_score"] = 0
    else:
        daily["z_score"] = (daily["daily_sales"] - mean) / std

    daily["is_anomaly"] = abs(daily["z_score"]) > threshold

    anomalies = daily[daily["is_anomaly"]].sort_values("z_score", ascending=False)

    return {
        "mean_sales": float(mean),
        "stddev": float(std),
        "num_anomalies": len(anomalies),
        "anomalies": anomalies.head(10).to_dict("records")
    }


# ---------------------------------------------------
# PROMO SIMULATION
# ---------------------------------------------------

def simulate_promo(category, discount_pct, duration_days=30, region=None, store_size=None):

    df = get_df()

    if category:
        df = df[df["category"] == category]

    if region:
        df = df[df["store_region"] == region]

    if store_size:
        df = df[df["store_size"] == store_size]

    baseline = df[df["promo_flag"] == 0][["units_sold", "revenue"]].mean()
    promo = df[df["promo_flag"] == 1][["units_sold", "revenue"]].mean()

    baseline_units = baseline["units_sold"] if not pd.isna(baseline["units_sold"]) else 0
    baseline_revenue = baseline["revenue"] if not pd.isna(baseline["revenue"]) else 0
    promo_units = promo["units_sold"] if not pd.isna(promo["units_sold"]) else 0

    if baseline_units > 0:
        historical_lift = (promo_units - baseline_units) / baseline_units
    else:
        historical_lift = 0.2

    adjusted_lift = historical_lift * (discount_pct / 20)

    predicted_units = baseline_units * (1 + adjusted_lift) * duration_days
    predicted_revenue = baseline_revenue * (1 + adjusted_lift) * (1 - discount_pct / 100) * duration_days

    baseline_total = baseline_units * duration_days

    return {
        "category": category,
        "discount_pct": discount_pct,
        "duration_days": duration_days,
        "baseline_daily_units": round(baseline_units, 2),
        "predicted_total_units": round(predicted_units, 2),
        "predicted_total_revenue": round(predicted_revenue, 2),
        "units_lift_pct": round((predicted_units - baseline_total) / baseline_total * 100, 2) if baseline_total > 0 else 0,
        "historical_promo_lift_pct": round(historical_lift * 100, 2)
    }