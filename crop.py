# crop_recommender_full_fixed.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ----------------------------
# 1. Sample Dataset with Yields & Profits
# ----------------------------
data = {
    "District": ["Ludhiana", "Amritsar", "Patiala", "Karnal", "Nagpur",
                 "Mumbai", "Hyderabad", "Bengaluru", "Chennai", "Kolkata"],
    "Rainfall": [880, 900, 870, 850, 1100, 2400, 950, 970, 1200, 1600],
    "Temperature": [25, 24, 26, 27, 30, 32, 28, 23, 29, 26],
    "Soil_pH": [6.7, 6.8, 6.5, 6.9, 6.2, 5.8, 6.4, 6.6, 6.3, 6.5],
    "Crop": ["Wheat", "Wheat", "Rice", "Rice", "Cotton",
             "Sugarcane", "Maize", "Millets", "Pulses", "Jute"],
    "Yield": [42, 44, 39, 38, 25, 80, 32, 28, 22, 30],  # q/ha
    "Profit": [45000, 46000, 41000, 40000, 35000, 90000, 30000, 27000, 20000, 32000],  # ₹/ha
    "SuccessRate": [78, 82, 75, 73, 65, 90, 70, 68, 60, 72]  # %
}
df = pd.DataFrame(data)

# ----------------------------
# 2. Encode & Train (with scaling)
# ----------------------------
le = LabelEncoder()
df = df.copy()
df["Crop_encoded"] = le.fit_transform(df["Crop"])

FEATURES = ["Rainfall", "Temperature", "Soil_pH"]
X = df[FEATURES].values.astype(float)
y = df["Crop_encoded"].values

scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_scaled, y)

# ----------------------------
# 3. Streamlit UI
# ----------------------------
st.set_page_config(page_title="🌱 Smart Crop Advisor", page_icon="🌾", layout="centered")
st.title("🌱 Smart Crop Advisor")
st.write("Find the **best crop** for your farm using soil, weather, and location conditions.")

input_type = st.radio("Choose input type:", ["📍 Select District", "✍️ Manual Input"])

if input_type == "📍 Select District":
    district = st.selectbox("Choose your District", df["District"].unique())
    district_row = df.loc[df["District"] == district].iloc[0]
    rainfall = float(district_row["Rainfall"])
    temperature = float(district_row["Temperature"])
    soil_ph = float(district_row["Soil_pH"])
else:
    # set reasonable defaults and enforce numeric types
    rainfall = float(st.number_input("🌧️ Enter average Rainfall (mm)", min_value=0.0, max_value=10000.0, value=1000.0, step=1.0))
    temperature = float(st.number_input("🌡️ Enter average Temperature (°C)", min_value=-10.0, max_value=60.0, value=25.0, step=0.5))
    soil_ph = float(st.number_input("🧪 Enter Soil pH", min_value=0.0, max_value=14.0, value=6.5, step=0.1))

if st.button("✅ Get Crop Recommendation"):
    input_array = np.array([[rainfall, temperature, soil_ph]], dtype=float)
    input_scaled = scaler.transform(input_array)

    try:
        pred_encoded = knn.predict(input_scaled)[0]
        best_crop = le.inverse_transform([pred_encoded])[0]
    except Exception as e:
        st.error(f"Could not compute recommendation: {e}")
    else:
        best_row = df.loc[df["Crop"] == best_crop].iloc[0]

        st.success("✅ Best Crop for Your Farm:")
        st.markdown(
            f"""
            🌾 **{best_crop}**
            - Expected Yield: **{best_row['Yield']} q/ha**
            - Expected Profit: **₹{int(best_row['Profit']):,} per hectare**
            - Success Rate: **{best_row['SuccessRate']}% in similar regions**
            """
        )

        # Nearest neighbors (indices into original df)
        neighbors_idx = knn.kneighbors(input_scaled, return_distance=False)[0]
        neighbor_rows = df.iloc[neighbors_idx].reset_index(drop=True)

        # Alternatives (from neighbors but excluding chosen crop)
        alternatives = neighbor_rows[neighbor_rows["Crop"] != best_crop].drop_duplicates(subset=["Crop"])

        st.subheader("🌱 Alternative Options")
        if not alternatives.empty:
            for i, (_, alt_row) in enumerate(alternatives.iterrows(), start=1):
                st.info(f"{i}. {alt_row['Crop']} – Yield: {alt_row['Yield']} q/ha, Profit: ₹{int(alt_row['Profit']):,}/ha")
        else:
            st.info("No alternative crops found among the closest neighbors.")

        # Show neighbor districts considered
        st.subheader("📊 Neighbor Districts Considered")
        for _, nr in neighbor_rows.iterrows():
            st.write(f"- {nr['District']} → {nr['Crop']} ({nr['Yield']} q/ha, ₹{int(nr['Profit']):,})")
