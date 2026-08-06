import streamlit as st
import requests

st.set_page_config(
    page_title="SuperKart Sales Forecast",
    page_icon="🛒",
    layout="centered"
)

st.title("🛒 SuperKart Sales Forecasting")

st.write(
    "Enter product and store information to estimate expected sales revenue."
)

product_id = st.text_input(
    "Product ID",
    value="FD6114"
)

product_weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66
)

sugar_content = st.selectbox(
    "Product Sugar Content",
    [
        "Low Sugar",
        "Regular",
        "No Sugar"
    ]
)

allocated_area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    max_value=1.0,
    value=0.027,
    format="%.3f"
)

product_type = st.selectbox(
    "Product Type",
    [
        "Baking Goods",
        "Breads",
        "Breakfast",
        "Canned",
        "Dairy",
        "Frozen Foods",
        "Fruits and Vegetables",
        "Hard Drinks",
        "Health and Hygiene",
        "Household",
        "Meat",
        "Others",
        "Seafood",
        "Snack Foods",
        "Soft Drinks",
        "Starchy Foods"
    ]
)

product_mrp = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08
)

store_id = st.selectbox(
    "Store ID",
    [
        "OUT001",
        "OUT002",
        "OUT003",
        "OUT004"
    ]
)

establishment_year = st.number_input(
    "Store Establishment Year",
    min_value=1900,
    max_value=2100,
    value=2009,
    step=1
)

store_size = st.selectbox(
    "Store Size",
    [
        "Small",
        "Medium",
        "High"
    ]
)

city_type = st.selectbox(
    "Store Location City Type",
    [
        "Tier 1",
        "Tier 2",
        "Tier 3"
    ]
)

store_type = st.selectbox(
    "Store Type",
    [
        "Departmental Store",
        "Supermarket Type1",
        "Supermarket Type2",
        "Food Mart"
    ]
)

BACKEND_URL = "http://backend:7860/predict"

if st.button("Predict Sales", type="primary"):

    if len(product_id) < 2:
        st.error("Please enter a valid Product ID.")

    else:
        product_prefix = product_id[:2].upper()

        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": sugar_content,
            "Product_Allocated_Area": allocated_area,
            "Product_Type": product_type,
            "Product_MRP": product_mrp,
            "Store_Id": store_id,
            "Store_Establishment_Year": establishment_year,
            "Store_Size": store_size,
            "Store_Location_City_Type": city_type,
            "Store_Type": store_type,
            "Product_Id_Prefix": product_prefix
        }

        try:
            response = requests.post(
                BACKEND_URL,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                prediction = result["predicted_sales"]

                st.success(
                    f"Predicted Sales: ${prediction:,.2f}"
                )

            else:
                st.error(
                    "Prediction failed: " + response.text
                )

        except requests.exceptions.RequestException as e:
            st.error(
                f"Unable to connect to prediction API: {e}"
            )