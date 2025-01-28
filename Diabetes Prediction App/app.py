from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/result', methods=['POST'])
def result():
    # Get form data from the user input
    age = float(request.form['Age'])
    glucose = float(request.form['Glucose'])
    blood_pressure = float(request.form['BloodPressure'])
    insulin = float(request.form['Insulin'])
    bmi = float(request.form['BMI'])
    skin_thickness = float(request.form['SkinThickness'])

    # Determine blood sugar range
    blood_sugar_range = calculate_blood_sugar_range(glucose)

    # Simple logic to determine diabetes prediction
    prediction = 'positive' if glucose > 140 or bmi > 30 else 'negative'

    # Get diet plan and quotes based on the result
    data = get_diet_plan(prediction, glucose, bmi)
    data['blood_sugar_range'] = blood_sugar_range  # Add range to the data dictionary

    # Generate a positive quote for users with a positive result
    quote = get_positive_quote() if prediction == 'positive' else None

    return render_template('result.html', data=data, quote=quote)

def calculate_blood_sugar_range(glucose):
    if glucose < 100:
        return "Normal (Under 100 mg/dL)"
    elif 100 <= glucose <= 125:
        return "Prediabetes Range (100-125 mg/dL)"
    else:
        return "Diabetes Range (Over 125 mg/dL)"

def get_diet_plan(prediction, glucose, bmi):
    diet_data = {}

    if prediction == 'positive':
        if glucose > 200:
            severity = "Severe"
            diet_data = {
                'severity': severity,
                'food': ["Lean meats, whole grains, legumes"],
                'fruits': ["Berries, Apples (in moderation)"],
                'vegetables': ["Leafy greens, broccoli"],
                '5210_rule': ["5 servings of fruits/vegetables", "1 hour physical activity", "2 hours or less screen time", "0 sugary drinks"],
            }
        elif glucose > 140:
            severity = "Moderate"
            diet_data = {
                'severity': severity,
                'food': ["Whole grains, beans, legumes"],
                'fruits': ["Apples, Pears, Citrus"],
                'vegetables': ["Spinach, Kale"],
                '5210_rule': ["5 servings of fruits/vegetables", "1 hour physical activity", "2 hours or less screen time", "0 sugary drinks"],
            }
        else:
            severity = "Mild"
            diet_data = {
                'severity': severity,
                'food': ["Whole wheat, Oats, Nuts"],
                'fruits': ["Berries, Apples, Pears"],
                'vegetables': ["Leafy greens, Tomatoes"],
                '5210_rule': ["5 servings of fruits/vegetables", "1 hour physical activity", "2 hours or less screen time", "0 sugary drinks"],
            }
    else:
        diet_data = {
            'severity': 'Negative',
            'food': ["Whole grains, fruits, lean proteins, healthy fats"],
            'fruits': ["Berries, Apples, Pears"],
            'vegetables': ["Carrots, Spinach, Cabbage"],
            '5210_rule': ["5 servings of fruits/vegetables", "1 hour physical activity", "2 hours or less screen time", "0 sugary drinks"],
        }

    return diet_data

def get_positive_quote():
    quotes = [
        "Your health is an investment, not an expense.",
        "Believe in yourself and your ability to overcome challenges.",
        "Take care of your body; it’s the only place you have to live.",
       "Knowledge is the best prescription for a healthier life.",
      "Healthy living is not a goal; it’s a journey.",
      "Small changes can lead to a lifetime of wellness",
    ]
    return random.choice(quotes)

if __name__ == "__main__":
    app.run(debug=True)
