✈️ Flight Price Prediction System

Overview
This project predicts flight ticket prices based on user inputs such as airline, route, duration, stops, and travel time.
It uses Machine Learning (Random Forest) along with feature engineering to improve prediction accuracy.

Features Used
- Airline
- Source & Destination
- Duration (minutes)
- Days left until journey
- Stops
- Departure & Arrival time
- Distance (engineered feature)
- Duration per stop (engineered feature)

Models Used
- Linear Regression
- Random Forest (final model)

Performance
- Random Forest MAE: 2367
- Random Forest RMSE: 5192
- Linear Regression MAE: 4210

Random Forest reduced error by ~40% compared to Linear Regression.

Sample Output
Predicted Price: ₹ 18,779  
Expected Range: ₹ 16,900 – ₹ 20,600

Key Insights
- Flight duration has the highest impact on price
- Prices increase as days left decrease
- More stops generally increase total cost

Tech Stack
- Python
- Pandas, NumPy
- Scikit-learn
- Streamlit

Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
