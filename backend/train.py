import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.preprocessing.preprocessor import DataPreprocessor, load_data
from src.feature_engineering.engineer import FeatureEngineer
from src.models.predictor import ShelfLifePredictor
import json


def train_model():
    print("Loading data...")
    X, y = load_data('data/food_shelf_life.csv')

    print("\nData shape:", X.shape)
    print("Target distribution:")
    print(y.describe())

    print("\nInitializing preprocessor...")
    preprocessor = DataPreprocessor()
    X_processed = preprocessor.fit_transform(X)

    print("Initializing feature engineer...")
    feature_engineer = FeatureEngineer()
    X_featured = feature_engineer.transform(X_processed)

    print("\nFeature columns:")
    print(X_featured.columns.tolist())

    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(
        X_featured, y, test_size=0.2, random_state=42
    )

    print(f"\nTraining set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")

    print("\nTraining Random Forest model with hyperparameter tuning...")
    predictor = ShelfLifePredictor(n_estimators=100, max_depth=15)
    best_params = predictor.hyperparameter_tune(X_train, y_train)

    print("\nBest hyperparameters:")
    for param, value in best_params.items():
        print(f"  {param}: {value}")

    print("\nEvaluating model...")
    metrics = predictor.evaluate(X_test, y_test)

    print("\nModel Performance Metrics:")
    print(f"Mean Absolute Error: {metrics['mae']:.2f} days")
    print(f"Root Mean Squared Error: {metrics['rmse']:.2f} days")
    print(f"R² Score: {metrics['r2']:.3f}")

    print("\nCross-validation results...")
    cv_results = predictor.cross_validate(X_featured, y)
    print(f"Mean MAE: {cv_results['mean_mae']:.2f} ± {cv_results['std_mae']:.2f}")

    print("\nTop 10 Feature Importances:")
    importance = predictor.get_feature_importance(10)
    for feat, imp in importance.items():
        print(f"  {feat}: {imp:.4f}")

    print("\nSaving model and preprocessor...")
    os.makedirs('models', exist_ok=True)

    predictor.save('models/shelf_life_predictor.pkl')
    preprocessor.save('models/preprocessor.pkl')

    print("Model saved successfully!")

    return predictor, preprocessor, feature_engineer


if __name__ == '__main__':
    train_model()
