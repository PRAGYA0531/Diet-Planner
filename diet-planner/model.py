import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier

# Load dataset
data = pd.read_csv("dataset.csv")

# Features (input)
feature_cols = ['age', 'gender', 'weight', 'activity', 'goal']
X = data[feature_cols]

# Targets (output)
y_calories = data['calories']
y_diet = data['diet']

# Split data
X_train, X_test, y_cal_train, y_cal_test = train_test_split(X, y_calories, test_size=0.2, random_state=42)
y_diet_train = train_test_split(X, y_diet, test_size=0.2, random_state=42)[2]

# Train models
calorie_model = LinearRegression()
calorie_model.fit(X_train, y_cal_train)

diet_model = KNeighborsClassifier(n_neighbors=3)
diet_model.fit(X_train, y_diet_train)

# Mappings for Text-to-Number conversion
GENDER_MAP = {"Male": 1, "Female": 0}
ACTIVITY_MAP = {"Low": 1, "Mid": 2, "High": 3}
GOAL_MAP = {"Maintain": 0, "Loss": 1, "Gain": 2}

def get_meal_plan(diet_type):
    plans = {
        "Balanced": {
            "Breakfast": "🥣 Oats + Milk + Fruits",
            "Lunch": "🍞 2 Roti + Dal + Veggies",
            "Snack": "🍎 Nuts + Fruit",
            "Dinner": "🍚 Rice + Paneer + Salad"
        },
        "Low Carb": {
            "Breakfast": "🍳 Boiled Eggs + Green Tea",
            "Lunch": "🥗 Grilled Chicken + Salad",
            "Snack": "🥜 Almonds",
            "Dinner": "🧀 Paneer + Vegetables"
        },
        "High Protein": {
            "Breakfast": "🥪 Eggs + Peanut Butter Toast",
            "Lunch": "🍗 Chicken + Brown Rice",
            "Snack": "🥤 Protein Shake",
            "Dinner": "🥗 Paneer/Chicken + Salad"
        }
    }
    return plans.get(diet_type, plans["Balanced"])

def predict_diet(age, gender_txt, weight, activity_txt, goal_txt):
    # Convert text to numbers using the maps
    gender = GENDER_MAP.get(gender_txt, 1)
    activity = ACTIVITY_MAP.get(activity_txt, 1)
    goal = GOAL_MAP.get(goal_txt, 0)

    # Use DataFrame to avoid UserWarning
    user_data = pd.DataFrame([[age, gender, weight, activity, goal]], columns=feature_cols)

    calories = calorie_model.predict(user_data)[0]
    diet = diet_model.predict(user_data)[0]
    meal_plan = get_meal_plan(diet)

    return round(calories), diet, meal_plan

def calculate_bmi(weight, height):
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    if bmi < 18.5: category = "Underweight"
    elif bmi < 24.9: category = "Normal"
    elif bmi < 29.9: category = "Overweight"
    else: category = "Obese"