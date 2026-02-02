import numpy as np


class RuleBasedInterpreter:
    def __init__(self):
        self.food_rules = {
            'dairy': {
                'max_temp': 8,
                'max_humidity': 75,
                'danger_zone_temp': 12
            },
            'meat': {
                'max_temp': 6,
                'max_humidity': 70,
                'danger_zone_temp': 8
            },
            'vegetables': {
                'max_temp': 8,
                'max_humidity': 95,
                'danger_zone_temp': 15
            },
            'fruits': {
                'max_temp': 10,
                'max_humidity': 90,
                'danger_zone_temp': 20
            },
            'bakery': {
                'max_temp': 25,
                'max_humidity': 60,
                'danger_zone_temp': 30
            },
            'seafood': {
                'max_temp': 4,
                'max_humidity': 70,
                'danger_zone_temp': 5
            }
        }

        self.storage_rules = {
            'refrigerator': {'ideal_temp': 4, 'ideal_humidity': 65},
            'freezer': {'ideal_temp': -18, 'ideal_humidity': 60},
            'pantry': {'ideal_temp': 20, 'ideal_humidity': 50}
        }

    def get_food_type_label(self, food_type_encoded):
        food_types = ['bakery', 'dairy', 'fruits', 'meat', 'seafood', 'vegetables']
        if food_type_encoded < len(food_types):
            return food_types[food_type_encoded]
        return 'dairy'

    def get_storage_type_label(self, storage_type_encoded):
        storage_types = ['freezer', 'pantry', 'refrigerator']
        if storage_type_encoded < len(storage_types):
            return storage_types[storage_type_encoded]
        return 'refrigerator'

    def check_extreme_conditions(self, food_type, storage_type, temperature, humidity, days_stored):
        issues = []
        severity = 'none'

        rules = self.food_rules.get(food_type, self.food_rules['dairy'])
        storage_ideal = self.storage_rules.get(storage_type, self.storage_rules['refrigerator'])

        if temperature > rules['danger_zone_temp']:
            issues.append(f'Temperature ({temperature}°C) exceeds danger zone threshold ({rules["danger_zone_temp"]}°C)')
            severity = 'critical'
        elif temperature > rules['max_temp']:
            issues.append(f'Temperature ({temperature}°C) above recommended maximum ({rules["max_temp"]}°C)')
            severity = 'high' if severity == 'none' else severity

        if humidity > rules['max_humidity']:
            issues.append(f'Humidity ({humidity}%) above recommended maximum ({rules["max_humidity"]}%)')
            severity = 'high' if severity in ['none', 'medium'] else severity

        if storage_type == 'refrigerator' and temperature > 8:
            issues.append('Refrigerator temperature too high - rapid bacterial growth risk')
            severity = 'critical'

        if storage_type == 'freezer' and temperature > -5:
            issues.append('Freezer temperature too high - food not properly frozen')
            severity = 'high' if severity == 'none' else severity

        if storage_type == 'pantry' and humidity > 70:
            issues.append('High pantry humidity - mold growth risk')
            severity = 'medium' if severity == 'none' else severity

        return issues, severity

    def adjust_prediction(self, predicted_days, issues, severity, days_stored):
        adjustment_factor = 1.0

        if severity == 'critical':
            adjustment_factor = 0.3
        elif severity == 'high':
            adjustment_factor = 0.5
        elif severity == 'medium':
            adjustment_factor = 0.7

        adjusted_days = predicted_days * adjustment_factor
        adjusted_days = max(0, adjusted_days)

        return adjusted_days

    def classify_safety(self, remaining_days, days_stored, issues):
        if remaining_days <= 0:
            return 'Expired'
        elif remaining_days <= 2:
            return 'Consume Soon'
        elif remaining_days <= 7:
            return 'Consume Soon'
        else:
            return 'Safe'

    def get_recommendations(self, food_type, storage_type, temperature, humidity, remaining_days):
        recommendations = []

        if remaining_days <= 2:
            recommendations.append('Consume immediately or discard')

        if temperature > 10 and storage_type == 'refrigerator':
            recommendations.append('Lower refrigerator temperature to 2-4°C')

        if humidity > 80:
            recommendations.append('Reduce humidity to prevent mold growth')

        if storage_type == 'pantry' and temperature > 25:
            recommendations.append('Move to cooler location or refrigerate')

        if remaining_days > 0 and remaining_days <= 5:
            recommendations.append('Monitor closely for signs of spoilage')

        return recommendations
