# VocalGuard Quick Start Guide

## Prerequisites

- Python 3.8+ installed
- Node.js 16+ and npm installed
- OpenAI API key (get from https://platform.openai.com/api-keys)
- ElevenLabs API key (optional, for audio - get from https://elevenlabs.io/)

## Setup Instructions

### Step 1: Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cd backend
cp .env.example .env

# Edit .env file and add your API keys:
# OPENAI_API_KEY=your_actual_key_here
# ELEVENLABS_API_KEY=your_actual_key_here
```

### Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### Step 3: Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
python app.py
```
Output: `Running on http://0.0.0.0:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Output: `Local: http://localhost:3000`

### Step 4: Access the Application

Open your browser and navigate to: http://localhost:3000

## Testing Without API Keys

You can test the PII redaction and threat detection locally without API keys:

```bash
python3 test_vocalguard.py
```

This will run tests showing:
- PII redaction (credit cards, SSN, phone numbers, emails)
- Threat detection (urgency, payment, impersonation, threats)
- Privacy mode (number blurring)

## Using the Application

1. **Call Screen Interface**: The app loads with an iPhone-style call screen
2. **Demo Transcript**: A sample scam call transcript is pre-loaded
3. **Analyze Call**: Click the "Analyze Call for Scams" button
4. **View Results**: See scam detection results with:
   - Threat level (HIGH/MEDIUM/LOW)
   - Confidence score
   - Detected threat categories
   - Warning message
5. **Privacy Toggle**: Click "Blur Numbers" to hide digits in the transcript
6. **End Call**: Click the red phone button to end the simulation

## API Testing with cURL

Test the backend API directly:

```bash
# Health check
curl http://localhost:5000/health

# Analyze a transcript
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "This is the IRS. You owe $5000. Pay immediately with gift cards or face arrest.",
    "generate_audio": false
  }'
```

## Features Demonstrated

### 1. iPhone-style UI
- Realistic call screen design
- Status bar with time
- Call duration timer
- Control buttons (mute, keypad, speaker)
- End call button

### 2. Scam Detection
- **OpenAI Integration**: AI-powered analysis
- **Local Threat Detection**: Keyword-based pattern matching
- **Combined Analysis**: Merges both results for accuracy

### 3. PII Protection
- **Credit Card Redaction**: Detects 16-digit card numbers
- **SSN Redaction**: Identifies social security numbers
- **Phone Redaction**: Masks phone numbers
- **Email Redaction**: Hides email addresses
- **ZIP Code Redaction**: Removes postal codes

### 4. Threat Categories
- **Urgency**: Time pressure tactics
- **Payment**: Gift cards, wire transfers, cryptocurrency
- **Personal Info**: Requests for sensitive data
- **Impersonation**: Claims to be IRS, police, tech support
- **Threats**: Arrest, lawsuits, account freezing
- **Too Good to Be True**: Lottery wins, prizes

### 5. Privacy Features
- Toggle to blur all numbers in transcript
- Client-side number masking
- No data persistence (privacy-first design)

### 6. Audio Warnings (Optional)
- Text-to-speech via ElevenLabs
- Spoken alerts for high-risk scams
- Customizable voice settings

## Troubleshooting

### Backend Issues

**Error: "OpenAI API key not found"**
- Ensure you've created `.env` file from `.env.example`
- Add your actual OpenAI API key to `.env`
- Restart the backend server

**Error: "Module not found"**
- Run: `pip install -r requirements.txt`
- Ensure you're in the correct directory

### Frontend Issues

**Error: "Failed to fetch"**
- Ensure backend is running on http://localhost:5000
- Check browser console for CORS errors
- Verify backend server is accessible

**Error: "Module not found"**
- Run: `cd frontend && npm install`
- Delete `node_modules` and reinstall if issues persist

### Port Conflicts

**Backend port 5000 already in use:**
```bash
# Change port in backend/.env
PORT=5001

# Update frontend/src/components/CallScreen.vue
# Change fetch URL from localhost:5000 to localhost:5001
```

**Frontend port 3000 already in use:**
```bash
# Change port in frontend/vite.config.js
server: { port: 3001 }
```

## Production Deployment

### Backend
```bash
# Use gunicorn for production
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```bash
# Build for production
cd frontend
npm run build

# Serve the dist/ directory with any static file server
# Example with Python:
cd dist
python -m http.server 3000
```

## Project Structure

```
VocalGuard/
├── backend/           # Flask API
│   ├── app.py        # Main API endpoints
│   └── scam_detector.py  # Detection logic
├── frontend/         # Vue.js app
│   └── src/
│       └── components/
│           └── CallScreen.vue  # Main UI
├── requirements.txt  # Python deps
└── README.md         # Documentation
```

## Next Steps

1. Customize the call screen UI
2. Add more threat detection patterns
3. Implement call recording integration
4. Add user authentication
5. Store analysis history
6. Create mobile app version
7. Add multi-language support

## Support

For issues or questions:
- Check the README.md for detailed documentation
- Review PROJECT_STRUCTURE.md for technical details
- Run test_vocalguard.py to verify setup

## Security Notes

- Never commit `.env` files with real API keys
- Keep API keys secure and rotate regularly
- PII is redacted before any logging/storage
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Add authentication for production use
