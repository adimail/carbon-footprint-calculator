import streamlit as st
from modules.utils import carbon_footprint_calculator
from modules.utils import input_preprocessing, sample, chart
import pandas as pd
import pickle
import numpy as np


def model_page():
    st.title("Carbon footprint calculator")
    st.write(
        "Calculate how many trees do you own nature")
    st.divider()

    df = carbon_footprint_calculator()
    data = input_preprocessing(df)

    sample_df = pd.DataFrame(data=sample,index=[0])
    sample_df[sample_df.columns] = 0
    sample_df[data.columns] = data

    ss = pickle.load(open("./models/scale.sav","rb"))
    model = pickle.load(open("./models/model.sav","rb"))
    prediction = round(np.exp(model.predict(ss.transform(sample_df))[0]))
    tree_count = round(prediction / 411.4)

    st.sidebar.image(chart(model,ss, sample_df,prediction), use_column_width="auto")
    if(tree_count > 0):
        st.sidebar.markdown(f"""You owe nature <b>{tree_count}</b> trees""",  unsafe_allow_html=True)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

def home_page():

    st.title("Carbon footprint calculator")
    st.divider()

    st.markdown("""
    # 🌳About Carbon Footprint

    A carbon footprint measures the total greenhouse gas emissions linked to an individual, organization, event, or product. It's a crucial metric for gauging our impact on the environment and climate change.

    # 🌳Why It Matters

    ####  🍃Climate Impact
    Reducing your carbon footprint directly contributes to global efforts against climate change, mitigating extreme weather and rising temperatures.

    #### 🍃Resource Conservation
    Cutting carbon often means using fewer natural resources, and promoting sustainability in water, energy, and raw materials.

    #### 🍃Health and Well-being
    Lowering emissions supports healthier lifestyle choices, improving air quality and physical well-being.

    #### 🍃Sustainable Practices
    Measuring and managing your carbon footprint encourages eco-friendly choices, fostering a more sustainable society.

    #### 🍃Responsibility
    Acknowledging and addressing your carbon impact demonstrates social and environmental responsibility.
    
    ------
            
    This project was made by **_Sanjana Godse_** as part of the term work project for Environmental informatics.
    """)