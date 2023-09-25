# About

Customer attrition, also known as customer churn, customer turnover, or customer defection, is the loss of clients or customers.

Telephone service companies, Internet service providers, pay TV companies, insurance firms, and alarm monitoring services, often use customer attrition analysis and customer attrition rates as one of their key business metrics because the cost of retaining an existing customer is far less than acquiring a new one. Companies from these sectors often have customer service branches which attempt to win back defecting clients, because recovered long-term customers can be worth much more to a company than newly recruited clients.

Predictive analytics use churn prediction models that predict customer churn by assessing their propensity of risk to churn. Since these models generate a small prioritized list of potential defectors, they are effective at focusing customer retention marketing programs on the subset of the customer base who are most vulnerable to churn.

In this project I aim to perform customer survival analysis and build a model which can predict customer churn. I also aim to build an app which can be used to understand why a specific customer would stop the service and to know his/her expected lifetime value.

## Explaining Code + Files (How it works)

first_telc.csv : template for csv -:

    [gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines,
    InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
    StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
    MonthlyCharges, TotalCharges] : 19 objects.

tel_churn.csv : EDA version of original csv -:

    includes 50 objects (gender_Female, gender_Male, Partner_No, Parnter_Yes) etc..
    tenure_group_1 - 12 | tenure_group_13 - 24 | tenure_group_25 - 36 |
    tenure_group_37 - 48 | tenure_group_49 - 60 | tenure_group_61 - 72 p

Wa_Fn-UseC : Original dataset -:

    [customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines,
    InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
    StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
    MonthlyCharges, TotalCharges, churn] : 21 objects.

19 concrete inputs : ONE HOT -> get_dummies -> 50-51 columns

As input : expected : concrete values : 19 inputs. {can also do CSV}, take 19 inputs, create tenure grp since model testing has tenure grps, drop
'tenure'
then convert everything to one hot encoder (all 19 to 50/51 columns)

## TODO

ASK Vineet
Fix the upload csv method. + fix showing records in upload csv
