"""
VocalGuard Advanced Scam Detector Module
Multi-language AI-powered scam detection with behavioral analysis
"""

import re
from typing import Dict, List, Tuple
import math


class ScamDetector:
    """
    Advanced scam pattern detector with multi-language support and ML-style scoring
    """
    
    def __init__(self):
        # PII patterns
        self.pii_patterns = {
            'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            'ssn': r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'zip_code': r'\b\d{5}(?:-\d{4})?\b',
            'bank_account': r'\b\d{8,17}\b',
            'cvv': r'\b\d{3,4}\b'
        }
        
        # EXPANDED Multi-language scam keywords (English + transliterated common scams)
        self.threat_keywords = {
            'urgency': [
                # English
                'immediately', 'right now', 'urgent', 'emergency', 'within 24 hours',
                'today only', 'limited time', 'act fast', 'hurry', 'expires soon',
                'expire today', 'last chance', 'final notice', 'time sensitive',
                # Spanish
                'inmediatamente', 'urgente', 'emergencia', 'ahora mismo',
                # French
                'immédiatement', 'urgent', 'maintenant',
                # German
                'sofort', 'dringend', 'notfall',
                # Hindi/Indian
                'turant', 'jaldi', 'abhi', 'emergency hai',
                # Common phrases
                'must act now', 'call back immediately', 'within one hour'
            ],
            'payment': [
                'wire transfer', 'gift card', 'bitcoin', 'cryptocurrency', 'crypto',
                'western union', 'moneygram', 'prepaid card', 'cash payment',
                'untraceable', 'iTunes card', 'google play card', 'steam card',
                'amazon gift card', 'walmart card', 'target gift card', 'paypal',
                'venmo', 'cash app', 'zelle', 'reload pack', 'green dot',
                'vanilla card', 'netspend', 'cash reload', 'bitcoin atm',
                'send money', 'transfer funds', 'payment required', 'processing fee',
                'activation fee', 'delivery fee', 'customs fee', 'tax payment',
                'ransom', 'bail money', 'fine payment'
            ],
            'personal_info': [
                'social security', 'ssn', 'social security number', 'password',
                'pin number', 'account number', 'routing number', 'credit card',
                'debit card', 'cvv', 'security code', 'date of birth', 'dob',
                'mother maiden name', 'maiden name', 'drivers license',
                'passport number', 'tax id', 'ein', 'bank account',
                'card number', 'expiration date', 'security question',
                'verify your identity', 'confirm your account', 'validate account',
                'access code', 'verification code', 'otp', 'one time password',
                'remote access', 'anydesk', 'teamviewer', 'screen share'
            ],
            'impersonation': [
                # Government
                'irs', 'internal revenue service', 'social security administration',
                'ssa', 'medicare', 'medicaid', 'federal trade commission', 'ftc',
                'department of justice', 'doj', 'fbi', 'cia', 'homeland security',
                'immigration', 'customs', 'border patrol', 'treasury department',
                # Tech companies
                'microsoft', 'windows', 'apple', 'mac support', 'icloud',
                'google', 'amazon', 'ebay', 'paypal', 'netflix', 'facebook',
                # Financial
                'bank', 'credit union', 'visa', 'mastercard', 'american express',
                'discover', 'wells fargo', 'chase', 'bank of america', 'citibank',
                'capital one', 'fraud department', 'security department',
                # Utilities
                'electric company', 'power company', 'water department', 'gas company',
                # Others
                'tech support', 'customer service', 'warranty department',
                'refund department', 'claiming to be', 'representing'
            ],
            'threats': [
                'arrest', 'arrested', 'lawsuit', 'legal action', 'warrant',
                'suspended', 'suspend', 'frozen account', 'freeze account',
                'compromised', 'investigation', 'criminal charges', 'jail',
                'prison', 'prosecution', 'prosecute', 'court', 'sheriff',
                'police', 'law enforcement', 'federal agent', 'legal consequences',
                'penalties', 'fines', 'seize', 'confiscate', 'revoke',
                'terminate', 'cancellation', 'suspended license', 'deportation',
                'virus detected', 'hacked', 'breach', 'malware', 'infected'
            ],
            'too_good': [
                'won', 'winner', 'congratulations', 'prize', 'lottery',
                'sweepstakes', 'free money', 'inheritance', 'millions',
                'guaranteed', 'risk-free', 'no obligation', 'incredible offer',
                'limited offer', 'special promotion', 'exclusive deal',
                'you have been selected', 'chosen', 'qualify for', 'eligible',
                'claim your', 'collect your', 'free trial', 'no cost',
                'refund', 'compensation', 'settlement', 'class action',
                'work from home', 'make money fast', 'get rich', 'financial freedom'
            ],
            'romance': [
                'love', 'darling', 'honey', 'baby', 'sweetheart', 'my love',
                'stranded', 'stuck', 'emergency', 'need money', 'western union',
                'moneygram', 'ticket', 'visa', 'passport', 'hospital',
                'military', 'deployed', 'overseas', 'meet you', 'come visit'
            ],
            'investment': [
                'investment opportunity', 'invest now', 'guaranteed returns',
                'double your money', 'triple your', 'forex', 'trading',
                'stock tip', 'insider information', 'cryptocurrency investment',
                'bitcoin investment', 'nft', 'real estate opportunity',
                'business opportunity', 'franchise', 'pyramid', 'mlm',
                'multi-level', 'recruitment', 'sign up fee'
            ],
            'charity': [
                'donation', 'charity', 'fundraiser', 'gofundme', 'disaster relief',
                'help children', 'orphans', 'cancer', 'veterans', 'homeless',
                'urgent appeal', 'emergency fund', 'please donate'
            ],
            'tech_scam': [
                'computer', 'pc', 'laptop', 'virus', 'malware', 'trojan',
                'spyware', 'ransomware', 'encrypted', 'firewall', 'antivirus',
                'license expired', 'subscription', 'renewal', 'ip address',
                'hacker', 'breach', 'security alert', 'suspicious activity',
                'refund owed', 'technical support', 'error message', 'blue screen'
            ]
        }
        
        # Behavioral red flags
        self.behavioral_patterns = {
            'excessive_urgency': ['now', 'immediately', 'today', 'urgent'],
            'pressure_tactics': ['only', 'limited', 'last', 'final'],
            'secrecy_requests': ['don\'t tell', 'keep secret', 'between us', 'confidential'],
            'payment_urgency': ['pay now', 'send immediately', 'right away'],
            'verification_bypass': ['no need to verify', 'trust me', 'skip verification']
        }
    
    def redact_pii(self, text: str) -> Dict[str, any]:
        """
        Redact personally identifiable information from text
        
        Args:
            text: Input text containing potential PII
            
        Returns:
            Dictionary with redacted_text and pii_found list
        """
        redacted_text = text
        pii_found = []
        
        # Redact credit card numbers
        if re.search(self.pii_patterns['credit_card'], text):
            pii_found.append('credit_card')
            redacted_text = re.sub(
                self.pii_patterns['credit_card'],
                '[CREDIT CARD REDACTED]',
                redacted_text
            )
        
        # Redact SSN
        if re.search(self.pii_patterns['ssn'], text):
            pii_found.append('ssn')
            redacted_text = re.sub(
                self.pii_patterns['ssn'],
                '[SSN REDACTED]',
                redacted_text
            )
        
        # Redact phone numbers
        if re.search(self.pii_patterns['phone'], text):
            pii_found.append('phone')
            redacted_text = re.sub(
                self.pii_patterns['phone'],
                '[PHONE REDACTED]',
                redacted_text
            )
        
        # Redact email addresses
        if re.search(self.pii_patterns['email'], text):
            pii_found.append('email')
            redacted_text = re.sub(
                self.pii_patterns['email'],
                '[EMAIL REDACTED]',
                redacted_text
            )
        
        # Redact ZIP codes
        if re.search(self.pii_patterns['zip_code'], text):
            pii_found.append('zip_code')
            redacted_text = re.sub(
                self.pii_patterns['zip_code'],
                '[ZIP REDACTED]',
                redacted_text
            )
        
        return {
            'redacted_text': redacted_text,
            'pii_found': pii_found
        }
    
    def flag_threats(self, text: str) -> Dict[str, any]:
        """
        Advanced ML-style scam detection with behavioral analysis
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with is_threat, confidence, detected_patterns, and risk_score
        """
        text_lower = text.lower()
        detected_patterns = []
        threat_scores = {}
        
        # Check each threat category with weighted scoring
        category_weights = {
            'urgency': 0.15,
            'payment': 0.25,  # Highest weight
            'personal_info': 0.20,
            'impersonation': 0.20,
            'threats': 0.20,
            'too_good': 0.15,
            'romance': 0.18,
            'investment': 0.18,
            'charity': 0.12,
            'tech_scam': 0.17
        }
        
        # Pattern matching with frequency analysis
        for category, keywords in self.threat_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            if matches > 0:
                detected_patterns.append(category)
                # Logarithmic scoring for multiple matches
                base_score = min(math.log(matches + 1) * 0.3, 1.0)
                weighted_score = base_score * category_weights.get(category, 0.1)
                threat_scores[category] = weighted_score
        
        # Behavioral analysis
        behavioral_score = self._analyze_behavior(text_lower)
        
        # Linguistic analysis
        linguistic_score = self._analyze_linguistics(text_lower)
        
        # Composite confidence score (ML-style ensemble)
        pattern_confidence = sum(threat_scores.values())
        
        # Combine all scores with weights
        final_confidence = min(
            pattern_confidence * 0.5 +  # 50% from patterns
            behavioral_score * 0.3 +    # 30% from behavior
            linguistic_score * 0.2,     # 20% from linguistics
            1.0
        )
        
        # Multi-factor threat detection
        is_threat = (
            len(detected_patterns) >= 2 or  # Multiple threat types
            final_confidence >= 0.4 or      # High confidence
            ('payment' in detected_patterns and 'urgency' in detected_patterns) or  # Critical combo
            ('personal_info' in detected_patterns and 'impersonation' in detected_patterns)
        )
        
        # Calculate risk score (0-100)
        risk_score = min(int(final_confidence * 150), 100)
        
        return {
            'is_threat': is_threat,
            'confidence': round(final_confidence, 2),
            'detected_patterns': detected_patterns,
            'risk_score': risk_score,
            'behavioral_score': round(behavioral_score, 2),
            'linguistic_score': round(linguistic_score, 2),
            'threat_breakdown': {k: round(v, 2) for k, v in threat_scores.items()}
        }
    
    def _analyze_behavior(self, text: str) -> float:
        """
        Analyze behavioral red flags in conversation
        """
        score = 0.0
        
        for pattern_type, keywords in self.behavioral_patterns.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > 0:
                score += min(matches * 0.15, 0.3)
        
        # Check for multiple exclamation marks (urgency indicator)
        if text.count('!') >= 2:
            score += 0.1
        
        # Check for ALL CAPS words (pressure tactic)
        caps_words = re.findall(r'\b[A-Z]{4,}\b', text)
        if len(caps_words) >= 2:
            score += 0.15
        
        # Check for repeated words (suspicious)
        words = text.split()
        if len(words) != len(set(words)):
            score += 0.05
        
        return min(score, 1.0)
    
    def _analyze_linguistics(self, text: str) -> float:
        """
        Analyze linguistic patterns common in scams
        """
        score = 0.0
        
        # Poor grammar indicators
        double_spaces = text.count('  ')
        if double_spaces > 2:
            score += 0.1
        
        # Excessive punctuation
        punctuation_ratio = sum(text.count(p) for p in '!?.') / max(len(text), 1)
        if punctuation_ratio > 0.03:
            score += 0.15
        
        # Number-heavy text (account numbers, amounts)
        numbers = re.findall(r'\d+', text)
        if len(numbers) > 4:
            score += 0.1
        
        # Question words (verification attempts)
        questions = ['what is your', 'can you provide', 'please confirm', 'verify your']
        question_count = sum(1 for q in questions if q in text)
        if question_count >= 2:
            score += 0.2
        
        return min(score, 1.0)
    
    def detect_language(self, text: str) -> str:
        """
        Simple language detection based on character patterns
        """
        # Check for non-English characters
        if re.search(r'[à-ÿ]', text):
            return 'French/Spanish/German'
        elif re.search(r'[а-яА-Я]', text):
            return 'Russian/Cyrillic'
        elif re.search(r'[\u4e00-\u9fff]', text):
            return 'Chinese'
        elif re.search(r'[\u0600-\u06ff]', text):
            return 'Arabic'
        elif re.search(r'[\u0900-\u097f]', text):
            return 'Hindi/Devanagari'
        else:
            return 'English/Latin'
    
    def redact_numbers_for_display(self, text: str, blur: bool = False) -> str:
        """
        Redact or blur numbers in transcript for privacy display
        
        Args:
            text: Input text
            blur: If True, replace numbers with asterisks for privacy
            
        Returns:
            Text with numbers redacted if blur=True
        """
        if not blur:
            return text
        
        # Replace all number sequences with asterisks
        return re.sub(r'\d', '*', text)
