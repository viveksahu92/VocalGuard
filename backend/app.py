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
from voice_analyzer import VoiceAnalyzer
from caller_intelligence import CallerIntelligence
from spoofing_detector import SpoofingDetector
from threat_intelligence import ThreatIntelligence
import tempfile
from datetime import datetime

# Load environment variables (optional)
try:
    load_dotenv()
except:
    pass

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize OpenAI client (optional)
try:
    openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
except:
    openai_client = None

# Initialize scam detectors and new modules
scam_detector = ScamDetector()
advanced_detector = AdvancedScamDetector()
voice_analyzer = VoiceAnalyzer()
caller_intelligence = CallerIntelligence()
spoofing_detector = SpoofingDetector()
threat_intelligence = ThreatIntelligence()
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
    ENHANCED v2.0: Analyze call transcript with ALL NEW FEATURES
    
    Expected JSON payload:
    {
        "transcript": "Call transcript text",
        "caller_name": "Caller name",
        "caller_number": "Phone number",
        "generate_audio": true/false (optional)
    }
    
    Returns comprehensive analysis including:
    - Dynamic risk scoring
    - Voice pattern analysis
    - Caller reputation
    - Spoofing detection
    - Threat intelligence matching
    - Auto-disconnect recommendation
    """
    try:
        data = request.json
        transcript = data.get('transcript', '')
        caller_name = data.get('caller_name', 'Unknown')
        caller_number = data.get('caller_number', 'Unknown')
        generate_audio = data.get('generate_audio', False)
        call_time = datetime.now().isoformat()
        
        if not transcript:
            return jsonify({'error': 'Transcript is required'}), 400
        
        # === FEATURE 1: Dynamic Risk Scoring ===
        risk_score, detected_patterns, threat_level = advanced_detector.calculate_risk_score(
            transcript, caller_number, call_time
        )
        
        # === FEATURE 2: Voice Pattern Analysis ===
        voice_analysis = voice_analyzer.comprehensive_voice_analysis(transcript)
        risk_score += voice_analysis['total_voice_risk_score']
        
        # === FEATURE 3: Caller Reputation Check ===
        reputation_data = caller_intelligence.check_number_reputation(caller_number)
        risk_score += reputation_data['risk_modifier']
        
        # === FEATURE 4: Threat Intelligence Matching ===
        threat_match = threat_intelligence.match_emerging_patterns(transcript)
        risk_score += threat_match['total_emerging_threat_risk']
        
        # === FEATURE 5 & 6: Robocall & Spoofing Detection ===
        spoofing_analysis = spoofing_detector.calculate_spoofing_probability(
            caller_number, caller_name
        )
        risk_score += spoofing_analysis['total_spoofing_risk_score']
        
        # === FEATURE 7: Time-based assessment (already in calculate_risk_score) ===
        
        # === FEATURE 8: Industry-specific detection ===
        scam_category = detect_scam_category(detected_patterns, transcript)
        
        # Cap final risk score at 100
        risk_score = min(risk_score, 100)
        
        # Redetermine threat level with enhanced score
        if risk_score >= 70:
            threat_level = 'HIGH'
        elif risk_score >= 40:
            threat_level = 'MEDIUM'
        else:
            threat_level = 'LOW'
        
        # === Standard PII detection ===
        redacted_result = scam_detector.redact_pii(transcript)
        redacted_transcript = redacted_result['redacted_text']
        detected_pii = redacted_result['pii_found']
        
        # === Language detection ===
        detected_language = advanced_detector.detect_language(transcript)
        
        # === Generate insights ===
        insights = advanced_detector.generate_insights(transcript, risk_score, threat_level)
        
        # === Determine if scam ===
        is_scam = risk_score >= 40
        confidence = risk_score / 100.0
        
        # Generate warning message
        warning_message = generate_warning_message(is_scam, threat_level, detected_patterns)
        
        # === FEATURE 10: Auto-disconnect recommendation ===
        auto_disconnect_recommended = risk_score >= 75
        
        # Prepare comprehensive result
        result = {
            'is_scam': is_scam,
            'confidence': round(confidence, 2),
            'risk_score': round(risk_score, 2),
            'threat_level': threat_level,
            'detected_threats': detected_patterns,
            'scam_category': scam_category,
            'redacted_transcript': redacted_transcript,
            'detected_pii': detected_pii,
            'warning_message': warning_message,
            'detected_language': detected_language,
            'insights': insights,
            
            # NEW: Enhanced data
            'voice_analysis': {
                'summary': voice_analysis['analysis_summary'],
                'rapid_speech': voice_analysis['speech_patterns']['rapid_speech_detected'],
                'robocall': voice_analysis['robocall_detection']['robocall_detected'],
                'emotional_manipulation': voice_analysis['emotional_manipulation']['emotion_manipulation_detected'],
                'dominant_emotion': voice_analysis['emotional_manipulation']['dominant_emotion'],
                'call_center_detected': voice_analysis['background_environment']['call_center_detected']
            },
            
            'caller_reputation': {
                'trust_level': reputation_data['trust_level'],
                'reputation_score': reputation_data['reputation_score'],
                'is_known_scammer': reputation_data['is_verified_scammer'],
                'community_reports': reputation_data['community_reports'],
                'recommendation': reputation_data['recommendation']
            },
            
            'spoofing_analysis': {
                'spoofing_detected': spoofing_analysis['spoofing_probability'] > 0.4,
                'spoofing_probability': spoofing_analysis['spoofing_probability'],
                'verdict': spoofing_analysis['verdict'],
                'recommendation': spoofing_analysis['recommendation']
            },
            
            'threat_intelligence': {
                'emerging_threats_matched': threat_match['threat_count'],
                'matched_threats': threat_match['matched_threats']
            },
            
            'auto_disconnect_recommended': auto_disconnect_recommended
        }
        
        # Update caller reputation in database
        caller_intelligence.update_reputation_score(caller_number, is_scam, risk_score, scam_category)
        
        # Track call pattern
        caller_intelligence.track_call_pattern(caller_number)
        
        # Generate audio warning if requested
        if generate_audio and is_scam:
            audio_url = generate_audio_warning(warning_message)
            result['audio_url'] = audio_url
        
        return jsonify(result)
        
    except Exception as e:
        import traceback
        print(f"Analysis error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


def detect_scam_category(patterns: list, transcript: str) -> str:
    """
    FEATURE 8: Detect industry-specific scam category
    """
    transcript_lower = transcript.lower()
    
    # Check for various scam categories
    if any(p in patterns for p in ['impersonation']) and any(word in transcript_lower for word in ['irs', 'tax', 'refund']):
        return 'IRS/Tax Scam'
    elif any(word in transcript_lower for word in ['microsoft', 'apple', 'computer', 'virus', 'tech support']):
        return 'Tech Support Scam'
    elif any(word in transcript_lower for word in ['bank', 'credit card', 'account', 'fraud department']):
        return 'Banking/Financial Scam'
    elif any(word in transcript_lower for word in ['social security', 'ssa', 'benefits']):
        return 'Social Security Scam'
    elif any(word in transcript_lower for word in ['lottery', 'prize', 'winner', 'congratulations']):
        return 'Prize/Lottery Scam'
    elif any(word in transcript_lower for word in ['invest', 'crypto', 'bitcoin', 'returns']):
        return 'Investment Scam'
    elif any(word in transcript_lower for word in ['electric', 'power', 'utility', 'water', 'gas']):
        return 'Utility Scam'
    elif any(word in transcript_lower for word in ['package', 'delivery', 'shipping', 'customs']):
        return 'Delivery Scam'
    elif any(word in transcript_lower for word in ['medicare', 'medicaid', 'health insurance']):
        return 'Healthcare Scam'
    elif 'romance' in patterns:
        return 'Romance Scam'
    else:
        return 'General Scam'


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
        return f"â ï¸ HIGH RISK SCAM DETECTED! This call shows multiple red flags: {', '.join(threat_list)}. DO NOT share personal information or make payments."
    elif threat_level == 'MEDIUM':
        return f"â ï¸ Potential scam detected: {', '.join(threat_list)}. Exercise caution and verify the caller's identity."
    else:
        return f"â ï¸ Some suspicious elements detected: {', '.join(threat_list)}. Stay vigilant."


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


# === NEW API ENDPOINTS ===

@app.route('/api/report', methods=['POST'])
def report_scam():
    """Community scam reporting"""
    try:
        data = request.json
        phone_number = data.get('phone_number')
        description = data.get('description', 'Scam call reported')
        risk_score = data.get('risk_score', 75)
        scam_category = data.get('scam_category', 'General Scam')
        
        if not phone_number:
            return jsonify({'error': 'Phone number is required'}), 400
        
        report_id = caller_intelligence.report_scam(
            phone_number, description, risk_score, scam_category
        )
        
        return jsonify({
            'success': True,
            'report_id': report_id,
            'message': 'Scam reported successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/block', methods=['POST'])
def block_number():
    """Block a phone number"""
    try:
        data = request.json
        phone_number = data.get('phone_number')
        reason = data.get('reason', 'User blocked')
        
        if not phone_number:
            return jsonify({'error': 'Phone number is required'}), 400
        
        success = caller_intelligence.block_number(phone_number, reason)
        
        return jsonify({
            'success': success,
            'message': f'Number {phone_number} blocked successfully' if success else 'Number already blocked'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reputation/<phone_number>', methods=['GET'])
def check_reputation_api(phone_number):
    """Check caller reputation"""
    try:
        reputation = caller_intelligence.check_number_reputation(phone_number)
        return jsonify({'success': True,' reputation': reputation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)

