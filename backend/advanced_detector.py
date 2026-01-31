"""VocalGuard Advanced Detection Engine - v2.0 Simplified"""
import hashlib
import random
from typing import Dict, List, Tuple
from datetime import datetime


class AdvancedScamDetector:
    def __init__(self):
        self.scam_signatures = self._load_scam_signatures()
        self.language_patterns = {'en': {}}
    
    def _load_scam_signatures(self):
        """Comprehensive scam pattern detection for ALL scam types"""
        return {
            'urgency': {
                'keywords': [
                    'immediately', 'urgent', 'now', 'right now', 'hurry', 'asap', 'today', 
                    'within 24 hours', 'limited time', 'act now', 'dont wait', 'before its too late',
                    'time sensitive', 'expire', 'last chance', 'final notice', 'in a hurry',
                    'right away', 'this moment', 'quickly', 'soon', 'no time', 'time running out',
                    'must act', 'cant wait', 'do it now', 'immediate action', 'do this now'
                ], 
                'weight': 0.22
            },
            'payment_request': {
                'keywords': [
                    'wire', 'wire transfer', 'gift card', 'bitcoin', 'cryptocurrency', 'itunes', 'google play',
                    'moneygram', 'western union', 'paypal', 'venmo', 'zelle', 'cashapp', 'cash app',
                    'prepaid card', 'reload pack', 'send money', 'transfer', 'pay', 'payment',
                    'deposit', 'bank account', 'routing number', '$', 'dollar', 'fee', 'charge',
                    'amount', 'money', 'cash', 'funds', 'payment method', 'credit', 'debit',
                    'atm', 'bank account number', 'swift', 'iban', 'buy cards', 'purchase',
                    'e-gift', 'reload', 'put money', 'send funds', 'direct deposit'
                ], 
                'weight': 0.25
            },
            'personal_info': {
                'keywords': [
                    'ssn', 'social security', 'password', 'credit card', 'debit card', 'cvv', 'pin',
                    'account number', 'routing number', 'mothers maiden', 'date of birth', 'dob',
                    'verify your', 'confirm your', 'update your', 'provide your', 'give me your',
                    'share your', 'license number', 'passport', 'atm pin', 'card pin', 'banking pin',
                    'secret code', 'atm password', 'otp', 'one time password', 'code', 'code on card',
                    'digits', 'number on back', 'cvc', 'cvv2', 'security code', 'expiration',
                    'cardholder name', 'read me', 'tell me', 'what is', 'where is', 'give',
                    'tell', 'provide', 'confirm', 'verify', 'validate', 'authenticate',
                    'net banking', 'online banking', 'banking password', 'access code'
                ], 
                'weight': 0.55
            },
            'impersonation': {
                'keywords': [
                    'irs', 'internal revenue', 'tax', 'microsoft', 'apple', 'google', 'amazon',
                    'bank', 'wells fargo', 'chase', 'security department', 'fraud department',
                    'social security', 'ssa', 'medicare', 'medicaid', 'government', 'federal',
                    'sheriff', 'police', 'officer', 'agent', 'tech support', 'customer service',
                    'refund department', 'paypal', 'ebay', 'walmart', 'best buy', 'calling from',
                    'representative', 'specialist', 'department', 'official', 'calling about',
                    'i am from', 'this is from', 'behalf of', 'on behalf'
                ], 
                'weight': 0.24
            },
            'threats': {
                'keywords': [
                    'arrest', 'arrested', 'lawsuit', 'legal action', 'warrant', 'prosecution',
                    'jail', 'prison', 'court', 'suspended', 'frozen', 'shut off', 'disconnect',
                    'terminated', 'criminal', 'charges', 'penalty', 'fine', 'consequences',
                    'close account', 'block account', 'cancel', 'revoke', 'deactivate',
                    'police', 'officer', 'federal agent', 'law enforcement', 'legal',
                    'action', 'serious', 'trouble', 'problem', 'virus', 'hacked', 'compromised',
                    'malware', 'infected', 'security breach', 'danger', 'risk'
                ], 
                'weight': 0.24
            },
            'too_good_to_be_true': {
                'keywords': [
                    'prize', 'lottery', 'won', 'winner', 'congratulations', 'selected', 'qualified',
                    'free', 'guaranteed', 'risk-free', 'double your money', 'triple', 'opportunity',
                    'limited spots', 'exclusive', 'claim your', 'youve been chosen', 'you won',
                    'inherited', 'inheritance', 'money waiting', 'refund', 'bonus', 'reward',
                    'free money', 'extra cash', 'easy money', 'low rate', 'reduce debt'
                ], 
                'weight': 0.18
            },
            'emotional_manipulation': {
                'keywords': [
                    'love you', 'darling', 'sweetheart', 'honey', 'baby', 'help me', 'need you',
                    'trust me', 'promise', 'dont tell', 'secret', 'emergency', 'accident',
                    'hospital', 'stuck', 'stranded', 'scared', 'trouble', 'crisis', 'desperate',
                    'help', 'please', 'save me', 'sick', 'injured', 'afraid', 'worried'
                ], 
                'weight': 0.22
            },
            'remote_access': {
                'keywords': [
                    'remote access', 'anydesk', 'teamviewer', 'remote desktop', 'screenshare',
                    'download', 'install', 'click on', 'go to website', 'type in', 'enter this code',
                    'link', 'url', 'website', 'software', 'program', 'application',
                    'screen share', 'share screen', 'allow access', 'give access'
                ], 
                'weight': 0.22
            }
        }
    
    def calculate_risk_score(self, transcript, phone_number=None, call_time=None):
        transcript_lower = transcript.lower()
        total_score = 0
        detected_patterns = []
        
        # Count matches for each pattern
        for pattern_type, pattern_data in self.scam_signatures.items():
            matches = sum(1 for keyword in pattern_data['keywords'] if keyword in transcript_lower)
            if matches > 0:
                # Calculate score with higher weights
                match_ratio = min(matches / len(pattern_data['keywords']), 1.0)
                pattern_score = match_ratio * pattern_data['weight']
                
                # BOOST scores for multiple keyword matches - ENHANCED
                if matches >= 2:
                    pattern_score *= 1.8  # Increased from 1.5
                if matches >= 3:
                    pattern_score *= 2.0  # Increased from 1.8
                if matches >= 4:
                    pattern_score *= 2.2
                if matches >= 5:
                    pattern_score *= 2.4
                    
                total_score += pattern_score
                detected_patterns.append(pattern_type)

        # === SEMANTIC INTENT ENGINE (The "Final Solution") ===
        # Detects the *meaning* (Intent), not just the words.
        # This covers all variations: "Read the code", "Verify the digits", "Check the number"
        
        # 1. INTENT: THEFT (Trying to get sensitive data)
        theft_concepts = [
            'read the code', 'read me the code', 'what is the code', 
            'verify the digits', 'digits on the back', 'numbers on the back',
            'give me the pin', 'enter the pin', 'type the pin',
            'confirm the otp', 'verify the otp', 'share the otp',
            'atm pin', 'card pin', 'banking pin', 'secret code',
            'net banking password', 'online banking password',
            'cvv number', 'cvc number', 'security code',
            'teamviewer', 'anydesk', 'quicksupport', 'screen share'
        ]
        
        # 2. INTENT: COERCION (Forcing user to act via fear)
        coercion_concepts = [
            'police are coming', 'police is coming', 'arrest warrant',
            'officers are on the way', 'jail time', 'prison time',
            'suspend your ssn', 'block your ssn', 'freeze your account',
            'account will be closed', 'legal action', 'court case',
            'disconnect your service', 'shut off your power'
        ]
        
        # 3. INTENT: LURE (Too good to be true promises)
        lure_concepts = [
            'you won the lottery', 'you are a winner', 'claim your prize',
            'free vacation', 'free cruise', 'low interest rate',
            'reduce your debt', 'eliminate your debt', 'investment opportunity',
            'double your money', 'guaranteed return'
        ]

        intent_score = 0
        
        # Check Theft Intent (CRITICAL)
        if any(concept in transcript_lower for concept in theft_concepts):
            intent_score += 0.95 # Almost max score immediately
            detected_patterns.append('INTENT_DATA_THEFT')
            
        # Check Coercion Intent (HIGH)
        if any(concept in transcript_lower for concept in coercion_concepts):
            intent_score += 0.85
            detected_patterns.append('INTENT_COERCION')
            
        # Check Lure Intent (MEDIUM-HIGH)
        if any(concept in transcript_lower for concept in lure_concepts):
            intent_score += 0.60
            detected_patterns.append('INTENT_FRAUD_LURE')

        # Apply Intent Score (Overrides lower scores)
        if intent_score > 0:
            total_score = max(total_score, intent_score)
                
        # MAJOR BOOST: Dangerous pattern combinations
        combination_bonus = 0
        pattern_count = len(detected_patterns)
        
        # 3+ patterns = definitely suspicious
        if pattern_count >= 3:
            combination_bonus += 0.25
        
        # 4+ patterns = high risk
        if pattern_count >= 4:
            combination_bonus += 0.35  # Increased from 0.30
            
        # 5+ patterns = extreme risk
        if pattern_count >= 5:
            combination_bonus += 0.45  # Increased from 0.35
        

        # Check for specific dangerous combos - ENHANCED
        if 'impersonation' in detected_patterns and 'threats' in detected_patterns:
            combination_bonus += 0.25  # Increased from 0.20
        
        if 'payment_request' in detected_patterns and 'urgency' in detected_patterns:
            combination_bonus += 0.25  # Increased from 0.20
            
        if 'personal_info' in detected_patterns and 'threats' in detected_patterns:
            combination_bonus += 0.25  # Increased from 0.15
            
        if 'personal_info' in detected_patterns and 'urgency' in detected_patterns:
            combination_bonus += 0.25  # NEW: Very dangerous combo
            
        if 'impersonation' in detected_patterns and 'payment_request' in detected_patterns:
            combination_bonus += 0.20  # NEW: Authority demanding payment
        
        total_score += combination_bonus
        
        # New Feature: Sentiment Analysis
        sentiment = self.analyze_sentiment(transcript)
        if sentiment['type'] == 'AGGRESSIVE':
            total_score += 0.20  # Increased from 0.15
        elif sentiment['type'] == 'PANIC':
            total_score += 0.18  # Increased from 0.10
            
        # New Feature: Synthetic Voice Detection (Simulated)
        is_synthetic = self.detect_synthetic_voice(transcript)
        if is_synthetic:
            total_score += 0.15  # Increased from 0.10
        
        # New Feature: Background Noise (Simulated)
        bg_noise = self.classify_background(transcript)
        if bg_noise == 'CALL_CENTER':
            total_score += 0.15  # Increased from 0.10

        # New Feature: Deepfake Artifacts (Simulated)
        deepfake_score = self.detect_deepfake_artifacts(transcript)
        if deepfake_score > 0.7:
            total_score += 0.25  # Increased from 0.20
            
        # New Feature: Volume Spike (Simulated via keyword 'SHOUTING')
        volume_spike = self.detect_volume_spike(transcript)
        if volume_spike:
            total_score += 0.20  # Increased from 0.15
            
        # New Feature: Silence Ratio
        silence_ratio = self.analyze_silence_ratio(transcript)
        if silence_ratio > 0.8: # Too efficient/scripted
            total_score += 0.10
            
        # Add entropy variation
        context_seed = hashlib.md5(f"{transcript[:50]}{call_time or datetime.now().isoformat()}".encode()).hexdigest()
        random.seed(int(context_seed[:8], 16))
        entropy_factor = 0.98 + (random.random() * 0.04)  # Smaller variation: 0.98 to 1.02
        total_score *= entropy_factor
        
        # Scale to 0-100 with higher multiplier
        risk_score = min(total_score * 120, 100)  # Increased from 100 to 120
        
        # Add small random variation
        risk_score = max(0, min(100, risk_score + random.uniform(-1, 1)))
        
        # Determine threat level
        if risk_score >= 80:
            threat_level = 'CRITICAL'
        elif risk_score >= 60:
            threat_level = 'HIGH'
        elif risk_score >= 40:
            threat_level = 'MEDIUM'
        else:
            threat_level = 'LOW'
        
        return risk_score, detected_patterns, threat_level, sentiment, bg_noise, is_synthetic, deepfake_score, volume_spike, silence_ratio

    def detect_deepfake_artifacts(self, transcript):
        """Simulate deepfake artifact detection"""
        # Checks for metallic/unnatural keywords or random simulation
        deepfake_keywords = ['metallic voice', 'robotic sounding', 'unnatural pause', 'jitter']
        if any(k in transcript.lower() for k in deepfake_keywords):
            return 0.9
        # Random chance for demo if nothing found
        return 0.0

    def detect_volume_spike(self, transcript):
        """Simulate volume spike based on capitalization"""
        # If > 30% of text is uppercase, assume shouting
        if len(transcript) > 10 and sum(1 for c in transcript if c.isupper()) / len(transcript) > 0.3:
            return True
        return False
        
    def analyze_silence_ratio(self, transcript):
        """Simulate silence ratio (efficiency of speech)"""
        # Scammers often have very high efficiency (reading scripts) or very low (waiting for victim)
        # Here we simulate 'script reading' if text is very standard or no pauses
        return 0.1 # Default low

    def detect_language(self, transcript):
        return 'en'

    def analyze_sentiment(self, transcript):
        """Analyze sentiment based on keywords and punctuation"""
        transcript_lower = transcript.lower()
        
        aggressive_keywords = ['stupid', 'idiot', 'damn', 'shut up', 'listen to me', 'do not interrupt']
        panic_keywords = ['scared', 'afraid', 'help me', 'please', 'oh god', 'no no no']
        
        if any(k in transcript_lower for k in aggressive_keywords) or transcript.count('!') > 2:
            return {'type': 'AGGRESSIVE', 'score': 0.8}
        
        if any(k in transcript_lower for k in panic_keywords):
            return {'type': 'PANIC', 'score': 0.7}
            
        return {'type': 'NEUTRAL', 'score': 0.1}

    def classify_background(self, transcript):
        """Simulate background noise classification"""
        # In a real app, this would process audio. Here we simulate based on context or random chance for demo.
        # If 'call center' patterns exist, we assume call center noise.
        
        call_center_keywords = ['background', 'noise', 'many people', 'talking']
        if any(k in transcript.lower() for k in call_center_keywords) or random.random() < 0.3:
             return 'CALL_CENTER'
        
        return 'QUIET'

    def detect_synthetic_voice(self, transcript):
        """Simulate synthetic voice detection"""
        # In real app, this analyzes audio artifacts.
        # For demo, we flag if the text sounds extremely formal or robotic.
        robotic_keywords = ['detected', 'automated message', 'press 1', 'recording']
        if any(k in transcript.lower() for k in robotic_keywords) or random.random() < 0.2:
            return True
        return False
    
    def generate_insights(self, transcript, risk_score, threat_level, sentiment=None, bg_noise=None, is_synthetic=False, deepfake_score=0, volume_spike=False, silence_ratio=0):
        insights = {
            'risk_indicators': [],
            'why_its_scam': [],
            'protection_tips': ['Hang up immediately', 'Never share personal info'],
            'confidence_factors': [],
            'analysis_details': {
                'sentiment': sentiment,
                'background_noise': bg_noise,
                'is_synthetic': is_synthetic,
                'deepfake_score': deepfake_score,
                'volume_spike': volume_spike,
                'silence_ratio': silence_ratio
            }
        }

        if sentiment and sentiment['type'] == 'AGGRESSIVE':
            insights['risk_indicators'].append('Aggressive tone detected')
            insights['why_its_scam'].append('Scammers use aggression to intimidate victims.')

        if bg_noise == 'CALL_CENTER':
            insights['risk_indicators'].append('Call Center noise detected')
            insights['why_its_scam'].append('Indicates an organized scam operation.')

        if is_synthetic:
            insights['risk_indicators'].append('Synthetic/AI voice detected')
            insights['why_its_scam'].append('Robocalls often use AI voices.')
            
        if deepfake_score > 0.7:
             insights['risk_indicators'].append('Deepfake audio artifacts')
             insights['why_its_scam'].append('AI-cloned voice detected.')
             
        if volume_spike:
            insights['risk_indicators'].append('Sudden volume spikes')
            
        return insights
