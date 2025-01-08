import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

scaler = pickle.load(open('scaler.pkl', 'rb'))
svr = pickle.load(open('svr_model.pkl', 'rb'))

# Header
st.title("Forecasting Healthcare Insurance Expenses for Individuals and Families Using Predictive Modeling")
st.subheader("""
In the contemporary world, every individual aspires to ensure a joyful, secure, and worry-free future for themselves and their loved ones. 
Consequently, individuals are allocating funds towards various objectives such as enhancing mental well-being through travel, fostering physical health via gyms and yoga, 
and promoting positive dietary habits. Despite investing substantially in these pursuits, unforeseen illnesses often arise, leading to substantial medical expenses. 

Amid the age of technological progress and advancements, even minor medical procedures can incur significant costs within reputable healthcare institutions. 
The expenses related to medications and medical tests further contribute to the financial burden. In such circumstances, achieving substantial savings for the entire family becomes a formidable challenge. 

When savings prove insufficient to cover sudden high expenses, individuals experience anxiety and distress, turning what should be a straightforward situation into a nightmarish ordeal. 
To counter these uncertainties, Health Insurance emerges as a safeguard for individuals across various socioeconomic strata. 
By paying a nominal insurance premium, individuals gain the assurance of being prepared to meet urgent medical needs. 
This provides a sense of security and confidence, alleviating the fear associated with sudden financial burdens.
""")

# Collect user input
age = st.number_input("What is your age:", min_value=18, max_value=120)
BMI = st.number_input("What is your BMI:", min_value=10.0, max_value=50.0, step=0.5)
gender = st.selectbox("What is your Gender", ['M', 'F'])
child = st.selectbox("Number of children", [0, 1, 2, 3, 4, 5])
smoke = st.selectbox("Do you smoke?", ['Y', 'N'])
location = st.selectbox("Choose your location", ['Northeast', 'Northwest', 'Southeast', 'Southwest'])

# Encoding the input data
sex_male = 1 if gender == 'M' else 0

Children_0 = Children_1 = Children_2 = Children_3 = Children_4 = Children_5 = 0
if child == 0:
    Children_0 = 1
elif child == 1:
    Children_1 = 1
elif child == 2:
    Children_2 = 1
elif child == 3:
    Children_3 = 1
elif child == 4:
    Children_4 = 1
elif child == 5:
    Children_5 = 1

smoking_status_yes = 1 if smoke == 'Y' else 0

region = region_northeast = region_northwest = region_southeast = region_southwest = 0
if region == 'Northeast':
    region_northeast = 1
elif region == 'Northwest':
    region_northwest = 1
elif region == 'Southeast':
    region_southeast = 1
elif region == 'Southwest':
    region_southwest = 1

# Prepare the input data for prediction
data = [
    age, BMI, sex_male, Children_1, Children_2, Children_3, Children_4, Children_5,
    smoking_status_yes, region_northwest, region_southeast, region_southwest
]
df = pd.DataFrame([data], columns=[
    'age', 'bmi', 'Gender_male', 'Children_1', 'Children_2', 'Children_3', 'Children_4', 'Children_5',
    'smoking_status_yes', 'region_northwest', 'region_southeast', 'region_southwest'
])

# Transform the data using the scaler
df_scaled = scaler.transform(df)

# Predict using the SVR model
pr = np.exp(svr.predict(df_scaled))

# Show the result
predict = f"Total Insurance Cost: ${pr[0]:.2f}"
if st.button("Insurance cost"):
    st.write(predict)


emi_months = 0
emi_months = st.select_slider("Select Your Months of EMI (Slider)", options=list(range(1, 13)))

Monthly_emi = pr/emi_months
st.subheader(f"Monthly Insurance Cost (EMI): ${Monthly_emi[0]:.2f}")

