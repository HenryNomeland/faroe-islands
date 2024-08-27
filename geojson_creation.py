import geojson
import os
import pandas as pd


def join_data():
    df = pd.read_csv("faroe-population.csv")
    return df


if __name__ == "__main__":
    join_data()
