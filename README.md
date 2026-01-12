# VocalGuard 🛡️

AI-powered Anti-Scam Call Defense System. Built with Vue.js, Python Flask, OpenAI, and ElevenLabs for Nexora Hacks 2026.

## Features

✨ **iPhone-style Call Simulation UI** - Realistic call interface with real-time scam detection
🤖 **AI-Powered Analysis** - Uses OpenAI GPT-4 to detect scam patterns and threats
🔒 **PII Redaction** - Automatically redacts credit cards, SSN, and other sensitive data
🎯 **Threat Detection** - Identifies urgency tactics, impersonation, payment requests, and more
🔊 **Audio Warnings** - Generates spoken alerts using ElevenLabs text-to-speech
🔐 **Privacy Toggle** - Blur numbers in transcripts for added privacy

## Project Structure

```
VocalGuard/
├── backend/
│   ├── app.py              # Flask API with /analyze endpoint
│   ├── scam_detector.py    # PII redaction and threat detection
│   └── .env.example        # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── CallScreen.vue   # iPhone-style call UI
│   │   ├── App.vue
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
└── requirements.txt        # Python dependencies
```

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your API keys
   ```

3. **Get API Keys**:
   - OpenAI API Key: https://platform.openai.com/api-keys
   - ElevenLabs API Key: https://elevenlabs.io/

4. **Run the backend**:
   ```bash
   cd backend
   python app.py
   ```
   
   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Run the development server**:
   ```bash
   npm run dev
   ```
   
   The frontend will run on `http://localhost:3000`

3. **Build for production**:
   ```bash
   npm run build
   ```

## Usage

1. Open the frontend at `http://localhost:3000`
2. The call screen displays an iPhone-style interface with a demo scam transcript
3. Click **"Analyze Call for Scams"** to analyze the transcript
4. The system will:
   - Detect PII and redact sensitive information
   - Analyze the transcript using OpenAI for scam patterns
   - Flag threats using keyword detection
   - Display a scam alert with confidence level and detected threats
5. Use the **"Blur Numbers"** toggle to hide digits in the transcript for privacy

## API Endpoints

### `POST /analyze`

Analyze a call transcript for scam detection.

**Request Body**:
```json
{
  "transcript": "Call transcript text",
  "generate_audio": true
}
```

**Response**:
```json
{
  "is_scam": true,
  "confidence": 0.95,
  "threat_level": "HIGH",
  "detected_threats": ["urgency", "payment", "personal_info"],
  "redacted_transcript": "Text with [CREDIT CARD REDACTED]",
  "detected_pii": ["credit_card", "phone"],
  "warning_message": "⚠️ HIGH RISK SCAM DETECTED!...",
  "audio_url": "/audio/warning.mp3"
}
```

### `GET /health`

Health check endpoint.

## Technologies Used

### Backend
- **Python 3.x** - Programming language
- **Flask** - Web framework
- **OpenAI GPT-4** - AI-powered scam detection
- **ElevenLabs** - Text-to-speech for audio warnings
- **Regular Expressions** - PII pattern matching

### Frontend
- **Vue.js 3** - JavaScript framework
- **Tailwind CSS** - Utility-first CSS framework
- **Vite** - Build tool and dev server

## Security Features

- **Credit Card Redaction** - Detects and redacts card numbers (e.g., 4532-1234-5678-9012)
- **SSN Protection** - Identifies and redacts social security numbers
- **Phone Number Privacy** - Redacts phone numbers from transcripts
- **Email Masking** - Removes email addresses
- **Privacy Toggle** - Allows users to blur all numbers in the UI

## Threat Detection Categories

- **Urgency** - Pressure tactics and time-sensitive demands
- **Payment** - Requests for wire transfers, gift cards, cryptocurrency
- **Personal Info** - Requests for SSN, passwords, account numbers
- **Impersonation** - Claims to be IRS, police, tech support, etc.
- **Threats** - Mentions of arrest, lawsuits, frozen accounts
- **Too Good to Be True** - Lottery wins, prizes, inheritance claims

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Style
- Backend follows PEP 8 Python style guide
- Frontend uses ESLint with Vue.js recommended rules

## License

MIT License - Built for Nexora Hacks 2026

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss proposed changes.

## Acknowledgments

- OpenAI for GPT-4 API
- ElevenLabs for text-to-speech technology
- Vue.js and Tailwind CSS communities
