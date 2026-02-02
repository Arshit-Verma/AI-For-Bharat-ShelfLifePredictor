import numpy as np
import pandas as pd
import os


class InferencePipeline:
    def __init__(self, preprocessor, feature_engineer, model, rule_interpreter):
        self.preprocessor = preprocessor
        self.feature_engineer = feature_engineer
        self.model = model
        self.rule_interpreter = rule_interpreter

    def predict(self, input_data):
        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        elif isinstance(input_data, list):
            df = pd.DataFrame(input_data)
        else:
            df = input_data.copy()

        required_columns = ['food_type', 'temperature', 'humidity', 'storage_type', 'days_stored']
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0

        df_processed = self.preprocessor.transform(df)
        df_featured = self.feature_engineer.transform(df_processed)

        predictions = self.model.predict(df_featured)

        results = []

        for i, pred in enumerate(predictions):
            food_type_str = str(df['food_type'].iloc[i])
            storage_type_str = str(df['storage_type'].iloc[i])
            
            food_type = food_type_str if food_type_str in ['dairy', 'meat', 'vegetables', 'fruits', 'bakery', 'seafood'] else 'dairy'
            storage_type = storage_type_str if storage_type_str in ['refrigerator', 'freezer', 'pantry'] else 'refrigerator'
            
            temperature = df['temperature'].iloc[i]
            humidity = df['humidity'].iloc[i]
            days_stored = df['days_stored'].iloc[i]

            issues, severity = self.rule_interpreter.check_extreme_conditions(
                food_type, storage_type, temperature, humidity, days_stored
            )

            adjusted_prediction = self.rule_interpreter.adjust_prediction(
                pred, issues, severity, days_stored
            )

            safety_class = self.rule_interpreter.classify_safety(
                adjusted_prediction, days_stored, issues
            )

            recommendations = self.rule_interpreter.get_recommendations(
                food_type, storage_type, temperature, humidity, adjusted_prediction
            )

            result = {
                'food_type': food_type,
                'storage_type': storage_type,
                'temperature': temperature,
                'humidity': humidity,
                'days_stored': days_stored,
                'predicted_remaining_days': round(float(adjusted_prediction), 2),
                'raw_prediction': round(float(pred), 2),
                'safety_classification': safety_class,
                'issues': issues,
                'severity': severity,
                'recommendations': recommendations,
                'feature_importance': self.model.get_feature_importance(5)
            }

            results.append(result)

        if len(results) == 1:
            return results[0]
        return results

    def predict_single(self, food_type, temperature, humidity, storage_type, days_stored):
        input_data = {
            'food_type': food_type,
            'temperature': temperature,
            'humidity': humidity,
            'storage_type': storage_type,
            'days_stored': days_stored
        }
        return self.predict(input_data)

    def explain_prediction(self, result):
        explanation = []

        explanation.append(f"Food Type: {result['food_type']}")
        explanation.append(f"Storage: {result['storage_type']}")
        explanation.append(f"Current Temperature: {result['temperature']}°C")
        explanation.append(f"Current Humidity: {result['humidity']}%")
        explanation.append(f"Days Already Stored: {result['days_stored']}")

        explanation.append(f"\nPredicted Remaining Shelf Life: {result['predicted_remaining_days']} days")
        explanation.append(f"Safety Classification: {result['safety_classification']}")

        if result['issues']:
            explanation.append(f"\nDetected Issues ({result['severity']} severity):")
            for issue in result['issues']:
                explanation.append(f"  - {issue}")

        if result['recommendations']:
            explanation.append(f"\nRecommendations:")
            for rec in result['recommendations']:
                explanation.append(f"  - {rec}")

        return '\n'.join(explanation)
