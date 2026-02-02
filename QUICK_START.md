# Quick Start Guide

## Prerequisites
- Python 3.9+
- Node.js 18+
- ElevenLabs API key (optional - for voice features)
- OpenRouter API key (optional - for chat features)

## Step 1: Start Backend

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies (if not already done)
pip install -r requirements.txt

# Configure API keys (optional)
cd ../config
cp .env.example .env
# Edit .env and add your actual API keys

# Start the API server
cd ../backend
python3 api.py
```

Backend will run on: **http://localhost:5001**

## Step 2: Start Frontend

Open a **new terminal**:

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

Frontend will run on: **http://localhost:3000**

## Step 3: Use the Application

### Tab 1: Prediction
1. Select food type (dairy, meat, vegetables, fruits, bakery, seafood)
2. Select storage type (refrigerator, freezer, pantry)
3. Enter temperature in °C
4. Enter humidity percentage
5. Enter days already stored
6. Click "Predict Shelf Life"
7. View results and recommendations

### Tab 2: Voice Agent
1. Configure food parameters
2. Click "Play Voice Explanation"
3. Listen to AI-generated explanation (requires ElevenLabs API key)

### Tab 3: Chat Assistant
1. Ask questions about food storage, safety, or your prediction
2. Get context-aware responses (requires OpenRouter API key)

## Testing Without API Keys

The **prediction features work perfectly without API keys**. Only the voice and chat features require:
- ElevenLabs API key for voice explanations
- OpenRouter API key for chat assistance

## Example Test

Try this in the Prediction tab:
- Food Type: Dairy
- Storage Type: Refrigerator
- Temperature: 4
- Humidity: 65
- Days Stored: 2

Expected result: ~2-3 days remaining, Safe status

## Troubleshooting

**Backend won't start?**
- Check if port 5001 is already in use
- Try using a different port by modifying `api.py`

**Frontend won't start?**
- Check if port 3000 is already in use
- Ensure `npm install` completed successfully

**Prediction not working?**
- Ensure backend is running
- Check browser console for errors
- Verify API server is healthy: `curl http://localhost:5001/health`

## Full Documentation

See `README.md` for comprehensive documentation and `SYSTEM_SUMMARY.md` for detailed technical information.
