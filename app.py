#Installing necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Importing Dataset
data = pd.read_csv('car_price.csv')
data.head()

# Converting the categorical columns into numeric using one-hot encoding
data_encoded = pd.get_dummies(data, columns=['Brand', 'Fuel Type', 'Transmission', 'Condition', 'Model'])
data_encoded = data_encoded.drop(['Car ID'], axis=1)
data_encoded.head()

# Defining Features (X) and Target (y)
X = data_encoded.drop('Price', axis=1)
y = data['Price']

# Splitting the data into training and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing Random Forest Regressor model
model = RandomForestRegressor()

# Training model
model.fit(X_train, y_train)

# Making Predictions
y_pred = model.predict(X_test)

# Evaluating the model predictions
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R2 Score: {r2:.2f}")

#Streamlit UI & User Input
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗")
st.title("🚗 Car Price Predictor")
st.write("Enter the car details below to estimate its market price.")

# Sidebar for input
brand = st.selectbox("Brand", sorted(data['Brand'].unique()))
car_model = st.selectbox("Model", sorted(data['Model'].unique()))
fuel_type = st.selectbox("Fuel Type", sorted(data['Fuel Type'].unique()))
transmission = st.selectbox("Transmission", sorted(data['Transmission'].unique()))
condition = st.selectbox("Condition", sorted(data['Condition'].unique()))

# Create single-row input DataFrame
input_df = pd.DataFrame([{
    'Brand': brand,
    'Model': car_model,
    'Fuel Type': fuel_type,
    'Transmission': transmission,
    'Condition': condition
}])

# One-hot encode the input
input_encoded = pd.get_dummies(input_df)
missing_cols = set(X.columns) - set(input_encoded.columns)
for col in missing_cols:
    input_encoded[col] = 0
input_encoded = input_encoded[X.columns]  # Align column order

# Predict button
if st.button("Predict Price"):
    prediction = model.predict(input_encoded)[0]
    st.success(f"💰 Estimated Car Price: ${prediction:,.2f}")

# Optional: Show model performance
with st.expander("📊 Model Evaluation"):
    st.write(f"**Mean Squared Error:** {mse:.2f}")
    st.write(f"**R² Score:** {r2:.2f}")