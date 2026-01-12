"""
VocalGuard Backend API
Flask application with OpenAI and ElevenLabs integration
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from scam_detector import ScamDetector
import tempfile
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize scam detector
scam_detector = ScamDetector()

# ElevenLabs API configuration
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL')  # Default voice


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'app': 'VocalGuard Backend API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            '/health': 'GET - Health check',
            '/analyze': 'POST - Analyze call transcript for scams'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})


@app.route('/analyze', methods=['POST'])
def analyze_call():
    """
    Analyze call transcript for scam detection
    
    Expected JSON payload:
    {
        "transcript": "Call transcript text",
        "generate_audio": true/false (optional)
    }
    
    Returns:
    {
        "is_scam": boolean,
        "confidence": float,
        "threat_level": string,
        "detected_threats": list,
        "redacted_transcript": string,
        "detected_pii": list,
        "warning_message": string,
        "audio_url": string (if generate_audio=true)
    }
    """
    try:
        data = request.json
        transcript = data.get('transcript', '')
        generate_audio = data.get('generate_audio', False)
        
        if not transcript:
            return jsonify({'error': 'Transcript is required'}), 400
        
        # Step 1: Detect and redact PII
        redacted_result = scam_detector.redact_pii(transcript)
        redacted_transcript = redacted_result['redacted_text']
        detected_pii = redacted_result['pii_found']
        
        # Step 2: Analyze transcript with OpenAI for scam detection
        scam_analysis = analyze_with_openai(transcript)
        
        # Step 3: Flag threats using local detection
        threat_analysis = scam_detector.flag_threats(transcript)
        
        # Combine analyses
        is_scam = scam_analysis['is_scam'] or threat_analysis['is_threat']
        confidence = max(scam_analysis['confidence'], threat_analysis['confidence'])
        
        # Determine threat level
        if confidence >= 0.8:
            threat_level = 'HIGH'
        elif confidence >= 0.5:
            threat_level = 'MEDIUM'
        else:
            threat_level = 'LOW'
        
        # Combine detected threats
        all_threats = list(set(scam_analysis['threats'] + threat_analysis['detected_patterns']))
        
        # Generate warning message
        warning_message = generate_warning_message(is_scam, threat_level, all_threats)
        
        result = {
            'is_scam': is_scam,
            'confidence': confidence,
            'threat_level': threat_level,
            'detected_threats': all_threats,
            'redacted_transcript': redacted_transcript,
            'detected_pii': detected_pii,
            'warning_message': warning_message
        }
        
        # Step 4: Generate audio warning if requested
        if generate_audio and is_scam:
            audio_url = generate_audio_warning(warning_message)
            result['audio_url'] = audio_url
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def analyze_with_openai(transcript):
    """
    Use OpenAI to analyze transcript for scam indicators
    """
    try:
        prompt = f"""Analyze the following phone call transcript for scam indicators.

Transcript: {transcript}

Identify if this appears to be a scam call. Look for:
- Urgency and pressure tactics
- Requests for personal information (SSN, passwords, credit cards)
- Impersonation of authority figures (IRS, police, tech support)
- Too-good-to-be-true offers
- Threats or intimidation
- Requests for immediate payment or wire transfers
- Poor grammar or unusual phrasing

Respond in JSON format with:
{{
  "is_scam": boolean,
  "confidence": float (0.0 to 1.0),
  "threats": list of detected threat types,
  "reasoning": brief explanation
}}"""

        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert at detecting phone scams and fraudulent calls. Analyze transcripts and provide accurate assessments."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"OpenAI analysis error: {e}")
        return {
            'is_scam': False,
            'confidence': 0.0,
            'threats': [],
            'reasoning': 'Analysis failed'
        }


def generate_warning_message(is_scam, threat_level, threats):
    """
    Generate a user-friendly warning message
    """
    if not is_scam:
        return "No scam indicators detected. Call appears legitimate."
    
    threat_descriptions = {
        'urgency': 'Pressure tactics detected',
        'personal_info': 'Request for personal information',
        'impersonation': 'Possible impersonation',
        'payment': 'Payment request detected',
        'threats': 'Threatening language',
        'too_good': 'Unrealistic offers'
    }
    
    threat_list = [threat_descriptions.get(t, t) for t in threats[:3]]
    
    if threat_level == 'HIGH':
        return f"⚠️ HIGH RISK SCAM DETECTED! This call shows multiple red flags: {', '.join(threat_list)}. DO NOT share personal information or make payments."
    elif threat_level == 'MEDIUM':
        return f"⚠️ Potential scam detected: {', '.join(threat_list)}. Exercise caution and verify the caller's identity."
    else:
        return f"⚠️ Some suspicious elements detected: {', '.join(threat_list)}. Stay vigilant."


def generate_audio_warning(warning_text):
    """
    Generate audio warning using ElevenLabs API
    """
    try:
        if not ELEVENLABS_API_KEY:
            return None
            
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        data = {
            "text": warning_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save audio to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_file.write(response.content)
            temp_file.close()
            
            # In production, you'd upload this to a CDN/storage
            # For now, return the local path
            return f"/audio/{os.path.basename(temp_file.name)}"
        
        return None
        
    except Exception as e:
        print(f"Audio generation error: {e}")
        return None


@app.route('/audio/<filename>', methods=['GET'])
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='audio/mpeg')
        
        return jsonify({'error': 'Audio file not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
