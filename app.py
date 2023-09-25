from PIL import Image
import streamlit as st
import pandas as pd
import pickle
import threading
import time
import sqlite3
model = pickle.load(open("model.sav", "rb"))

# initial data (as a template)
df_1 = pd.read_csv("first_telc.csv")


def main():
    image = Image.open('images/main.png')
    image2 = Image.open('images/logo.png')
    st.image(image, use_column_width=False)
    st.title("Customer Churn Prediction")
    st.sidebar.image(image2)
    data_option = st.sidebar.selectbox(
        "How would you like to predict?",
        ("Online", "Upload CSV"))
    st.sidebar.info('This app is created to predict Customer Churn')
    if data_option == "Online":
        senior_citizen = st.number_input(
            "SeniorCitizen", min_value=0, max_value=1, value=0)
        monthly_charges = st.number_input("MonthlyCharges")
        total_charges = st.number_input("TotalCharges")
        gender = st.selectbox("Gender", ["Male", "Female"])
        partner = st.selectbox("Partner", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["Yes", "No"])
        phone_service = st.selectbox("PhoneService", ["Yes", "No"])
        multiple_lines = st.selectbox("MultipleLines", ["Yes", "No"])
        internet_service = st.selectbox(
            "InternetService", ["DSL", "Fiber optic", "No"])
        online_security = st.selectbox(
            "OnlineSecurity", ["Yes", "No", "No internet service"])
        online_backup = st.selectbox(
            "OnlineBackup", ["Yes", "No", "No internet service"])
        protection = st.selectbox(
            "DeviceProtection", ["Yes", "No", "No internet service"])
        tech_support = st.selectbox(
            "TechSupport", ["Yes", "No", "No internet service"])
        streaming_tv = st.selectbox(
            "StreamingTV", ["Yes", "No", "No internet service"])
        streaming_movies = st.selectbox(
            "StreamingMovies", ["Yes", "No", "No internet service"])
        contract = st.selectbox(
            "Contract", ["Month-to-month", "One year", "Two year"])
        paperless = st.selectbox("PaperlessBilling", ["Yes", "No"])
        payment_method = st.selectbox(
            "PaymentMethod",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)",
            ],
        )
        tenure = st.number_input("Tenure")

        if st.button("Predict"):
            # input data for prediction
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

            df_2 = pd.concat([df_1, new_df], ignore_index=True)

            # Group the tenure in bins of 12 months
            labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
            df_2["tenure_group"] = pd.cut(
                df_2.tenure.astype(int), range(1, 80, 12), right=False, labels=labels
            )

            # Drop column customerID (already dropped before) and tenure
            df_2.drop(columns=["tenure"], axis=1, inplace=True)

            # Create another dataframe of just monthly and total charges : add to final_df

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

            # Concatenate new_dummy and new_df__dummies
            final_df = pd.concat([new_dummy, new_df__dummies], axis=1)

            # make sure monthly charges and all other one hot encoded categories : are in the correct order (see training data set x_train)
            # how to upload csv? (after uploading -> do one hot encoding again on it (categorical columns only))

            final_df = final_df[
                ['SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender_Female', 'gender_Male', 'Partner_No',
                 'Partner_Yes', 'Dependents_No', 'Dependents_Yes', 'PhoneService_No', 'PhoneService_Yes', 'MultipleLines_No',
                 'MultipleLines_No phone service', 'MultipleLines_Yes', 'InternetService_DSL', 'InternetService_Fiber optic', 'InternetService_No',
                 'OnlineSecurity_No', 'OnlineSecurity_No internet service', 'OnlineSecurity_Yes', 'OnlineBackup_No', 'OnlineBackup_No internet service',
                 'OnlineBackup_Yes', 'DeviceProtection_No', 'DeviceProtection_No internet service', 'DeviceProtection_Yes', 'TechSupport_No',
                 'TechSupport_No internet service', 'TechSupport_Yes', 'StreamingTV_No', 'StreamingTV_No internet service', 'StreamingTV_Yes',
                 'StreamingMovies_No', 'StreamingMovies_No internet service', 'StreamingMovies_Yes', 'Contract_Month-to-month', 'Contract_One year',
                 'Contract_Two year', 'PaperlessBilling_No', 'PaperlessBilling_Yes', 'PaymentMethod_Bank transfer (automatic)', 'PaymentMethod_Credit card (automatic)',
                 'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check', 'tenure_group_1 - 12', 'tenure_group_13 - 24', 'tenure_group_25 - 36',
                 'tenure_group_37 - 48', 'tenure_group_49 - 60', 'tenure_group_61 - 72',
                 ]
            ]  # should consists gender'Dependents_No''female etc...

            # Predict churn on final_df

            single = model.predict(final_df.tail(1))
            probability = model.predict_proba(final_df.tail(1))[:, 1]

            if single == 1:
                st.write("This customer will churn!")
                st.write(f"Confidence: {probability*100}%")
            else:
                st.write("No churn")
                st.write(f"Confidence: {probability*100}%")

    elif data_option == "Upload CSV":

        file_upload = st.file_uploader(
            "Upload csv file for predictions", type=["csv"])
        st.write("Uploading...")
        
        if file_upload is not None:
            data = pd.read_csv(file_upload)
            data = pd.concat([df_1, data], ignore_index=True)
            # Group the tenure in bins of 12 months
            labels = ["{0} - {1}".format(i, i + 11) for i in range(1, 72, 12)]
            data["tenure_group"] = pd.cut(
                data.tenure.astype(int), range(1, 80, 12), right=False, labels=labels
            )

            # Drop column customerID (already dropped before) and tenure
            data.drop(columns=["tenure"], axis=1, inplace=True)

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

            numerical_data = data[["MonthlyCharges", "TotalCharges"]]
            final_df_csv = pd.concat([data_encoded, numerical_data], axis=1)

            final_df_csv = final_df_csv[
                ['SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender_Female', 'gender_Male', 'Partner_No',
                 'Partner_Yes', 'Dependents_No', 'Dependents_Yes', 'PhoneService_No', 'PhoneService_Yes', 'MultipleLines_No',
                 'MultipleLines_No phone service', 'MultipleLines_Yes', 'InternetService_DSL', 'InternetService_Fiber optic', 'InternetService_No',
                 'OnlineSecurity_No', 'OnlineSecurity_No internet service', 'OnlineSecurity_Yes', 'OnlineBackup_No', 'OnlineBackup_No internet service',
                 'OnlineBackup_Yes', 'DeviceProtection_No', 'DeviceProtection_No internet service', 'DeviceProtection_Yes', 'TechSupport_No',
                 'TechSupport_No internet service', 'TechSupport_Yes', 'StreamingTV_No', 'StreamingTV_No internet service', 'StreamingTV_Yes',
                 'StreamingMovies_No', 'StreamingMovies_No internet service', 'StreamingMovies_Yes', 'Contract_Month-to-month', 'Contract_One year',
                 'Contract_Two year', 'PaperlessBilling_No', 'PaperlessBilling_Yes', 'PaymentMethod_Bank transfer (automatic)', 'PaymentMethod_Credit card (automatic)',
                 'PaymentMethod_Electronic check', 'PaymentMethod_Mailed check', 'tenure_group_1 - 12', 'tenure_group_13 - 24', 'tenure_group_25 - 36',
                 'tenure_group_37 - 48', 'tenure_group_49 - 60', 'tenure_group_61 - 72',
                 ]
            ]

            # Perform one hot encoding again (Convert all 19 values to 50/51 columns.)
            single = model.predict(final_df_csv.tail(1))
            probability = model.predict_proba(final_df_csv.tail(1))[:, 1]
            # st.write(single)
            if single == 1:
                st.write("This customer is likely to churn!!")
                st.write(f"Confidence: {probability*100}%")
            else:
                st.write("This customer is likely to continue!!")
                st.write(f"Confidence: {probability*100}%")


if __name__ == "__main__":
    main()



# def create_or_connect_db():
#     conn = sqlite3.connect("uploaded_data.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS uploaded_csv (
#             id INTEGER PRIMARY KEY,
#             filename TEXT,
#             processing_time REAL
#         )
#     ''')
#     conn.commit()
#     return conn

# def insert_into_db(conn, filename, processing_time):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO uploaded_csv (filename, processing_time) VALUES (?, ?)", (filename, processing_time))
#     conn.commit()

# def process_csv(file):
#     time.sleep(5)
#     df = pd.read_csv(file)
#     return df

# def main():
#     st.title("CSV File Upload with Processing Time and SQLite Database")

#     uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

#     if uploaded_file is not None:
#         st.write("Uploading...")

#         def process_file():
#             start_time = time.time()
#             df = process_csv(uploaded_file)
#             end_time = time.time()
#             processing_time = end_time - start_time

#             st.success(f"File uploaded and processed in {processing_time:.2f} seconds!")
#             st.dataframe(df)
#             conn = create_or_connect_db()
#             insert_into_db(conn, uploaded_file.name, processing_time)

#         thread = threading.Thread(target=process_file)
#         thread.start()
