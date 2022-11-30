import pandas as pd
from helium_api_wrapper.helpers import (
    load_hotspot,
)

h = pd.read_pickle("../../data/hotspots.pkl")
c = pd.read_pickle("../../data/challenges_with_location.pkl")
missings = []

print(len(c[c["challengee_lat"] == 0]))
print(len(h))

""" iterate over challenges and check if hotspot is in hotspots """
for i, row in c.iterrows():
    if (
        row["challengee_lat"] != 0
        and row["witness_lat"] != 0
        and row["challengee_lng"] != 0
        and row["witness_lng"] != 0
    ):
        continue

    if row["challengee"] not in h["address"].values:
        try:
            h.loc[len(h)] = load_hotspot(row["challengee"])
        except Exception:
            missings.append(row["challengee"])
            pass

    lat = h[h["address"] == row["challengee"]]["lat"].values[0]
    lng = h[h["address"] == row["challengee"]]["lng"].values[0]
    c.at[i, "challengee_lat"] = lat
    c.at[i, "challengee_lng"] = lng

    if row["witness"] not in h["address"].values:
        try:
            h.loc[len(h)] = load_hotspot(row["witness"])
        except Exception:
            missings.append(row["witness"])
            pass

    lat = h[h["address"] == row["witness"]]["lat"].values[0]
    lng = h[h["address"] == row["witness"]]["lng"].values[0]
    c.at[i, "witness_lat"] = lat
    c.at[i, "witness_lng"] = lng

    # print(len(missings))
    pd.to_pickle(c, "../../data/challenges_with_location.pkl")
    pd.to_pickle(h, "../../data/hotspots.pkl")
    pd.to_pickle(missings, "../../data/missings.pkl")
