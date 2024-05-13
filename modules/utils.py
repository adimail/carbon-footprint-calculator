import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import io

def carbon_footprint_calculator():
    Personal, Travel, Waste, Energy, Consumption = st.tabs(["Personal", "Travel", "Waste", "Energy", "Consumption"])
    
    with Personal:
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Height (cm)", 0, 251, help="Height in cm", value=160)
        with col2:
            weight = st.number_input("Weight (kg)", 0, 250, help="Weight in kg", value=65)

        col1, col2 = st.columns(2)
        with col1:
            sex = st.selectbox('Gender', ["female", "male"])
        with col2:
            social = st.selectbox('Social Activity', ['never', 'often', 'sometimes'], help="...")
        diet = st.selectbox('Diet', ['omnivore', 'pescatarian', 'vegetarian', 'vegan'], help="...")
    
    with Travel:
        col1, col2 = st.columns(2)
        transport = st.selectbox('Transportation', ['public', 'private', 'walk/bicycle'], help="...")
        if transport == "private":
            vehicle_type = st.selectbox('Vehicle Type', ['petrol', 'diesel', 'hybrid', 'lpg', 'electric'], help="...")
        else:
            vehicle_type = "None"
        with col1:
            air_travel = st.selectbox('Monthly Air Travel Hours', ['never', 'rarely', 'frequently', 'very frequently'], help="...")
        with col2:
            vehicle_km = st.slider('Monthly Distance Traveled by Vehicle (km)', 0, 5000, 0)
    
    with Waste:
        col1, col2 = st.columns(2)
        with col1:
           waste_bag = st.selectbox('Waste Bag Size', ['small', 'medium', 'large', 'extra large'])
        with col2:
            recycle = st.multiselect('Recycled Materials', ['Plastic', 'Paper', 'Metal', 'Glass'])
        waste_count = st.slider('Weekly Waste Bags', 0, 10, 0)
    
    with Energy:
        col1, col2 = st.columns(2)
        with col1:
            heating_energy = st.selectbox('Heating Energy Source', ['natural gas', 'electricity', 'wood', 'coal'])
        with col2:
            energy_efficiency = st.selectbox('Energy Efficiency Consideration', ['No', 'Yes', 'Sometimes' ])
        for_cooking = st.multiselect('Cooking Systems', ['microwave', 'oven', 'grill', 'airfryer', 'stove'])
        with col1:
            daily_tv_pc = st.slider('Daily Telivision and Computer Hours', 0, 24, 0)
        with col2:
            internet_daily = st.slider('Daily Internet Usage (Hours)', 0, 24, 0)
    
    with Consumption:
        shower = st.selectbox('Shower Frequency', ['daily', 'twice a day', 'more frequently', 'less frequently'])
        col1, col2 = st.columns(2)
        with col1:
            grocery_bill = st.slider('Monthly Grocery Spending (₹)', 1000, 10000, 100) / 85
        with col2:
            clothes_monthly = st.slider('Monthly Clothes Purchases', 0, 30, 0)

    if (weight is None) or (weight == 0) : weight = 1
    if (height is None) or (height == 0) : height = 1
    calculation = weight / (height/100)**2
    body_type = "underweight" if (calculation < 18.5) else \
                 "normal" if ((calculation >=18.5) and (calculation < 25 )) else \
                 "overweight" if ((calculation >= 25) and (calculation < 30)) else "obese"
    
    # Collect data into a dictionary
    data = {"Body Type": body_type,
            "Sex": sex,
            "Diet": diet,
            "How Often Shower": shower,
            "Heating Energy Source": heating_energy,
            "Transport": transport,
            "Social Activity": social,
            "Monthly Grocery Bill": grocery_bill,
            "Frequency of Traveling by Air": air_travel,
            "Vehicle Monthly Distance Km": vehicle_km,
            "Waste Bag Size": waste_bag,
            "Waste Bag Weekly Count": waste_count,
            "How Long TV PC Daily Hour": daily_tv_pc,
            "Vehicle Type": vehicle_type,
            "How Many New Clothes Monthly": clothes_monthly,
            "How Long Internet Daily Hour": internet_daily,
            "Energy efficiency": energy_efficiency
            }
    
    df = pd.DataFrame(data, index=[0])
    
    return df

def input_preprocessing(data):
    data["Body Type"] = data["Body Type"].map({'underweight':0, 'normal':1, 'overweight':2, 'obese':3})
    data["Sex"] = data["Sex"].map({'female':0, 'male':1})
    data = pd.get_dummies(data, columns=["Diet","Heating Energy Source","Transport","Vehicle Type"], dtype=int)
    data["How Often Shower"] = data["How Often Shower"].map({'less frequently':0, 'daily':1, "twice a day":2, "more frequently":3})
    data["Social Activity"] = data["Social Activity"].map({'never':0, 'sometimes':1, "often":2})
    data["Frequency of Traveling by Air"] = data["Frequency of Traveling by Air"].map({'never':0, 'rarely':1, "frequently":2, "very frequently":3})
    data["Waste Bag Size"] = data["Waste Bag Size"].map({'small':0, 'medium':1, "large":2,  "extra large":3})
    data["Energy efficiency"] = data["Energy efficiency"].map({'No':0, 'Sometimes':1, "Yes":2})
    return data

sample = {'Body Type': 2,
 'Sex': 0,
 'How Often Shower': 1,
 'Social Activity': 2,
 'Monthly Grocery Bill': 230,
 'Frequency of Traveling by Air': 2,
 'Vehicle Monthly Distance Km': 210,
 'Waste Bag Size': 2,
 'Waste Bag Weekly Count': 4,
 'How Long TV PC Daily Hour': 7,
 'How Many New Clothes Monthly': 26,
 'How Long Internet Daily Hour': 1,
 'Energy efficiency': 0,
 'Do You Recyle_Paper': 0,
 'Do You Recyle_Plastic': 0,
 'Do You Recyle_Glass': 0,
 'Do You Recyle_Metal': 1,
 'Cooking_with_stove': 1,
 'Cooking_with_oven': 1,
 'Cooking_with_microwave': 0,
 'Cooking_with_grill': 0,
 'Cooking_with_airfryer': 1,
 'Diet_omnivore': 0,
 'Diet_pescatarian': 1,
 'Diet_vegan': 0,
 'Diet_vegetarian': 0,
 'Heating Energy Source_coal': 1,
 'Heating Energy Source_electricity': 0,
 'Heating Energy Source_natural gas': 0,
 'Heating Energy Source_wood': 0,
 'Transport_private': 0,
 'Transport_public': 1,
 'Transport_walk/bicycle': 0,
 'Vehicle Type_None': 1,
 'Vehicle Type_diesel': 0,
 'Vehicle Type_electric': 0,
 'Vehicle Type_hybrid': 0,
 'Vehicle Type_lpg': 0,
 'Vehicle Type_petrol': 0}

def hesapla(model,ss, sample_df):
    copy_df = sample_df.copy()
    travels = copy_df[["Frequency of Traveling by Air",
                         "Vehicle Monthly Distance Km",
                         'Transport_private',
                          'Transport_public',
                          'Transport_walk/bicycle',
                          'Vehicle Type_None',
                          'Vehicle Type_diesel',
                          'Vehicle Type_electric',
                          'Vehicle Type_hybrid',
                          'Vehicle Type_lpg',
                          'Vehicle Type_petrol']]
    copy_df[list(set(copy_df.columns) - set(travels.columns))] = 0
    travel = np.exp(model.predict(ss.transform(copy_df)))

    copy_df = sample_df.copy()
    energys = copy_df[[ 'Heating Energy Source_coal','How Often Shower', 'How Long TV PC Daily Hour',
                         'Heating Energy Source_electricity','How Long Internet Daily Hour',
                         'Heating Energy Source_natural gas',
                         'Cooking_with_stove',
                          'Cooking_with_oven',
                          'Cooking_with_microwave',
                          'Cooking_with_grill',
                          'Cooking_with_airfryer',
                         'Heating Energy Source_wood','Energy efficiency']]
    copy_df[list(set(copy_df.columns) - set(energys.columns))] = 0
    energy = np.exp(model.predict(ss.transform(copy_df)))

    copy_df = sample_df.copy()
    wastes = copy_df[[  'Do You Recyle_Paper','How Many New Clothes Monthly',
                         'Waste Bag Size',
                         'Waste Bag Weekly Count',
                         'Do You Recyle_Plastic',
                         'Do You Recyle_Glass',
                         'Do You Recyle_Metal',
                         'Social Activity',]]
    copy_df[list(set(copy_df.columns) - set(wastes.columns))] = 0
    waste = np.exp(model.predict(ss.transform(copy_df)))

    copy_df = sample_df.copy()
    diets = copy_df[[ 'Diet_omnivore',
                     'Diet_pescatarian',
                     'Diet_vegan',
                     'Diet_vegetarian', 'Monthly Grocery Bill','Transport_private',
                     'Transport_public',
                     'Transport_walk/bicycle',
                      'Heating Energy Source_coal',
                      'Heating Energy Source_electricity',
                      'Heating Energy Source_natural gas',
                      'Heating Energy Source_wood',
                      ]]
    copy_df[list(set(copy_df.columns) - set(diets.columns))] = 0
    diet = np.exp(model.predict(ss.transform(copy_df)))
    hesap = {"Travel": travel[0], "Energy": energy[0], "Waste": waste[0], "Diet": diet[0]}

    return hesap

def chart(model, scaler,sample_df, prediction):
    p = hesapla(model, scaler,sample_df)

    plt.figure(figsize=(10, 10))
    patches, texts = plt.pie(x=p.values(),
                             labels=p.keys(),
                             explode=[0.03] * 4,
                             labeldistance=0.75,
                             colors=["#29ad9f", "#1dc8b8", "#99d9d9", "#b4e3dd" ], shadow=True,
                             textprops={'fontsize': 20, 'weight': 'bold', "color": "#000000ad"})
    for text in texts:
        text.set_horizontalalignment('center')

    data = io.BytesIO()
    plt.savefig(data, transparent=True)

    background = Image.open("./media/default.png")
    st.sidebar.divider()
    st.sidebar.subheader(f"Monthly Emission {prediction:.0f} kgCO₂e")
    data_back = io.BytesIO()
    background.save(data_back, "PNG")
    background = Image.open(data_back).convert('RGBA')
    piechart = Image.open(data)
    ayak = Image.open("./media/ayak.png").resize((370, 370))
    bg_width, bg_height = piechart.size
    ov_width, ov_height = ayak.size
    x = (bg_width - ov_width) // 2
    y = (bg_height - ov_height) // 2
    piechart.paste(ayak, (x, y), ayak.convert('RGBA'))
    background.paste(piechart, (40, 200), piechart.convert('RGBA'))
    data2 = io.BytesIO()
    background.save(data2, "PNG")
    background = Image.open(data2).resize((700, 700))
    data3 = io.BytesIO()
    background.save(data3, "PNG")
    return data3

