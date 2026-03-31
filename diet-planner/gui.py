import tkinter as tk
from tkinter import messagebox, font
from model import predict_diet, calculate_bmi

# --- Styling Constants ---
BG_COLOR = "#F8FAFC"
CARD_BG = "#FFFFFF"
ACCENT_COLOR = "#3B82F6"
TEXT_PRIMARY = "#1E293B"
TEXT_SECONDARY = "#64748B"

def calculate():
    try:
        age = int(age_entry.get())
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        
        bmi, category = calculate_bmi(weight, height)
        calories, diet, meal_plan = predict_diet(age, gender_var.get(), weight, activity_var.get(), goal_var.get())

        res_bmi.config(text=f"{bmi} ({category})")
        res_cal.config(text=f"{calories} kcal")
        res_diet.config(text=f"{diet}")
        
        meal_text = ""
        for m, i in meal_plan.items():
            meal_text += f"● {m}\n{i}\n\n"
        res_plan.config(text=meal_text)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please fill all numerical fields (Age, Weight, Height) correctly.")

root = tk.Tk()
root.title("AI Diet Planner")
root.geometry("500x800")
root.configure(bg=BG_COLOR)

# --- Scrollable Container Logic ---
container = tk.Frame(root, bg=BG_COLOR)
container.pack(fill="both", expand=True)

canvas = tk.Canvas(container, bg=BG_COLOR, highlightthickness=0)
scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
scroll_frame = tk.Frame(canvas, bg=BG_COLOR)

scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scroll_frame, anchor="nw", width=480)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# --- Typography ---
h1 = font.Font(family="Helvetica", size=20, weight="bold")
lbl_font = font.Font(family="Helvetica", size=10, weight="bold")

tk.Label(scroll_frame, text="Diet & Health Profile", font=h1, bg=BG_COLOR, fg=TEXT_PRIMARY).pack(pady=(20, 10))

# --- Input Fields ---
def create_label(text):
    tk.Label(scroll_frame, text=text, font=lbl_font, bg=BG_COLOR, fg=TEXT_SECONDARY).pack(anchor="w", padx=50, pady=(10, 2))

# Age, Weight, Height
create_label("AGE")
age_entry = tk.Entry(scroll_frame, font=("Helvetica", 11), bd=0, highlightthickness=1, highlightbackground="#CBD5E1")
age_entry.pack(fill="x", padx=50, ipady=8)

create_label("WEIGHT (KG)")
weight_entry = tk.Entry(scroll_frame, font=("Helvetica", 11), bd=0, highlightthickness=1, highlightbackground="#CBD5E1")
weight_entry.pack(fill="x", padx=50, ipady=8)
 
create_label("HEIGHT (CM)")
height_entry = tk.Entry(scroll_frame, font=("Helvetica", 11), bd=0, highlightthickness=1, highlightbackground="#CBD5E1")
height_entry.pack(fill="x", padx=50, ipady=8)

# Dropdowns with labels ABOVE
create_label("GENDER")
gender_var = tk.StringVar(value="Male")
gender_menu = tk.OptionMenu(scroll_frame, gender_var, "Male", "Female")
gender_menu.config(bg="white", relief="flat", font=("Helvetica", 10))
gender_menu.pack(fill="x", padx=50)

create_label("ACTIVITY LEVEL")
activity_var = tk.StringVar(value="Low")
activity_menu = tk.OptionMenu(scroll_frame, activity_var, "Low", "Mid", "High")
activity_menu.config(bg="white", relief="flat", font=("Helvetica", 10))
activity_menu.pack(fill="x", padx=50)

create_label("PRIMARY GOAL")
goal_var = tk.StringVar(value="Maintain")
goal_menu = tk.OptionMenu(scroll_frame, goal_var, "Maintain", "Loss", "Gain")
goal_menu.config(bg="white", relief="flat", font=("Helvetica", 10))
goal_menu.pack(fill="x", padx=50)

# Calculate Button
tk.Button(scroll_frame, text="GENERATE MY PLAN", command=calculate, bg=ACCENT_COLOR, 
          fg="white", font=("Helvetica", 12, "bold"), bd=0, cursor="hand2", pady=12).pack(fill="x", padx=50, pady=30)

# --- Result Card ---
card = tk.Frame(scroll_frame, bg=CARD_BG, padx=25, pady=25, relief="flat", highlightthickness=1, highlightbackground="#E2E8F0")
card.pack(fill="both", padx=40, pady=(0, 40))

def add_res_row(label):
    f = tk.Frame(card, bg=CARD_BG)
    f.pack(fill="x", pady=4)
    tk.Label(f, text=label, font=("Helvetica", 10), bg=CARD_BG, fg=TEXT_SECONDARY).pack(side="left")
    v = tk.Label(f, text="--", font=("Helvetica", 10, "bold"), bg=CARD_BG, fg=TEXT_PRIMARY)
    v.pack(side="right")
    return v

res_bmi = add_res_row("BMI Status:")
res_cal = add_res_row("Daily Calories:")
res_diet = add_res_row("Diet Strategy:")

tk.Label(card, text="MEAL PLAN:", font=lbl_font, bg=CARD_BG, fg=ACCENT_COLOR).pack(anchor="w", pady=(15, 5))
res_plan = tk.Label(card, text="", font=("Helvetica", 10), bg=CARD_BG, fg=TEXT_PRIMARY, justify="left", wraplength=340)
res_plan.pack(anchor="w")

root.mainloop()