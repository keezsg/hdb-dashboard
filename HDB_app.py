import streamlit as st
import pandas as pd
import seaborn as sns
#import matplotlib.pyplot as plt
#import matplotlib.ticker as mtick
import requests


st.title("HDB buying & selling companion")

st.header("Enter parameters for resale price prediction")

st.markdown("\n\n\n\n\n\n\n")

#input parameter
block = st.text_input(
    "Block number, e.g. 309, 612C, etc.",
    value="612C")

#st.write("The selected block is", block)

street_name = st.text_input(
    "Street name, e.g. ANG MO KIO AVE 1, PUNGGOL DR, etc.",
    value="PUNGGOL DR")

#st.write("The selected street name is", street_name)

town = st.text_input(
    "Town, e.g. ANG MO KIO, PUNGGOL, etc",
    value="PUNGGOL")

#st.write("The selected town is", town)

flat_types = ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI-GENERATION"]
flat_type = st.selectbox("Select Flat Type", options=flat_types, index=3)

#st.write("The selected flat type is", flat_type)

level_list = ["Low", "Mid", "High"]
storey_range = st.selectbox(
    "Select Storey Range",
    options=level_list,
    index=0)

#st.write("The selected storey range is", storey_range)

floor_area_sqm = st.number_input(
    "Floor area (square meter), e.g. 67, 93, etc",
    min_value=20,
    max_value=200,
    value=93)

#st.write("The selected floor area is", floor_area_sqm)

remaining_lease_year = st.number_input(
    "Remaining lease (year), e.g. 60, 90, etc.",
    min_value=1,
    max_value=99,
    value=90)

#st.write("The selected remaining lease is", remaining_lease_year)

month_year = st.text_input(
    "Resale date in MM-YYYY format, e.g. 07-2026",
    value="07-2026")

#st.write("The selected month year is", month_year)

params = {
    "block": block,
    "street_name": street_name,
    "town": town,
    "flat_type": flat_type,
    "storey_range": storey_range,
    "floor_area_sqm": floor_area_sqm,
    "remaining_lease_year": remaining_lease_year,
    "month_year": month_year
}


st.markdown("\n\n\n\n\n\n\n")
url = 'https://hdb-proj-938050412638.asia-southeast1.run.app/predict'
if st.button("Get HDB price prediction"):
    respond = requests.get(url, params=params)
    if respond.status_code == 200:
        prediction = respond.json()["price"]
        formatted_price = "${:,.2f}".format(int(round(prediction)))
        st.success(f"Predicted Fare: {formatted_price}")

    else:
        st.error("Failed to retrive prediction from API")

st.markdown("\n\n\n\n\n\n\n")
if st.button("View HDB location"):
    add = f"{block} {street_name}"
    coord_df = pd.read_csv("data/coords_with_walk_metrics.csv")
    coord_df_filtered = coord_df.query("add == @add")

    lat = coord_df_filtered.iloc[0]["latitude"]
    lon = coord_df_filtered.iloc[0]["longitude"]

    lat_lon_data = {
    "lat": lat,
    "lon": lon,
    }

    lat_lon_df = pd.DataFrame(lat_lon_data, index=[0])

    st.map(lat_lon_df, zoom=15, size=25)
