"""
VocalGuard Backend API - Advanced Scam Detection
Flask application with advanced pattern analysis and database storage
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests
from scam_detector import ScamDetector
from database import VocalGuardDB
from advanced_detector import AdvancedScamDetector
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

# Initialize scam detectors
scam_detector = ScamDetector()
advanced_detector = AdvancedScamDetector()
db = VocalGuardDB()

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
        "risk_score": float (0-100),
        "insights": object with detailed analysis
    }
    """
    try:
        data = request.json
        transcript = data.get('transcript', '')
        caller_name = data.get('caller_name', 'Unknown')
        caller_number = data.get('caller_number', 'Unknown')
        generate_audio = data.get('generate_audio', False)
        
        if not transcript:
            return jsonify({'error': 'Transcript is required'}), 400
        
        # Step 1: Detect language
        detected_language = advanced_detector.detect_language(transcript)
        
        # Step 2: Advanced risk analysis
        risk_score, detected_patterns, threat_level = advanced_detector.calculate_risk_score(transcript)
        
        # Step 3: Detect and redact PII
        redacted_result = scam_detector.redact_pii(transcript)
        redacted_transcript = redacted_result['redacted_text']
        detected_pii = redacted_result['pii_found']
        
        # Step 4: Generate insights
        insights = advanced_detector.generate_insights(transcript, risk_score, threat_level)
        
        # Step 5: Determine if scam based on risk score
        is_scam = risk_score >= 40
        confidence = risk_score / 100.0
        
        # Generate warning message
        warning_message = generate_warning_message(is_scam, threat_level, detected_patterns)
        
        result = {
            'is_scam': is_scam,
            'confidence': confidence,
            'risk_score': round(risk_score, 2),
            'threat_level': threat_level,
            'detected_threats': detected_patterns,
            'redacted_transcript': redacted_transcript,
            'detected_pii': detected_pii,
            'warning_message': warning_message,
            'detected_language': detected_language,
            'insights': insights
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


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get overall statistics from database"""
    try:
        stats = db.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calls/history', methods=['GET'])
def get_call_history():
    """Get call history from database"""
    try:
        limit = request.args.get('limit', 50, type=int)
        calls = db.get_all_calls(limit=limit)
        return jsonify({'calls': calls, 'total': len(calls)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calls/search', methods=['POST'])
def search_calls():
    """Search calls in database"""
    try:
        data = request.json
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        calls = db.search_calls(query)
        return jsonify({'calls': calls, 'total': len(calls)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/generate', methods=['POST'])
def generate_report():
    """Generate a detailed report for a call"""
    try:
        data = request.json
        call_id = data.get('call_id')
        
        if not call_id:
            return jsonify({'error': 'Call ID required'}), 400
        
        # Get call data
        calls = db.get_all_calls(limit=999)
        call = next((c for c in calls if c['id'] == call_id), None)
        
        if not call:
            return jsonify({'error': 'Call not found'}), 404
        
        # Generate comprehensive report
        report = {
            'call_id': call['id'],
            'timestamp': call['timestamp'],
            'caller_info': {
                'name': call['caller_name'],
                'number': call['caller_number'],
                'duration': call['duration']
            },
            'analysis': {
                'is_scam': call['is_scam'],
                'confidence': call['confidence'],
                'threat_level': call['threat_level'],
                'detected_threats': call['detected_threats'],
                'risk_indicators': call['warning_message']
            },
            'protection': {
                'pii_detected': call['detected_pii'],
                'redacted_transcript': call['redacted_transcript'],
                'recommended_action': 'Block number and report to FTC' if call['is_scam'] else 'No action needed'
            },
            'tips': [
                'Never share personal information over the phone',
                'Verify caller identity independently',
                'Hang up and call official numbers',
                'Report suspicious calls to authorities'
            ]
        }
        
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
