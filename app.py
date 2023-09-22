import streamlit as st
import pandas as pd
import pickle

model = pickle.load(open("model.sav", "rb"))

# initial data (as a template)
df_1 = pd.read_csv("first_telc.csv")

st.title("Customer Churn Prediction")
senior_citizen = st.number_input("SeniorCitizen")
monthly_charges = st.number_input("MonthlyCharges")
total_charges = st.number_input("TotalCharges")
gender = st.selectbox("Gender", ["Male", "Female"])
partner = st.selectbox("Partner", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["Yes", "No"])
phone_service = st.selectbox("PhoneService", ["Yes", "No"])
multiple_lines = st.selectbox("MultipleLines", ["Yes", "No"])
internet_service = st.selectbox("InternetService", ["DSL", "Fiber optic", "No"])
online_security = st.selectbox("OnlineSecurity", ["Yes", "No", "No internet service"])
online_backup = st.selectbox("OnlineBackup", ["Yes", "No", "No internet service"])
protection = st.selectbox("DeviceProtection", ["Yes", "No", "No internet service"])
tech_support = st.selectbox("TechSupport", ["Yes", "No", "No internet service"])
streaming_tv = st.selectbox("StreamingTV", ["Yes", "No", "No internet service"])
streaming_movies = st.selectbox("StreamingMovies", ["Yes", "No", "No internet service"])
contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
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
    # Prepare the input data for prediction
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
    # charges_only = df_2[["MonthlyCharges", "TotalCharges"]]

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

    # st.write(final_df)
    # make sure monthly charges and all other one hot encoded categories : are in the correct order (see training data set x_train)
    # how to upload csv? (after uplading -> do one hot encoding again on it (categorical columns only))

    # Predict churn on final_df
    if "MonthlyCharges" in final_df.columns and "TotalCharges" in final_df.columns:
        single = model.predict(final_df.tail(1))
        probability = model.predict_proba(final_df.tail(1))[:, 1]

        if single == 1:
            st.write("This customer is likely to churn!!")
            st.write(f"Confidence: {probability*100}%")
        else:
            st.write("This customer is likely to continue!!")
            st.write(f"Confidence: {probability*100}%")
    else:
        st.write("Please provide values for 'MonthlyCharges' and 'TotalCharges'.")
