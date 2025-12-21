class BMICalculator:
    # Calculates BMI from weight (kg) and height (m)

    def __init__(self, weight, height):
        self.weight = weight
        self.height = height

    def calculate_bmi(self):
        return self.weight / (self.height ** 2)

    def get_category(self):
        bmi = self.calculate_bmi()

        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal weight"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"
