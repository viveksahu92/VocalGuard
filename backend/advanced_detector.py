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
                    'time sensitive', 'expire', 'last chance', 'final notice'
                ], 
                'weight': 0.18
            },
            'payment_request': {
                'keywords': [
                    'wire', 'gift card', 'bitcoin', 'cryptocurrency', 'itunes', 'google play',
                    'moneygram', 'western union', 'paypal', 'venmo', 'zelle', 'cashapp', 'cash app',
                    'prepaid card', 'reload pack', 'send money', 'transfer', 'pay', 'payment',
                    'deposit', 'bank account', 'routing number', '$', 'dollar', 'fee', 'charge'
                ], 
                'weight': 0.22
            },
            'personal_info': {
                'keywords': [
                    'ssn', 'social security', 'password', 'credit card', 'debit card', 'cvv', 'pin',
                    'account number', 'routing number', 'mothers maiden', 'date of birth', 'dob',
                    'verify your', 'confirm your', 'update your', 'provide your', 'give me your',
                    'share your', 'license number', 'passport'
                ], 
                'weight': 0.22
            },
            'impersonation': {
                'keywords': [
                    'irs', 'internal revenue', 'tax', 'microsoft', 'apple', 'google', 'amazon',
                    'bank', 'wells fargo', 'chase', 'security department', 'fraud department',
                    'social security', 'ssa', 'medicare', 'medicaid', 'government', 'federal',
                    'sheriff', 'police', 'officer', 'agent', 'tech support', 'customer service',
                    'refund department'
                ], 
                'weight': 0.20
            },
            'threats': {
                'keywords': [
                    'arrest', 'arrested', 'lawsuit', 'legal action', 'warrant', 'prosecution',
                    'jail', 'prison', 'court', 'suspended', 'frozen', 'shut off', 'disconnect',
                    'terminated', 'criminal', 'charges', 'penalty', 'fine', 'consequences'
                ], 
                'weight': 0.20
            },
            'too_good_to_be_true': {
                'keywords': [
                    'prize', 'lottery', 'won', 'winner', 'congratulations', 'selected', 'qualified',
                    'free', 'guaranteed', 'risk-free', 'double your money', 'triple', 'opportunity',
                    'limited spots', 'exclusive', 'claim your', 'youve been chosen'
                ], 
                'weight': 0.15
            },
            'emotional_manipulation': {
                'keywords': [
                    'love you', 'darling', 'sweetheart', 'honey', 'baby', 'help me', 'need you',
                    'trust me', 'promise', 'dont tell', 'secret', 'emergency', 'accident',
                    'hospital', 'stuck', 'stranded', 'scared', 'trouble', 'crisis'
                ], 
                'weight': 0.20
            },
            'remote_access': {
                'keywords': [
                    'remote access', 'anydesk', 'teamviewer', 'remote desktop', 'screenshare',
                    'download', 'install', 'click on', 'go to website', 'type in', 'enter this code'
                ], 
                'weight': 0.18
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
                
                # BOOST scores for multiple keyword matches
                if matches >= 2:
                    pattern_score *= 1.5
                if matches >= 3:
                    pattern_score *= 1.8
                    
                total_score += pattern_score
                detected_patterns.append(pattern_type)
        
        # MAJOR BOOST: Dangerous pattern combinations
        combination_bonus = 0
        pattern_count = len(detected_patterns)
        
        # 3+ patterns = definitely suspicious
        if pattern_count >= 3:
            combination_bonus += 0.25
        
        # 4+ patterns = high risk
        if pattern_count >= 4:
            combination_bonus += 0.30
            
        # 5+ patterns = extreme risk
        if pattern_count >= 5:
            combination_bonus += 0.35
        
        # Check for specific dangerous combos
        if 'impersonation' in detected_patterns and 'threats' in detected_patterns:
            combination_bonus += 0.20  # Authority + threat = classic scam
        
        if 'payment_request' in detected_patterns and 'urgency' in detected_patterns:
            combination_bonus += 0.20  # Payment + urgency = pressure scam
            
        if 'personal_info' in detected_patterns and 'threats' in detected_patterns:
            combination_bonus += 0.15  # Info harvesting + threats
        
        total_score += combination_bonus
        
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
        if risk_score >= 70:
            threat_level = 'HIGH'
        elif risk_score >= 40:
            threat_level = 'MEDIUM'
        else:
            threat_level = 'LOW'
        
        return risk_score, detected_patterns, threat_level
    
    def detect_language(self, transcript):
        return 'en'
    
    def generate_insights(self, transcript, risk_score, threat_level):
        return {
            'risk_indicators': [],
            'why_its_scam': [],
            'protection_tips': ['Hang up immediately', 'Never share personal info'],
            'confidence_factors': []
        }
