# sentry_lite/main.py

import streamlit as st
import joblib
from sentry_lite.risk_model import predict_risk

st.title("SENTRY-Lite Sponsor Vetting")

# User inputs from the UI
sponsor_name = st.text_input("Sponsor Name")
age = st.slider("Child Age", 5, 17)
gender = st.selectbox("Gender", ["M", "F"])
country = st.selectbox("Country", ["Honduras", "Guatemala", "El Salvador", "Mexico"])
family_ties = st.selectbox("Family Ties Status", ["Verified", "Unverified", "Unknown"])
criminal_history = st.checkbox("Sponsor Criminal History")
past_sponsorships = st.slider("Past Sponsorships", 0, 5)
past_denials = st.slider("Past Denials", 0, 3)
financial_status = st.selectbox("Financial Status", ["Low", "Medium", "High"])
prior_trafficking = st.checkbox("Prior Trafficking History")
network_affiliation = st.checkbox("Network Affiliation")
known_route = st.checkbox("Known Trafficking Route")

# Define the model path (adjust if needed)
MODEL_PATH = "models/sar_model.pkl"

# Button to run risk scoring
if st.button("Run Risk Scoring"):
    # Load the model
    model = joblib.load(MODEL_PATH)
    
    # Prepare the record for scoring (note: only a subset of features come from user input)
    record = {
        "Age": age,
        "Gender": gender,
        "Country_of_Origin": country,
        "Family_Ties_Status": family_ties,
        "Criminal_History": int(criminal_history),
        "Past_Sponsorships": past_sponsorships,
        "Past_Denials": past_denials,
        "Financial_Status": financial_status,
        "Prior_Trafficking_History": int(prior_trafficking),
        "Trafficking_Network_Affiliation": int(network_affiliation),
        "Known_Trafficking_Route": int(known_route)
    }

    # Obtain the risk score from the model.
    score = predict_risk(record, model)

    # Display the risk score and a risk category based on thresholds.
    st.metric(label="Risk Score", value=f"{score:.2f}%")
    if score > 85:
        st.error("HIGH RISK")
    elif score > 60:
        st.warning("MEDIUM RISK")
    else:
        st.success("LOW RISK")
