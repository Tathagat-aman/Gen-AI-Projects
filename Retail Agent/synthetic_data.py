import pandas as pd
import numpy as np

def generate_sales_data(rows=100000, file_path="sales_data.csv"):

    np.random.seed(123)

    date_range = pd.date_range('2022-01-01', '2024-12-31')

    stores = list(range(1, 11))
    regions = ['North', 'South', 'East']
    skus = list(range(101, 151))
    categories = ['Beverages', 'Snacks', 'Dairy', 'Household', 'Personal Care']
    promo_types = [None, 'Discount', 'BuyOneGetOne', 'FlashSale']
    store_sizes = ['Small', 'Medium', 'Large']

    data = []

    for _ in range(rows):

        date = np.random.choice(date_range)
        store = np.random.choice(stores)
        region = np.random.choice(regions)
        sku = np.random.choice(skus)
        category = np.random.choice(categories)

        base_price = np.round(np.random.uniform(2, 10), 2)

        promo_flag = np.random.choice([0,1], p=[0.8,0.2])
        promo_type = np.random.choice(promo_types) if promo_flag else None

        price = base_price * (0.8 if promo_flag else 1.0)

        holiday_flag = 1 if pd.Timestamp(date).weekday() in [5,6] else 0

        base_demand = 10

        if promo_flag:
            base_demand *= 2

        if holiday_flag:
            base_demand *= 1.5

        units_sold = np.random.poisson(base_demand)

        revenue = units_sold * price

        inventory_level = np.random.randint(100,1000)

        store_size = np.random.choice(store_sizes)

        data.append([
            date, store, region, sku, category,
            units_sold, revenue, promo_flag, promo_type,
            price, inventory_level, store_size, holiday_flag
        ])

    df = pd.DataFrame(data, columns=[
        'date','store_id','store_region','sku_id','category',
        'units_sold','revenue','promo_flag','promo_type',
        'price','inventory_level','store_size','holiday_flag'
    ])

    df.to_csv(file_path, index=False)

    return df


def load_sales_data(file_path="sales_data.csv"):

    df = pd.read_csv(file_path, parse_dates=['date'])

    return df