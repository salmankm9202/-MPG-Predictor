import streamlit as st
import pandas as pd
import joblib
from src.database import PredictionLogger
from src.auth import authenticate

# --- Authentication ---
is_authenticated, username = authenticate()
if not is_authenticated:
    st.error("🔒 Please login to access the MPG Predictor")
    st.stop()

# --- App Config ---
st.set_page_config(
    page_title="MPG Predictor",
    page_icon="🚗",
    layout="wide"
)


# --- Load Components ---
@st.cache_resource
def load_model():
    return joblib.load("models/mpg_model.pkl")


model = load_model()
logger = PredictionLogger()

# --- Sidebar ---
with st.sidebar:
    st.success(f"Welcome, {username}!")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    st.header("Vehicle Specs")
    cylinders = st.slider("Cylinders", 3, 8, 4)
    horsepower = st.slider("Horsepower", 50, 250, 100)
    weight = st.slider("Weight (lbs)", 1500, 5500, 3000)
    model_year = st.slider("Model Year", 70, 85, 80)

# --- Main App ---
st.title("🚗 Advanced MPG Predictor")
st.markdown("Predict fuel efficiency based on vehicle specifications")

# Features dictionary
features = {
    'cylinders': cylinders,
    'horsepower': horsepower,
    'weight': weight,
    'model_year': model_year
}

# Prediction Section
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Make Prediction")
    if st.button("Calculate MPG", type="primary"):
        try:
            prediction = model.predict(pd.DataFrame([features]))[0]
            logger.log_prediction(username, features, prediction)

            st.success(f"""
            **Prediction Result**  
            Estimated MPG: `{prediction:.2f}`
            """)

            # Show input summary
            with st.expander("View Input Details"):
                st.json(features)

        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")

with col2:
    st.header("Feature Analysis")

    # Feature Importance Visualization
    try:
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        elif hasattr(model, 'coef_'):
            importance = abs(model.coef_[0])
        else:
            importance = [1 / len(features)] * len(features)

        importance_df = pd.DataFrame({
            'Feature': list(features.keys()),
            'Impact': importance
        }).sort_values('Impact', ascending=False)

        st.bar_chart(importance_df.set_index('Feature'))

    except Exception as e:
        st.warning(f"Couldn't generate feature analysis: {str(e)}")

# Footer
st.divider()
st.caption("""
    *Note: Predictions are based on historical vehicle data.  
    Logged in as: {username}*
""")