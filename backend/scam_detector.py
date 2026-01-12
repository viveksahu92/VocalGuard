"""
Scam Detector Module
Handles PII redaction and threat pattern detection
"""

import re
from typing import Dict, List, Tuple


class ScamDetector:
    """
    Detects scam patterns and redacts PII from call transcripts
    """
    
    def __init__(self):
        # PII patterns
        self.pii_patterns = {
            'credit_card': r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',
            'ssn': r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'zip_code': r'\b\d{5}(?:-\d{4})?\b'
        }
        
        # Scam threat patterns
        self.threat_keywords = {
            'urgency': [
                'immediately', 'right now', 'urgent', 'emergency',
                'within 24 hours', 'today only', 'limited time',
                'act fast', 'hurry', 'expires soon'
            ],
            'payment': [
                'wire transfer', 'gift card', 'bitcoin', 'cryptocurrency',
                'western union', 'moneygram', 'prepaid card',
                'cash payment', 'untraceable', 'iTunes card',
                'google play card', 'steam card'
            ],
            'personal_info': [
                'social security', 'ssn', 'password', 'pin number',
                'account number', 'routing number', 'credit card',
                'cvv', 'security code', 'date of birth', 'mother\'s maiden name'
            ],
            'impersonation': [
                'irs', 'internal revenue service', 'social security administration',
                'medicare', 'microsoft support', 'apple support',
                'amazon customer service', 'bank security', 'federal agent',
                'police department', 'sheriff', 'warrant'
            ],
            'threats': [
                'arrest', 'lawsuit', 'legal action', 'warrant',
                'suspended', 'frozen account', 'compromised',
                'investigation', 'criminal charges', 'jail',
                'prosecution', 'court', 'sheriff'
            ],
            'too_good': [
                'won', 'winner', 'prize', 'lottery', 'sweepstakes',
                'free money', 'inheritance', 'millions', 'guaranteed',
                'risk-free', 'no obligation', 'incredible offer'
            ]
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
        Detect scam threat patterns in text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with is_threat, confidence, and detected_patterns
        """
        text_lower = text.lower()
        detected_patterns = []
        threat_scores = []
        
        # Check each threat category
        for category, keywords in self.threat_keywords.items():
            matches = sum(1 for keyword in keywords if keyword in text_lower)
            
            if matches > 0:
                detected_patterns.append(category)
                # Score based on number of matches in category
                category_score = min(matches * 0.2, 1.0)
                threat_scores.append(category_score)
        
        # Calculate overall confidence
        if threat_scores:
            # Multiple categories = higher confidence
            confidence = min(sum(threat_scores) * 0.3, 1.0)
            is_threat = len(detected_patterns) >= 2 or confidence >= 0.5
        else:
            confidence = 0.0
            is_threat = False
        
        return {
            'is_threat': is_threat,
            'confidence': confidence,
            'detected_patterns': detected_patterns
        }
    
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
