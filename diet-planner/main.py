from model import predict_diet, calculate_bmi

print("=== AI Diet Planner ===")

# User input
age = int(input("Enter age: "))
gender = int(input("Enter gender (Male=1, Female=0): "))
weight = float(input("Enter weight (kg): "))
height = float(input("Enter height (cm): "))
activity = int(input("Activity (1=Low, 2=Moderate, 3=High): "))
goal = int(input("Goal (0=Maintain, 1=Loss, 2=Gain): "))

# BMI
bmi, category = calculate_bmi(weight, height)

# Prediction
calories, diet, meal_plan = predict_diet(age, gender, weight, activity, goal)

# Output
print("\n--- RESULT ---")
print(f"BMI: {bmi} ({category})")
print(f"Recommended Calories: {calories} kcal")
print(f"Suggested Diet Type: {diet}")

print("\nMeal Plan:")
for meal, item in meal_plan.items():
    print(f"{meal}: {item}")
    