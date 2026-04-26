import streamlit as st
import pandas as pd
import joblib

# load model
model = joblib.load("flight_price_model.pkl")
le_airline = joblib.load("airline_encoder.pkl")
le_source = joblib.load("source_encoder.pkl")
le_dest = joblib.load("dest_encoder.pkl")
columns_order = joblib.load("columns.pkl")

st.title("✈️ Flight Price Prediction")

st.write("Enter flight details:")


days_left = st.number_input("Days Until Journey (How many days from today?)", min_value=1, max_value=60, value=10)
duration = st.number_input("Duration (minutes)", min_value=30, max_value=1000, value=150)
airline = st.selectbox("Airline", le_airline.classes_)
source = st.selectbox(
    "From",
    ["Select City"] + sorted(le_source.classes_)
)

destination = st.selectbox(
    "To",
    ["Select City"] + sorted(le_dest.classes_)
)
flight_class = st.selectbox("Class", ["Economy", "Business"])
stops = st.selectbox("Stops", ["Non-stop", "1 Stop", "2 Stops"])
departure = st.selectbox("Departure Time", ["Morning", "Afternoon", "Evening", "Night"])
arrival = st.selectbox("Arrival Time", ["Morning", "Afternoon", "Evening", "Night"])

class_map = {"Economy": 0, "Business": 1}
stops_map = {"Non-stop": 0, "1 Stop": 1, "2 Stops": 2}
time_map = {"Morning": 0, "Afternoon": 1, "Evening": 2, "Night": 3}

class_encoded = class_map[flight_class]
stops_encoded = stops_map[stops]
departure_encoded = time_map[departure]
arrival_encoded = time_map[arrival]
import math

city_coords = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867)
}

def calculate_distance_ui(src, dest):
    return math.sqrt((city_coords[src][0] - city_coords[dest][0])**2 +
                     (city_coords[src][1] - city_coords[dest][1])**2)

duration_per_stop = duration / (stops_encoded + 1)

if st.button("Predict Price"):
    
    if source == "Select City" or destination == "Select City":
        st.error("Please select both source and destination")
        st.stop()
    
    if source == destination:
        st.error("Source and destination cannot be same")
        st.stop()

    if duration < 60:
        st.error("Duration too low for a flight")
        st.stop()

    distance = calculate_distance_ui(source, destination)

    airline_encoded = le_airline.transform([airline])[0]
    source_encoded = le_source.transform([source])[0]
    destination_encoded = le_dest.transform([destination])[0]

    input_data = {
        "airline": airline_encoded,
        "source_city": source_encoded,
        "destination_city": destination_encoded,
        "days_left": days_left,
        "duration_minutes": duration,
        "class_encoded": class_encoded,
        "stops_encoded": stops_encoded,
        "departure_encoded": departure_encoded,
        "arrival_encoded": arrival_encoded,
        "distance": distance,
        "duration_per_stop": duration / (stops_encoded + 1)
    }

    input_df = pd.DataFrame([input_data])
    input_df = input_df[columns_order]

    prediction = model.predict(input_df)[0]

    lower = prediction * 0.9
    upper = prediction * 1.1

    st.success(f"Estimated Price: ₹ {round(prediction, 2)}")
    st.info(f"Expected Range: ₹ {round(lower, 2)} - ₹ {round(upper, 2)}")
    st.subheader("Key Factors Affecting Price")

    st.write("""
    - ⏱ Duration has major impact  
    - 📅 Days left affects demand  
    - ✈️ Stops increase price  
    """)