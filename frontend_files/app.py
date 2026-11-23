import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(
    page_title="SuperKart Sales Forecasting Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 SuperKart Sales Forecasting Service")
st.markdown('''
Welcome to the SuperKart Sales Forecasting system! This interface connects directly with our containerized machine learning microservice to deliver real-time and batch predictions.
''')

# Define backend API endpoints (using docker network alias inside codespaces/containers)
BACKEND_BASE_URL = "http://backend:7860"

tab1, tab2 = st.tabs(["🔮 Real-Time Single Prediction", "📁 Batch CSV Upload"])

with tab1:
    st.header("Single Product Prediction")
    st.write("Fill in the product and store attributes below to estimate total sales.")

    col1, col2 = st.columns(2)

    with col1:
        product_weight = st.number_input("Product Weight (kg)", min_value=0.0, max_value=50.0, value=12.5, step=0.1)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        allocated_area = st.number_input("Product Display Allocated Area Ratio", min_value=0.0, max_value=1.0, value=0.05, format="%.4f")
        product_mrp = st.number_input("Maximum Retail Price (MRP)", min_value=0.0, value=120.0, step=0.5)
        product_char = st.selectbox("Product Broad Type (Prefix)", ["FD", "DR", "NC"])

    with col2:
        store_size = st.selectbox("Store Size", ["Small", "Medium", "High"])
        city_type = st.selectbox("City Location Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Outlet Type", ["Supermarket Type1", "Supermarket Type2", "Supermarket Type3", "Departmental Store", "Food Mart"])
        store_age = st.number_input("Store Age (Years)", min_value=0, max_value=100, value=15, step=1)
        product_category = st.selectbox("Product Shelf Life Category", ["Perishables", "Non Perishables"])

    # Convert clean categorical names to values matching encoded training columns
    product_char_clean = product_char.split(" ")[0]

    payload = {
        "Product_Weight": product_weight,
        "Product_Sugar_Content": product_sugar,
        "Product_Allocated_Area": allocated_area,
        "Product_MRP": product_mrp,
        "Store_Size": store_size,
        "Store_Location_City_Type": city_type,
        "Store_Type": store_type,
        "Product_Id_char": product_char_clean,
        "Store_Age_Years": int(store_age),
        "Product_Type_Category": product_category
    }

    if st.button("Predict Total Sales", type="primary"):
        try:
            with st.spinner("Communicating with prediction backend..."):
                response = requests.post(f"{BACKEND_BASE_URL}/v1/predict", json=payload)

            if response.status_code == 200:
                result = response.json()
                predicted_sales = result.get("prediction", 0.0)
                st.success(f"### Estimated Outlet Sales Revenue: ${predicted_sales:,.2f}")
            else:
                st.error(f"Backend returned error ({response.status_code}): {response.text}")
        except Exception as e:
            st.error(f"Unable to establish connection with the backend microservice: {e}")

with tab2:
    st.header("Batch Sales Prediction")
    st.write("Upload a standard CSV format dataset to generate bulk sales estimates instantly.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        df_preview = pd.read_csv(uploaded_file)
        st.write("**Uploaded Dataset Preview:**")
        st.dataframe(df_preview.head(5))

        # Reset buffer pointer for uploading to API
        uploaded_file.seek(0)

        if st.button("Run Batch Predictions", type="primary"):
            try:
                files = {'file': (uploaded_file.name, uploaded_file.getvalue(), 'text/csv')}
                with st.spinner("Processing bulk file on the predictive server..."):
                    response = requests.post(f"{BACKEND_BASE_URL}/v1/predictbatch", files=files)

                if response.status_code == 200:
                    predictions_dict = response.json()
                    # Convert dictionary predictions to series and join
                    preds_series = pd.Series({int(k): v for k, v in predictions_dict.items()})
                    df_preview["Predicted_Store_Sales_Total"] = preds_series

                    st.success("Batch predictions completed successfully!")
                    st.dataframe(df_preview)

                    # Enable CSV download
                    output_csv = df_preview.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Predicted Sales Dataset",
                        data=output_csv,
                        file_name="SuperKart_Sales_Predictions.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"Batch API failed: {response.text}")
            except Exception as e:
                st.error(f"Failed to route requests to backend service: {e}")
