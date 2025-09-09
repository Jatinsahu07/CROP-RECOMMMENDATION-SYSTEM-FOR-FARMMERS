🌱 Smart Crop Advisor

A decision-support tool that helps farmers choose the best crop based on climate, soil conditions, and sustainability factors.


---

✅ Features

Crop Recommendation (AI-powered)

Uses KNN model with Rainfall, Temperature, and Soil pH.

Two input options:

📍 Select District (auto-fills climate & soil data).

✍️ Manual Input (farmer enters data).



Detailed Results

Best crop recommendation with Yield, Profit, Success Rate.

Alternative crop suggestions ranked by performance.

Neighbor district data considered in predictions.


Sustainability Insights (unique feature)

💧 Water Requirement (litres/kg).

🧪 Fertilizer & Pesticide Need.

🌿 Soil Health Impact (enriching / neutral / degrading).

🌍 Carbon Footprint (low / medium / high).

Sustainability Score (1–20 scale).


Future-Ready Features

Realtime GPS location access.

Weather API integration (rainfall, temp).

Soil data API integration.


Visualization (planned)

Bar chart comparison of Yield, Profit, and Sustainability Score.

Ranking mode to prioritize sustainable crops.




---

🚀 How It Works

1. Farmer selects a district OR enters rainfall, temperature, and soil pH.


2. The KNN model finds the best crop based on climate & soil.


3. System compares yield, profit, and sustainability factors.


4. Farmer sees:

Best crop ✅

Alternative crops 🌱

Detailed sustainability report 🌍





---

📊 Example Output

Best Crop: 🌾 Wheat

Yield: 42 q/ha

Profit: ₹45,000/ha

Success Rate: 78%


Sustainability Insights:

💧 Water: 1200 L/kg

🧪 Fertilizer: Medium

🌿 Soil: Neutral

🌍 Carbon: Medium

✅ Score: 12/20


Alternatives:

1. Rice → Profit ₹41,000/ha, Score 6/20


2. Maize → Profit ₹30,000/ha, Score 14/20




---

🛠 Tech Stack

Python (scikit-learn, pandas, numpy)

Streamlit (UI dashboard)

APIs (planned): WeatherAPI, SoilGrids, OpenWeatherMap



---

🌍 Impact

This project helps farmers:

Improve profits 💰

Save water 💧

Reduce fertilizer use 🧪

Protect soil health 🌿

Lower carbon emissions 🌍
