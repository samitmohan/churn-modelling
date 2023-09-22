first_telc.csv : template for csv

[gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines,
InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
MonthlyCharges, TotalCharges] : 19 objects.

tel_churn.csv : modified version of original data set WA_Fn-UseC...

includes 50 objects (gender_Female, gender_Male, Partner_No, Parnter_Yes) etc..
tenure_group_1 - 12 | tenure_group_13 - 24 | tenure_group_25 - 36 |
tenure_group_37 - 48 | tenure_group_49 - 60 | tenure_group_61 - 72 p

Wa_Fn-UseC Original.

[customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines,
InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod,
MonthlyCharges, TotalCharges, churn] : 21 objects.

19 concrete inputs

ONE HOT -> get_dummies -> 50-51 columns

As input : expected : concrete values : 19 inputs. {can also do CSV}

take 19 inputs, create tenure grp since model testing has tenure grps, drop
'tenure'

then convert everything to one hot encoder (all 19 to 50/51 columns)
{technically not 19, probably 17 (exclude monthly and total charges)}

TODO : fix monthlycharges issue : make app work
ADD : 2 Options : Manual Select and Upload CSV (use on hot encoder after uploaded)
      Time taken to process the CSV (multi-threading)
      Database (Track what all is uploaded before)
      Images (Make UI better, genpact logo etc..)
      About Page.
# Try to make it look like ATS resume
