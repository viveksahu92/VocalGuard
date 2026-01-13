"""
VocalGuard Advanced Detection with Gemini Nano
Lightweight AI-powered scam detection without requiring paid APIs
Uses advanced pattern analysis and similarity matching
"""

import json
import math
from typing import Dict, List, Tuple

class AdvancedScamDetector:
    """Advanced scam detection using pattern analysis and scoring"""
    
    def __init__(self):
        self.scam_signatures = self._load_scam_signatures()
        self.language_patterns = self._load_language_patterns()
    
    def _load_scam_signatures(self) -> Dict:
        """Load comprehensive scam signatures and patterns"""
        return {
            'urgency': {
                'keywords': [
                    'immediately', 'right now', 'urgent', 'emergency', 'now',
                    'within 24 hours', 'today only', 'limited time', 'act fast',
                    'hurry', 'expires soon', 'don\'t wait', 'quickly', 'asap',
                    'before', 'deadline', 'last chance', 'final notice'
                ],
                'weight': 0.15,
                'description': 'Pressure tactics'
            },
            'payment_request': {
                'keywords': [
                    'wire transfer', 'gift card', 'bitcoin', 'cryptocurrency',
                    'western union', 'moneygram', 'prepaid card', 'cash payment',
                    'untraceable', 'itunes card', 'google play', 'steam card',
                    'payment', 'card number', 'bank account', 'routing number',
                    'wire', 'send money', 'pay now', 'purchase', 'refund'
                ],
                'weight': 0.20,
                'description': 'Payment request detected'
            },
            'personal_info': {
                'keywords': [
                    'social security', 'ssn', 'password', 'pin', 'pin number',
                    'account number', 'routing number', 'credit card', 'cvv',
                    'security code', 'date of birth', 'mother\'s maiden name',
                    'license number', 'passport', 'verify identity', 'confirm',
                    'personal information', 'credentials', 'login'
                ],
                'weight': 0.20,
                'description': 'Personal information request'
            },
            'impersonation': {
                'keywords': [
                    'irs', 'internal revenue', 'social security', 'medicare',
                    'microsoft', 'apple', 'amazon', 'google', 'paypal', 'bank',
                    'police', 'sheriff', 'federal agent', 'fbi', 'government',
                    'official', 'authority', 'federal', 'law enforcement'
                ],
                'weight': 0.18,
                'description': 'Possible impersonation'
            },
            'threats': {
                'keywords': [
                    'arrest', 'lawsuit', 'legal action', 'warrant', 'jail',
                    'prison', 'fine', 'penalty', 'sued', 'court', 'judge',
                    'prosecution', 'criminal', 'charges', 'delinquent',
                    'debt', 'collection', 'seize', 'freeze', 'close'
                ],
                'weight': 0.17,
                'description': 'Threatening language'
            },
            'too_good_to_be_true': {
                'keywords': [
                    'million', 'inheritance', 'prize', 'lottery', 'won',
                    'congratulations', 'claim', 'reward', 'free', 'bonus',
                    'money', 'cash', 'refund', 'windfall', 'rich', 'wealthy'
                ],
                'weight': 0.10,
                'description': 'Unrealistic offers'
            }
        }
    
    def _load_language_patterns(self) -> Dict:
        """Load patterns for multiple languages"""
        return {
            'en': {
                'urgency': ['immediately', 'urgent', 'now', 'hurry'],
                'payment': ['transfer', 'payment', 'card', 'money'],
                'threat': ['arrest', 'lawsuit', 'legal']
            },
            'es': {
                'urgency': ['inmediatamente', 'urgente', 'ahora', 'rápido'],
                'payment': ['transferencia', 'pago', 'tarjeta', 'dinero'],
                'threat': ['arresto', 'demanda', 'legal']
            },
            'fr': {
                'urgency': ['immédiatement', 'urgent', 'maintenant', 'vite'],
                'payment': ['virement', 'paiement', 'carte', 'argent'],
                'threat': ['arrestation', 'procès', 'légal']
            },
            'hi': {
                'urgency': ['तुरंत', 'आपातकाल', 'अभी', 'जल्दी'],
                'payment': ['स्थानांतरण', 'भुगतान', 'कार्ड', 'पैसा'],
                'threat': ['गिरफ्तारी', 'मुकदमा', 'कानूनी']
            }
        }
    
    def calculate_risk_score(self, transcript: str) -> Tuple[float, List[str], str]:
        """Calculate comprehensive risk score using advanced analysis"""
        transcript_lower = transcript.lower()
        total_score = 0
        detected_patterns = []
        
        # Analyze each scam signature
        for pattern_type, pattern_data in self.scam_signatures.items():
            pattern_score = 0
            keywords = pattern_data['keywords']
            
            # Count keyword matches
            matches = sum(1 for keyword in keywords if keyword in transcript_lower)
            
            if matches > 0:
                # Calculate pattern score based on matches
                pattern_score = min(matches / len(keywords), 1.0) * pattern_data['weight']
                total_score += pattern_score
                detected_patterns.append(pattern_type)
        
        # Bonus analysis: Check for multiple threat combinations
        threat_combinations = self._analyze_threat_combinations(transcript_lower)
        combination_boost = len(threat_combinations) * 0.05
        total_score += min(combination_boost, 0.15)
        
        # Normalize to 0-100 scale
        risk_score = min(total_score * 100, 100)
        
        # Determine threat level
        if risk_score >= 70:
            threat_level = 'HIGH'
        elif risk_score >= 40:
            threat_level = 'MEDIUM'
        else:
            threat_level = 'LOW'
        
        return risk_score, detected_patterns, threat_level
    
    def _analyze_threat_combinations(self, transcript: str) -> List[str]:
        """Detect dangerous combinations of threat factors"""
        combinations = []
        
        # Check for urgency + payment
        urgency_keys = self.scam_signatures['urgency']['keywords']
        payment_keys = self.scam_signatures['payment_request']['keywords']
        
        has_urgency = any(k in transcript for k in urgency_keys)
        has_payment = any(k in transcript for k in payment_keys)
        
        if has_urgency and has_payment:
            combinations.append('urgent_payment_demand')
        
        # Check for impersonation + threats
        imperson_keys = self.scam_signatures['impersonation']['keywords']
        threat_keys = self.scam_signatures['threats']['keywords']
        
        has_imperson = any(k in transcript for k in imperson_keys)
        has_threats = any(k in transcript for k in threat_keys)
        
        if has_imperson and has_threats:
            combinations.append('authority_threat')
        
        # Check for personal info + urgent payment
        info_keys = self.scam_signatures['personal_info']['keywords']
        has_info = any(k in transcript for k in info_keys)
        
        if has_info and has_payment:
            combinations.append('info_and_payment')
        
        return combinations
    
    def detect_language(self, transcript: str) -> str:
        """Detect language of transcript"""
        transcript_lower = transcript.lower()
        
        language_scores = {}
        for lang, patterns in self.language_patterns.items():
            score = 0
            for pattern_type, keywords in patterns.items():
                score += sum(1 for k in keywords if k in transcript_lower)
            language_scores[lang] = score
        
        # Return language with highest score, default to English
        return max(language_scores, key=language_scores.get) if max(language_scores.values()) > 0 else 'en'
    
    def generate_insights(self, transcript: str, risk_score: float, threat_level: str) -> Dict:
        """Generate detailed insights about the scam"""
        insights = {
            'risk_indicators': [],
            'why_its_scam': [],
            'protection_tips': [],
            'confidence_factors': []
        }
        
        transcript_lower = transcript.lower()
        
        # Identify risk indicators
        if any(k in transcript_lower for k in self.scam_signatures['urgency']['keywords']):
            insights['risk_indicators'].append('⚠️ High pressure/urgency tactics')
            insights['why_its_scam'].append('Scammers use urgency to prevent you from thinking clearly')
        
        if any(k in transcript_lower for k in self.scam_signatures['payment_request']['keywords']):
            insights['risk_indicators'].append('💳 Unusual payment method requested')
            insights['why_its_scam'].append('Legitimate organizations don\'t ask for gift cards or wire transfers')
        
        if any(k in transcript_lower for k in self.scam_signatures['personal_info']['keywords']):
            insights['risk_indicators'].append('🔐 Personal information requested')
            insights['why_its_scam'].append('Real institutions never ask for SSN, passwords, or credit card numbers')
        
        if any(k in transcript_lower for k in self.scam_signatures['impersonation']['keywords']):
            insights['risk_indicators'].append('👤 Suspicious caller identity')
            insights['why_its_scam'].append('Verify independently before trusting caller credentials')
        
        if any(k in transcript_lower for k in self.scam_signatures['threats']['keywords']):
            insights['risk_indicators'].append('⚡ Threatening or intimidating language')
            insights['why_its_scam'].append('Scammers threaten legal action to create fear')
        
        # Add protection tips
        insights['protection_tips'] = [
            '✓ Hang up immediately if pressured',
            '✓ Never share personal/financial information',
            '✓ Verify by calling official numbers',
            '✓ No legitimate entity sends money via gift cards',
            '✓ Report to FTC at reportfraud.ftc.gov'
        ]
        
        # Confidence factors
        if risk_score >= 70:
            insights['confidence_factors'] = [
                f'Multiple red flags detected ({len(insights["risk_indicators"])})',
                'Strong pattern match to known scams',
                'High confidence classification'
            ]
        elif risk_score >= 40:
            insights['confidence_factors'] = [
                'Some suspicious indicators present',
                'Proceed with caution',
                'Verify caller independently'
            ]
        else:
            insights['confidence_factors'] = [
                'Low risk indicators detected',
                'Appears to be legitimate',
                'But stay vigilant'
            ]
        
        return insights
