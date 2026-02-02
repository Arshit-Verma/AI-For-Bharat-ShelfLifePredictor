# File Locations & Key Components

## Core Backend Files

### 1. Data Processing
**Location**: `backend/src/preprocessing/preprocessor.py`
**Purpose**: Handles missing values, encoding, and scaling
**Key Methods**:
- `fit(X)` - Learn preprocessing parameters
- `transform(X)` - Apply preprocessing
- `fit_transform(X)` - Fit and transform in one step
- `save(filepath)` - Save preprocessor state
- `load(filepath)` - Load preprocessor state

### 2. Feature Engineering
**Location**: `backend/src/feature_engineering/engineer.py`
**Purpose**: Creates interaction features and degradation indicators
**Key Features**:
- `base_shelf_life` - Expected shelf life for food-storage combo
- `temp_deviation` - Distance from ideal temperature
- `humidity_deviation` - Distance from ideal humidity
- `storage_progress` - Days stored / expected shelf life
- `degradation_factor` - Combined environmental stress
- `temp_humidity_interaction` - Combined effect metric
- `is_extreme_temp` - Binary flag for dangerous temperatures
- `is_extreme_humidity` - Binary flag for dangerous humidity
- `days_remaining_ratio` - Ratio of remaining to total shelf life

### 3. ML Model
**Location**: `backend/src/models/predictor.py`
**Purpose**: Random Forest Regressor with hyperparameter tuning
**Key Methods**:
- `train(X_train, y_train)` - Train the model
- `predict(X)` - Make predictions
- `evaluate(X_test, y_test)` - Calculate metrics (MAE, RMSE, R²)
- `cross_validate(X, y, cv=5)` - 5-fold cross-validation
- `hyperparameter_tune(X_train, y_train)` - Grid search for best params
- `get_feature_importance(top_n=10)` - Get most important features
- `save(filepath)` - Save trained model
- `load(filepath)` - Load trained model

**Model Performance**:
- MAE: ~0.8 days
- R²: ~0.95
- CV MAE: ~1.0 ± 0.2 days

### 4. Rule-Based Interpreter
**Location**: `backend/src/rules/interpreter.py`
**Purpose**: Adjust predictions based on extreme conditions
**Key Methods**:
- `check_extreme_conditions(food_type, storage_type, temp, humidity, days_stored)` - Detect issues
- `adjust_prediction(predicted_days, issues, severity, days_stored)` - Apply rule adjustments
- `classify_safety(remaining_days, days_stored, issues)` - Determine safety status
- `get_recommendations(food_type, storage_type, temp, humidity, remaining_days)` - Generate advice

**Adjustment Factors**:
- Critical severity: 30% of original prediction
- High severity: 50% of original prediction
- Medium severity: 70% of original prediction
- None: 100% of original prediction

### 5. Inference Pipeline
**Location**: `backend/src/inference/pipeline.py`
**Purpose**: Orchestrates the complete prediction workflow
**Key Methods**:
- `predict(input_data)` - Single or batch predictions
- `predict_single(food_type, temperature, humidity, storage_type, days_stored)` - Convenience method
- `explain_prediction(result)` - Generate human-readable explanation

**Workflow**:
1. Preprocess input data
2. Engineer features
3. Generate ML prediction
4. Apply rule-based adjustments
5. Classify safety status
6. Generate recommendations
7. Return comprehensive result

### 6. Flask API
**Location**: `backend/api.py`
**Purpose**: HTTP API for frontend communication
**Endpoints**:
- `GET /health` - Health check
- `POST /predict` - Single prediction
- `POST /explain` - Detailed prediction with explanation
- `POST /batch_predict` - Multiple predictions
- `POST /voice/explain` - Audio explanation
- `POST /chat` - Chat with AI assistant
- `POST /chat/prediction_explanation` - AI analysis of prediction
- `POST /chat/storage_advice` - Storage recommendations

**Port**: 5001 (updated from default 5000)

### 7. Training Script
**Location**: `backend/train.py`
**Purpose**: Train and save the model
**Usage**:
```bash
cd backend
python3 train.py
```

### 8. Voice Service
**Location**: `backend/src/services/voice_service.py`
**Purpose**: ElevenLabs API integration for voice explanations
**Key Methods**:
- `text_to_speech(text, voice_id=None)` - Convert text to audio
- `generate_explanation_audio(prediction_result)` - Generate voice explanation
- `get_available_voices()` - List available voices

**Default Voice**: `21m00Tcm4TlvDq8ikWAM`

### 9. Chat Service
**Location**: `backend/src/services/chat_service.py`
**Purpose**: OpenRouter API integration for AI chat
**Key Methods**:
- `chat(message, context=None)` - General chat
- `get_prediction_explanation(prediction_result)` - AI analysis of prediction
- `get_storage_advice(food_type, storage_conditions)` - Storage recommendations
- `get_safety_guidelines(food_type)` - Safety information

**Model**: `anthropic/claude-3-haiku`

## Core Frontend Files

### 1. Main Page (Multi-Tab UI)
**Location**: `frontend/src/app/page.tsx`
**Purpose**: Main application with three tabs
**Components**:
- Tab 1: Prediction form and results
- Tab 2: Voice agent interface
- Tab 3: Chat assistant interface

**Key Features**:
- Food type selector (dairy, meat, vegetables, fruits, bakery, seafood)
- Storage type selector (refrigerator, freezer, pantry)
- Temperature input with Thermometer icon
- Humidity input with Droplets icon
- Days stored input with Clock icon
- Safety classification badges (Safe/Consume Soon/Expired)
- Issue detection and display
- Recommendations list
- Feature importance visualization
- Voice explanation button
- Chat interface with message history

### 2. API Client
**Location**: `frontend/src/services/api.ts`
**Purpose**: HTTP client for backend communication
**Methods**:
- `healthCheck()` - Check API status
- `predict(input)` - Get shelf life prediction
- `explain(input)` - Get detailed explanation
- `getVoiceExplanation(input)` - Get audio explanation (returns Blob)
- `chat(message, context)` - Send chat message
- `getPredictionExplanation(input)` - Get AI prediction analysis
- `getStorageAdvice(food_type, storage_conditions)` - Get storage recommendations

**Base URL**: `/api` (rewrites to `http://localhost:5001`)

### 3. Prediction Hook
**Location**: `frontend/src/hooks/usePrediction.ts`
**Purpose**: Custom React hook for predictions
**Returns**:
- `result` - Prediction result object
- `loading` - Loading state
- `error` - Error message (if any)
- `predict` - Function to trigger prediction
- `setResult` - Function to set result

### 4. Layout
**Location**: `frontend/src/app/layout.tsx`
**Purpose**: Root layout component
**Features**:
- Google Fonts (Inter)
- Metadata configuration
- Page structure

### 5. Global Styles
**Location**: `frontend/src/app/globals.css`
**Purpose**: Global CSS with Tailwind
**Features**:
- Tailwind directives
- Custom color variables
- Gradient background

## Configuration Files

### 1. Environment Variables
**Location**: `config/.env`
**Variables**:
```
ELEVENLABS_API_KEY=your_key_here
OPENROUTER_API_KEY=your_key_here
FLASK_ENV=development
FLASK_PORT=5001
```

**Example**: `config/.env.example`

### 2. Backend Requirements
**Location**: `backend/requirements.txt`
**Dependencies**:
- pandas==2.1.4
- numpy==1.26.2
- scikit-learn==1.3.2
- joblib==1.3.2
- flask==3.0.0
- flask-cors==4.0.0
- requests==2.31.0
- python-dotenv==1.0.0

### 3. Frontend Package
**Location**: `frontend/package.json`
**Dependencies**:
- next==14.0.4
- react==18.2.0
- react-dom==18.2.0
- axios==1.6.2
- lucide-react==0.294.0
- clsx==2.0.0
- tailwind-merge==2.1.0

### 4. Next.js Config
**Location**: `frontend/next.config.js`
**Key Setting**: API rewrite to port 5001

### 5. Tailwind Config
**Location**: `frontend/tailwind.config.js`
**Content**: Tailwind CSS configuration

### 6. TypeScript Config
**Location**: `frontend/tsconfig.json`
**Content**: TypeScript compiler options

## Data Files

### 1. Training Dataset
**Location**: `backend/data/food_shelf_life.csv`
**Columns**:
- food_type (categorical: dairy, meat, vegetables, fruits, bakery, seafood)
- temperature (numerical: °C)
- humidity (numerical: %)
- storage_type (categorical: refrigerator, freezer, pantry)
- days_stored (numerical)
- remaining_shelf_life (numerical - target variable)

**Size**: 1000+ samples

### 2. Trained Models
**Location**: `backend/models/`
**Files**:
- `shelf_life_predictor.pkl` - Random Forest model (472 KB)
- `preprocessor.pkl` - Fitted preprocessor (2.4 KB)

## Key Code Patterns

### Preprocessing Pattern
```python
preprocessor = DataPreprocessor()
X_processed = preprocessor.fit_transform(X)
preprocessor.save('models/preprocessor.pkl')
```

### Training Pattern
```python
predictor = ShelfLifePredictor()
best_params = predictor.hyperparameter_tune(X_train, y_train)
metrics = predictor.evaluate(X_test, y_test)
predictor.save('models/shelf_life_predictor.pkl')
```

### Inference Pattern
```python
preprocessor = DataPreprocessor().load('models/preprocessor.pkl')
model = ShelfLifePredictor().load('models/shelf_life_predictor.pkl')
feature_engineer = FeatureEngineer()
rule_interpreter = RuleBasedInterpreter()

pipeline = InferencePipeline(preprocessor, feature_engineer, model, rule_interpreter)
result = pipeline.predict_single(food_type, temperature, humidity, storage_type, days_stored)
```

### API Call Pattern (Frontend)
```typescript
const result = await api.predict({
  food_type: 'dairy',
  temperature: 4,
  humidity: 65,
  storage_type: 'refrigerator',
  days_stored: 2
});
```

## Testing

### Backend Tests
```bash
# Health check
curl http://localhost:5001/health

# Prediction
curl -X POST http://localhost:5001/predict \
  -H "Content-Type: application/json" \
  -d '{"food_type":"dairy","temperature":4,"humidity":65,"storage_type":"refrigerator","days_stored":2}'
```

### Frontend Tests
1. Open browser to http://localhost:3000
2. Navigate to Prediction tab
3. Enter food details
4. Click "Predict Shelf Life"
5. Verify results display correctly

## Troubleshooting

### Common Issues

**Port already in use**:
- Backend: Change port in `api.py` or kill process on port 5001
- Frontend: Kill process on port 3000

**Model not found**:
- Ensure `train.py` has been run
- Check `backend/models/` directory exists with .pkl files

**API connection errors**:
- Verify backend is running
- Check browser console for CORS errors
- Ensure API rewrite in `next.config.js` points to correct port

**Predictions not working**:
- Check backend logs for errors
- Verify data types match expected formats
- Test with curl command directly

## Deployment Notes

### Backend Deployment
- Use production WSGI server (Gunicorn, uWSGI)
- Set `FLASK_ENV=production`
- Use environment variables for API keys
- Enable HTTPS for API endpoints

### Frontend Deployment
- Run `npm run build` to create production build
- Deploy to Vercel, Netlify, or similar
- Update API URL in production environment
- Enable HTTPS

### Security Considerations
- Never commit `.env` file with actual API keys
- Use environment variables for all sensitive data
- Implement rate limiting for API endpoints
- Validate all user inputs
- Sanitize outputs to prevent XSS
