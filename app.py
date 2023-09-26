# Importing Libraries
from PIL import Image
import streamlit as st
import pandas as pd
import pickle
import threading
import time
import sqlite3

# Loading Model + UI + Initial Data (Template) + Database
model = pickle.load(open("model.sav", "rb"))
st.set_page_config(page_title="Churn Predictor", page_icon="📊")
df_1 = pd.read_csv("first_telc.csv")

conn = sqlite3.connect("churn_database.db")
cursor = conn.cursor()

# Create a table to store records
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS customer_records (
        id INTEGER PRIMARY KEY,
        SeniorCitizen INTEGER,
        MonthlyCharges REAL,
        TotalCharges REAL,
        gender TEXT,
        Partner TEXT,
        Dependents TEXT,
        PhoneService TEXT,
        MultipleLines TEXT,
        InternetService TEXT,
        OnlineSecurity TEXT,
        OnlineBackup TEXT,
        DeviceProtection TEXT,
        TechSupport TEXT,
        StreamingTV TEXT,
        StreamingMovies TEXT,
        Contract TEXT,
        PaperlessBilling TEXT,
        PaymentMethod TEXT,
        tenure INTEGER
    )
"""
)
conn.commit()


# Column Order (Reorder as per model)
def get_column_order():
    column_order = [
        "SeniorCitizen",
        "MonthlyCharges",
        "TotalCharges",
        "gender_Female",
        "gender_Male",
        "Partner_No",
        "Partner_Yes",
        "Dependents_No",
        "Dependents_Yes",
        "PhoneService_No",
        "PhoneService_Yes",
        "MultipleLines_No",
        "MultipleLines_No phone service",
        "MultipleLines_Yes",
        "InternetService_DSL",
        "InternetService_Fiber optic",
        "InternetService_No",
        "OnlineSecurity_No",
        "OnlineSecurity_No internet service",
        "OnlineSecurity_Yes",
        "OnlineBackup_No",
        "OnlineBackup_No internet service",
        "OnlineBackup_Yes",
        "DeviceProtection_No",
        "DeviceProtection_No internet service",
        "DeviceProtection_Yes",
        "TechSupport_No",
        "TechSupport_No internet service",
        "TechSupport_Yes",
        "StreamingTV_No",
        "StreamingTV_No internet service",
        "StreamingTV_Yes",
        "StreamingMovies_No",
        "StreamingMovies_No internet service",
        "StreamingMovies_Yes",
        "Contract_Month-to-month",
        "Contract_One year",
        "Contract_Two year",
        "PaperlessBilling_No",
        "PaperlessBilling_Yes",
        "PaymentMethod_Bank transfer (automatic)",
        "PaymentMethod_Credit card (automatic)",
        "PaymentMethod_Electronic check",
        "PaymentMethod_Mailed check",
        "tenure_group_1 - 12",
        "tenure_group_13 - 24",
        "tenure_group_25 - 36",
        "tenure_group_37 - 48",
        "tenure_group_49 - 60",
        "tenure_group_61 - 72",
    ]
    return column_order


# Process CSV File
def process_csv(file_upload):
    with st.spinner("Processing CSV..."):
        # Check if the uploaded file is empty
        if file_upload is None or file_upload.size == 0:
            st.error("Error: The uploaded CSV file is empty.")
            return

        time.sleep(2)  # Simulate CSVhj
        start_time = time.time()
        data = pd.read_csv(file_upload)
        data = pd.concat([df_1, data], ignore_index=True)

        # Insert records from the CSV into the database
        for index, row in data.iterrows():
            cursor.execute(
                """
                INSERT INTO customer_records (
                    SeniorCitizen, MonthlyCharges, TotalCharges, gender, Partner, Dependents,
                    PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup,
                    DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract,
                    PaperlessBilling, PaymentMethod, tenure
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    row["SeniorCitizen"],
                    row["MonthlyCharges"],
                    row["TotalCharges"],
                    row["gender"],
                    row["Partner"],
                    row["Dependents"],
                    row["PhoneService"],
                    row["MultipleLines"],
                    row["InternetService"],
                    row["OnlineSecurity"],
                    row["OnlineBackup"],
                    row["DeviceProtection"],
                    row["TechSupport"],
                    row["StreamingTV"],
                    row["StreamingMovies"],
                    row["Contract"],
                    row["PaperlessBilling"],
                    row["PaymentMethod"],
                    row["tenure"],
                ),
            )
        conn.commit()
        end_time = time.time()
        processing_time = round(end_time - start_time, 2)
        st.success(f"CSV file processed in {processing_time} seconds")

        # Group the tenure in bins of 12 months
        labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
        data["tenure_group"] = pd.cut(
            data.tenure.astype(int), range(1, 80, 12), right=False, labels=labels
        )

        # Drop column customerID (already dropped before) and tenure
        data.drop(columns=["tenure"], axis=1, inplace=True)

        # One Hot Encoding (Categorical (17) to Numerical (50 columns))
        data_encoded = pd.get_dummies(
            data[
                [
                    "gender",
                    "SeniorCitizen",
                    "Partner",
                    "Dependents",
                    "PhoneService",
                    "MultipleLines",
                    "InternetService",
                    "OnlineSecurity",
                    "OnlineBackup",
                    "DeviceProtection",
                    "TechSupport",
                    "StreamingTV",
                    "StreamingMovies",
                    "Contract",
                    "PaperlessBilling",
                    "PaymentMethod",
                    "tenure_group",
                ]
            ]
        )

        # Combining One Hot Categorical + Numerical into final_df_csv

        numerical_data = data[["MonthlyCharges", "TotalCharges"]]
        final_df_csv = pd.concat([data_encoded, numerical_data], axis=1)

        final_df_csv = final_df_csv.reindex(columns=get_column_order())

        single = model.predict(final_df_csv.tail(1))
        probability = model.predict_proba(final_df_csv.tail(1))[:, 1]
        if single == 1:
            st.success("Prediction : This customer will churn")
        else:
            st.success("Prediction : This customer will continue")
        probability_value = probability[0]
        st.write("Confidence: {:.2f}%".format(probability_value * 100))

        return data  # Return DataFrame


# Main
def main():
    image = Image.open("images/main.png")
    image2 = Image.open("images/logo.png")
    st.title("Customer Churn Prediction")
    st.sidebar.image(image2, use_column_width=True)

    # Container for the main content
    main_container = st.container()
    main_container.image(image, use_column_width=True)
    st.sidebar.title("Navigation")

    # Input
    data_option = st.sidebar.selectbox(
        "How would you like to predict?", ("Online", "Upload CSV")
    )
    st.sidebar.info("This app is created to predict Customer Churn")
    if data_option == "Online":
        st.header("Enter Customer Information")

        senior_citizen = st.number_input(
            "Senior Citizen",
            min_value=0,
            max_value=1,
            value=0,
            help="Enter 1 if the customer is a senior citizen, otherwise enter 0.",
        )
        monthly_charges = st.number_input("Monthly Charges")
        total_charges = st.number_input("Total Charges")
        gender = st.selectbox("Gender", ["Male", "Female"])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No"])
        internet_service = st.selectbox(
            "Internet Service", ["DSL", "Fiber optic", "No"]
        )
        online_security = st.selectbox(
            "Online Security", ["Yes", "No", "No internet service"]
        )
        online_backup = st.selectbox(
            "Online Backup", ["Yes", "No", "No internet service"]
        )
        protection = st.selectbox(
            "Device Protection", ["Yes", "No", "No internet service"]
        )
        tech_support = st.selectbox(
            "Tech Support", ["Yes", "No", "No internet service"]
        )
        streaming_tv = st.selectbox(
            "Streaming TV", ["Yes", "No", "No internet service"]
        )
        streaming_movies = st.selectbox(
            "Streaming Movies", ["Yes", "No", "No internet service"]
        )
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("Paperless Billing", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )
        tenure = st.number_input(
            "Tenure",
            help="Duration for which a customer has been using the service provided by the company.",
        )

        if st.button("Predict"):
            # Input data for prediction
            data = [
                [
                    senior_citizen,
                    monthly_charges,
                    total_charges,
                    gender,
                    partner,
                    dependents,
                    phone_service,
                    multiple_lines,
                    internet_service,
                    online_security,
                    online_backup,
                    protection,
                    tech_support,
                    streaming_tv,
                    streaming_movies,
                    contract,
                    paperless,
                    payment_method,
                    tenure,
                ]
            ]

            new_df = pd.DataFrame(
                data,
                columns=[
                    "SeniorCitizen",
                    "MonthlyCharges",
                    "TotalCharges",
                    "gender",
                    "Partner",
                    "Dependents",
                    "PhoneService",
                    "MultipleLines",
                    "InternetService",
                    "OnlineSecurity",
                    "OnlineBackup",
                    "DeviceProtection",
                    "TechSupport",
                    "StreamingTV",
                    "StreamingMovies",
                    "Contract",
                    "PaperlessBilling",
                    "PaymentMethod",
                    "tenure",
                ],
            )

            # Insert the new record into the database
            cursor.execute(
                """
                INSERT INTO customer_records (
                    SeniorCitizen, MonthlyCharges, TotalCharges, gender, Partner, Dependents,
                    PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup,
                    DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract,
                    PaperlessBilling, PaymentMethod, tenure
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                tuple(new_df.iloc[0]),
            )
            conn.commit()

            st.success("Record added successfully!")

            df_2 = pd.concat([df_1, new_df], ignore_index=True)

            # Group the tenure in bins of 12 months
            labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
            df_2["tenure_group"] = pd.cut(
                df_2.tenure.astype(int), range(1, 80, 12), right=False, labels=labels
            )

            # Drop column customerID (already dropped before) and tenure
            df_2.drop(columns=["tenure"], axis=1, inplace=True)

            # Combining One Hot Encoded Data with Numerical data into final_df

            # Performing one-hot encoding on all categorical data : convert from 17 (not 19 [monthly, total charges]) to 50 columns
            new_df__dummies = pd.get_dummies(
                df_2[
                    [
                        "gender",
                        "SeniorCitizen",
                        "Partner",
                        "Dependents",
                        "PhoneService",
                        "MultipleLines",
                        "InternetService",
                        "OnlineSecurity",
                        "OnlineBackup",
                        "DeviceProtection",
                        "TechSupport",
                        "StreamingTV",
                        "StreamingMovies",
                        "Contract",
                        "PaperlessBilling",
                        "PaymentMethod",
                        "tenure_group",
                    ]
                ]
            )

            # Create another dataframe of just MonthlyCharges and TotalCharges
            new_dummy = df_2[["MonthlyCharges", "TotalCharges"]]

            final_df = pd.concat([new_dummy, new_df__dummies], axis=1)
            final_df = final_df.reindex(columns=get_column_order())

            single = model.predict(final_df.tail(1))
            probability = model.predict_proba(final_df.tail(1))[:, 1]

            if single == 1:
                st.success("Prediction : This customer will churn")
            else:
                st.success("Prediction : This customer will continue")

            probability_value = probability[0]
            st.write("Confidence: {:.2f}%".format(probability_value * 100))

    elif data_option == "Upload CSV":
        # Instructions
        st.sidebar.markdown("## Upload a CSV file for predictions")
        st.sidebar.info(
            "Please upload a CSV file containing the following columns in the specified order:\n"
            "1. SeniorCitizen (0 or 1)\n"
            "2. MonthlyCharges (numeric)\n"
            "3. TotalCharges (numeric)\n"
            "4. gender (Male or Female)\n"
            "5. Partner (Yes or No)\n"
            "6. Dependents (Yes or No)\n"
            "7. PhoneService (Yes or No)\n"
            "8. MultipleLines (Yes, No, or No phone service)\n"
            "9. InternetService (DSL, Fiber optic, or No)\n"
            "10. OnlineSecurity (Yes, No, or No internet service)\n"
            "11. OnlineBackup (Yes, No, or No internet service)\n"
            "12. DeviceProtection (Yes, No, or No internet service)\n"
            "13. TechSupport (Yes, No, or No internet service)\n"
            "14. StreamingTV (Yes, No, or No internet service)\n"
            "15. StreamingMovies (Yes, No, or No internet service)\n"
            "16. Contract (Month-to-month, One year, or Two year)\n"
            "17. PaperlessBilling (Yes or No)\n"
            "18. PaymentMethod (Electronic check, Mailed check, Bank transfer (automatic), or Credit card (automatic))\n"
            "19. tenure (numeric)"
        )
        file_upload = st.file_uploader("Upload csv file for predictions", type=["csv"])
        if file_upload is not None:
            if st.button("Process CSV"):
                uploaded_data = process_csv(file_upload)

        # Display previously entered records
        st.subheader("Customer Records")
        records = cursor.execute("SELECT * FROM customer_records").fetchall()
        if records:
            df_records = pd.DataFrame(
                records, columns=[desc[0] for desc in cursor.description]
            )
            st.write(df_records)
        else:
            st.info("No records found in the database.")


if __name__ == "__main__":
    main()
