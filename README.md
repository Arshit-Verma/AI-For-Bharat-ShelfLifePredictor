# AI Food Shelf Life Predictor

An end-to-end AI system that predicts the remaining shelf life of food items using machine learning, with a user-friendly multi-tab UI featuring voice explanations and chat assistance.

## Features

- **ML-Based Prediction**: Random Forest Regressor trained on food storage data
- **Smart Preprocessing**: Handles missing values, encoding, and scaling
- **Feature Engineering**: Environment-food interaction features and degradation indicators
- **Rule-Based Interpretation**: Adjusts predictions under extreme conditions
- **Safety Classifications**: Safe / Consume Soon / Expired
- **Multi-Tab UI**:
  - Prediction Results Tab: Real-time shelf life predictions with recommendations
  - Voice Agent Tab: AI-powered voice explanations using ElevenLabs API
  - Chat Assistant Tab: Storage and safety Q&A using OpenRouter API

## Project Structure

```
Ai-for-Bharat/
├── backend/
│   ├── data/
│   │   └── food_shelf_life.csv          # Training dataset
│   ├── models/                          # Trained models and preprocessors
│   ├── src/
│   │   ├── preprocessing/
│   │   │   └── preprocessor.py         # Data preprocessing pipeline
│   │   ├── feature_engineering/
│   │   │   └── engineer.py             # Feature engineering module
│   │   ├── models/
│   │   │   └── predictor.py             # Random Forest predictor
│   │   ├── inference/
│   │   │   └── pipeline.py              # Inference pipeline
│   │   ├── rules/
│   │   │   └── interpreter.py           # Rule-based interpretation
│   │   └── services/
│   │       ├── voice_service.py         # ElevenLabs integration
│   │       └── chat_service.py          # OpenRouter integration
│   ├── train.py                         # Model training script
│   ├── api.py                           # Flask API server
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx                # Main multi-tab UI
│   │   │   └── globals.css
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   │   └── api.ts                  # API client
│   │   └── hooks/
│   │       └── usePrediction.ts        # Prediction hook
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── next.config.js
└── config/
    └── .env.example
```

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   cd ../config
   cp .env.example .env
   ```
   Edit `.env` with your API keys:
   - `ELEVENLABS_API_KEY`: Your ElevenLabs API key for voice features
   - `OPENROUTER_API_KEY`: Your OpenRouter API key for chat features

3. **Train the model**:
   ```bash
   cd ../backend
   python train.py
   ```
   This will:
   - Load the training data
   - Train the Random Forest model
   - Save the model and preprocessor to `backend/models/`

4. **Start the API server**:
   ```bash
   python api.py
   ```
   The API will run on `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```
   The UI will be available at `http://localhost:3000`

## Usage

### 1. Prediction Tab
- Enter food details (food type, storage type, temperature, humidity, days stored)
- Click "Predict Shelf Life"
- View results including:
  - Predicted remaining days
  - Safety classification (Safe / Consume Soon / Expired)
  - Detected issues (if any)
  - Recommendations
- Listen to voice explanation (ElevenLabs)

### 2. Voice Agent Tab
- Configure food parameters
- Click "Play Voice Explanation"
- Receive AI-generated spoken explanation of the prediction
- Requires ElevenLabs API key

### 3. Chat Assistant Tab
- Ask questions about food storage, safety, and best practices
- Get context-aware responses based on your recent predictions
- Requires OpenRouter API key

## Model Performance

The Random Forest model achieves:
- **Mean Absolute Error**: ~0.8 days
- **R² Score**: ~0.95
- **Cross-validated MAE**: ~1.0 ± 0.2 days

## Key Features Explained

### Data Preprocessing
- Missing value imputation using median strategy
- Label encoding for categorical variables
- Standard scaling for numerical features

### Feature Engineering
- **Base shelf life**: Expected shelf life based on food and storage type
- **Temperature deviation**: How far current temp is from ideal
- **Humidity deviation**: How far current humidity is from ideal
- **Storage progress**: Ratio of days stored to expected shelf life
- **Degradation factor**: Combined metric of environmental stress
- **Temperature-humidity interaction**: Combined effect of temp and humidity
- **Extreme condition flags**: Binary flags for dangerous conditions

### Rule-Based Interpretation
- Adjusts predictions based on extreme conditions
- Provides safety recommendations
- Generates human-readable explanations
- Handles edge cases beyond ML model capabilities

### Inference Pipeline
1. Preprocess input data
2. Engineer features
3. Generate ML prediction
4. Apply rule-based adjustments
5. Classify safety status
6. Generate recommendations
7. Return comprehensive result

## API Endpoints

- `GET /health` - Health check
- `POST /predict` - Get shelf life prediction
- `POST /explain` - Get detailed explanation
- `POST /batch_predict` - Batch predictions
- `POST /voice/explain` - Get voice explanation (audio)
- `POST /chat` - Chat with AI assistant
- `POST /chat/prediction_explanation` - Get AI explanation of prediction
- `POST /chat/storage_advice` - Get storage advice for food type

## API Integration

### ElevenLabs (Voice)
- Used for generating spoken explanations
- API endpoint: `https://api.elevenlabs.io/v1/text-to-speech`
- Model: `eleven_monolingual_v1`

### OpenRouter (Chat)
- Used for AI-powered Q&A
- API endpoint: `https://openrouter.ai/api/v1/chat/completions`
- Model: `anthropic/claude-3-haiku`

## Notes

- The system uses dynamic, condition-aware predictions rather than fixed expiry dates
- Extreme conditions trigger rule-based adjustments
- Safety is prioritized - when in doubt, the system recommends caution
- The modular architecture allows easy extension and customization

## License

MIT License
