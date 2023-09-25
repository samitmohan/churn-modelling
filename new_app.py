import streamlit as st
import pandas as pd
import pickle

model = pickle.load(open("model.sav", "rb"))

# Add an "About" page
def about_page():
    st.title("About")
    st.write(
        "This app predicts customer churn based on user-provided data. "
        "You can input customer details manually or upload a CSV file."
    )
    st.write("Made with ❤️ by Your Name")

# Create the main app
def main():
    st.title("Customer Churn Prediction")

    # Add options for "Online" or "Upload CSV"
    data_option = st.radio("Select Data Input Method:", ("Online", "Upload CSV"))

    if data_option == "Online":
        # Input customer data
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

            # Perform the same data preprocessing as before

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

    elif data_option == "Upload CSV":
        st.write("Upload your CSV file here:")
        uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            # Perform the same data preprocessing as before

            # Predict churn on final_df (for the uploaded CSV data)
            # ...

    # Add a link to the "About" page
    st.sidebar.markdown("[About](#about)")
    
    # To add more styling/UI improvements, you can use CSS in Streamlit.
    # You can also explore Streamlit's built-in layout elements and widgets to enhance the UI further.

if __name__ == "__main__":
    main()
