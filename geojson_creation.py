import geojson
import os
import pandas as pd


def wrangle_data():
    pop_df = pd.read_csv("faroe-population.csv")
    pop_df = (
        pop_df.pipe(
            lambda x: x.assign(
                Population=pd.to_numeric(x["Population"], errors="coerce")
            )
        )
        .dropna()
        .pipe(lambda x: x.assign(Population=x["Population"].astype(int)))
        .rename(columns={"Place": "PlaceName"})
    )
    coord_df = pd.read_csv("overpass-faroes.csv")
    faroe_df = pd.concat(
        [coord_df, coord_df.iloc[:, 0].str.split("\t", expand=True)], axis=1
    )
    faroe_df = faroe_df.rename(
        columns={0: "_", 1: "Latitude", 2: "Longitude", 3: "PlaceName", 4: "PlaceType"}
    )
    faroe_df = faroe_df.drop(faroe_df.columns[[0, 1]], axis=1)
    faroe_df.PlaceName = faroe_df.PlaceName.astype(str)
    faroe_df = pd.merge(faroe_df, pop_df, on="PlaceName", how="outer")

    def manual_data_insert(placename, lati, longi, placetype):
        faroe_df.loc[faroe_df["PlaceName"] == placename, "Latitude"] = lati
        faroe_df.loc[faroe_df["PlaceName"] == placename, "Longitude"] = longi
        faroe_df.loc[faroe_df["PlaceName"] == placename, "PlaceType"] = placetype

    PlaceList = faroe_df[faroe_df["Latitude"].isna()]["PlaceName"].tolist()
    LatLongDict = {
        "62": "-7",
        "62.2451801": "-6.6678361",
        "62.1753702": "-6.7752761",
        "62.1939598": "-6.8540808",
        "62.0811545": "-6.7294839",
        "62.0187017": "-6.9123819",
        "61.7706823": "-6.8066251",
        "61.6849993": "-6.7558718",
        "61.5509988": "-6.8308499",
    }
    TypeList = ["country"] + ["village"] * 8
    zipped_list = zip(
        PlaceList, list(LatLongDict.keys()), list(LatLongDict.values()), TypeList
    )
    for placename, lati, longi, placetype in zipped_list:
        manual_data_insert(placename, lati, longi, placetype)
    faroe_df["Latitude"] = pd.to_numeric(faroe_df["Latitude"])
    faroe_df["Longitude"] = pd.to_numeric(faroe_df["Longitude"])
    faroe_df = faroe_df.dropna(subset=["Population"])
    return faroe_df


def to_geojson(df):
    features = []
    for _, row in df.iterrows():
        point = geojson.Point((row["Longitude"], row["Latitude"]))
        properties = {"PlaceName": row["PlaceName"], "Population": row["Population"]}
        features.append(geojson.Feature(geometry=point, properties=properties))
    with open("faroe_df.geojson", "w") as f:
        geojson.dump(geojson.FeatureCollection(features), f)


if __name__ == "__main__":
    faroe_df = wrangle_data()
    faroe_df.to_csv("faroe_df.csv")
    to_geojson(faroe_df)
