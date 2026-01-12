# VocalGuard Project Structure

## Directory Layout

```
VocalGuard/
├── README.md                    # Main documentation
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── backend/                     # Python Flask backend
│   ├── app.py                   # Main Flask application
│   ├── scam_detector.py         # PII redaction & threat detection
│   └── .env.example             # Environment variables template
│
└── frontend/                    # Vue.js + Tailwind frontend
    ├── public/                  # Static assets
    ├── src/
    │   ├── components/
    │   │   └── CallScreen.vue   # iPhone-style call simulation UI
    │   ├── assets/              # Images, icons, etc.
    │   ├── App.vue              # Root Vue component
    │   ├── main.js              # Application entry point
    │   └── style.css            # Tailwind CSS imports
    ├── index.html               # HTML entry point
    ├── package.json             # Node.js dependencies
    ├── vite.config.js           # Vite configuration
    ├── tailwind.config.js       # Tailwind CSS configuration
    └── postcss.config.js        # PostCSS configuration
```

## File Descriptions

### Backend Files

#### `backend/app.py`
- Main Flask application with CORS enabled
- `/health` - Health check endpoint
- `/analyze` - Main endpoint for scam detection
  - Accepts transcript and optional generate_audio flag
  - Returns scam analysis with confidence, threats, and warnings
- `/audio/<filename>` - Serves generated audio warnings
- Integrates with OpenAI GPT-4 for AI-powered analysis
- Integrates with ElevenLabs for text-to-speech generation

#### `backend/scam_detector.py`
- `ScamDetector` class for local threat detection
- PII pattern matching (credit cards, SSN, phone, email, ZIP)
- Threat keyword detection across 6 categories:
  - urgency, payment, personal_info, impersonation, threats, too_good
- `redact_pii()` - Removes sensitive information from text
- `flag_threats()` - Detects scam patterns using keyword matching
- `redact_numbers_for_display()` - Privacy feature to blur numbers

#### `backend/.env.example`
- Template for environment variables
- Required: OPENAI_API_KEY, ELEVENLABS_API_KEY
- Optional: FLASK_ENV, PORT, ELEVENLABS_VOICE_ID

### Frontend Files

#### `frontend/src/components/CallScreen.vue`
- iPhone-style call screen component
- Features:
  - Status bar with time and signal indicators
  - Caller information display
  - Real-time call duration timer
  - Transcript display with scrolling
  - Privacy toggle to blur numbers
  - Scam alert badge (color-coded by threat level)
  - Detected threats chips
  - Call control buttons (mute, keypad, speaker)
  - End call button
  - Analyze call button
- Responsive and styled with Tailwind CSS
- Connects to backend API for analysis

#### `frontend/src/App.vue`
- Root Vue component
- Imports and displays CallScreen component
- Global styles

#### `frontend/src/main.js`
- Application entry point
- Creates and mounts Vue app
- Imports Tailwind CSS

#### `frontend/src/style.css`
- Tailwind CSS directives
- Imports base, components, and utilities

#### `frontend/index.html`
- HTML entry point
- Includes app div and module script

#### `frontend/package.json`
- Node.js project configuration
- Dependencies: vue
- Dev dependencies: vite, tailwindcss, autoprefixer, postcss
- Scripts: dev, build, preview

#### `frontend/vite.config.js`
- Vite build tool configuration
- Vue plugin setup
- Dev server on port 3000
- Proxy for backend API

#### `frontend/tailwind.config.js`
- Tailwind CSS configuration
- Content paths for Vue files
- Theme extensions (none by default)

#### `frontend/postcss.config.js`
- PostCSS configuration
- Tailwind CSS and Autoprefixer plugins

### Root Files

#### `requirements.txt`
- Python dependencies for backend
- Flask, flask-cors, openai, requests, python-dotenv, gunicorn
- Testing: pytest, pytest-flask, pytest-cov

#### `.gitignore`
- Python bytecode and cache files
- Virtual environments
- Node modules
- Build artifacts
- Environment files
- IDE-specific files

## Quick Start Commands

### Backend
```bash
pip install -r requirements.txt
cd backend
cp .env.example .env
# Edit .env with your API keys
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Integration Flow

1. User interacts with CallScreen.vue
2. Click "Analyze Call" triggers analyzeCall()
3. Frontend sends POST to http://localhost:5000/analyze
4. Backend app.py receives request
5. scam_detector.py redacts PII
6. OpenAI analyzes transcript
7. Local threat detection runs
8. Results combined and formatted
9. Optional audio generation via ElevenLabs
10. Response sent back to frontend
11. CallScreen.vue displays results

## Environment Variables

### Backend (.env)
- `FLASK_ENV` - development or production
- `PORT` - Server port (default: 5000)
- `OPENAI_API_KEY` - Required for AI analysis
- `ELEVENLABS_API_KEY` - Required for audio generation
- `ELEVENLABS_VOICE_ID` - Optional voice selection

### Frontend
- No environment variables required
- Backend URL hardcoded to localhost:5000 for dev
- Can be configured via vite.config.js proxy settings

## Deployment Considerations

### Backend
- Use gunicorn for production WSGI server
- Set FLASK_ENV=production
- Configure proper CORS origins
- Store audio files in CDN/S3 instead of temp directory
- Add rate limiting for API endpoints
- Implement API key authentication

### Frontend
- Run `npm run build` to create production bundle
- Serve static files from dist/ directory
- Update backend API URL for production
- Enable HTTPS
- Configure CDN for assets

## Testing Strategy

### Backend Testing
- Unit tests for scam_detector.py functions
- Integration tests for API endpoints
- Mock OpenAI and ElevenLabs API calls
- Test PII redaction patterns
- Test threat detection accuracy

### Frontend Testing
- Component tests for CallScreen.vue
- Test user interactions (buttons, toggles)
- Test API integration
- Test privacy mode functionality
- Visual regression testing for UI

## Security Notes

- Never commit .env files (included in .gitignore)
- API keys should be stored in environment variables
- PII is redacted before storage/logging
- CORS should be configured for production domains
- Input validation on all API endpoints
- Rate limiting to prevent abuse
- HTTPS required for production
