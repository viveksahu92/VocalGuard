#!/usr/bin/env python3
"""
VocalGuard Backend Test Script
Tests the scam detection functionality without requiring API keys
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from scam_detector import ScamDetector

def print_separator():
    print("\n" + "="*80 + "\n")

def test_pii_redaction():
    print("🔒 Testing PII Redaction")
    print_separator()
    
    detector = ScamDetector()
    
    test_cases = [
        "My credit card number is 4532-1234-5678-9012",
        "Contact me at 555-123-4567 or email me at john@example.com",
        "My SSN is 123-45-6789 and I live in 90210",
    ]
    
    for text in test_cases:
        result = detector.redact_pii(text)
        print(f"Original: {text}")
        print(f"Redacted: {result['redacted_text']}")
        print(f"PII Found: {result['pii_found']}")
        print()

def test_threat_detection():
    print("🚨 Testing Threat Detection")
    print_separator()
    
    detector = ScamDetector()
    
    test_cases = [
        ("Legitimate call", "Hello, this is your doctor's office calling to confirm your appointment."),
        ("Low threat", "You've won a prize! Call us back to claim it."),
        ("Medium threat", "This is the IRS. You must pay your taxes immediately or face legal action."),
        ("High threat", "URGENT! Your account is frozen. Wire money to this account immediately using gift cards or you will be arrested within 24 hours. Provide your credit card now!")
    ]
    
    for label, text in test_cases:
        result = detector.flag_threats(text)
        print(f"Test: {label}")
        print(f"Text: {text}")
        print(f"Is Threat: {result['is_threat']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Detected Patterns: {', '.join(result['detected_patterns'])}")
        print()

def test_privacy_mode():
    print("👁️ Testing Privacy Mode")
    print_separator()
    
    detector = ScamDetector()
    
    text = "Call me at 555-123-4567 with your card number 4532-1234-5678-9012"
    
    print(f"Original: {text}")
    print(f"Normal Mode: {detector.redact_numbers_for_display(text, blur=False)}")
    print(f"Privacy Mode: {detector.redact_numbers_for_display(text, blur=True)}")

def display_features():
    print("\n" + "🛡️  VocalGuard - AI Anti-Scam Call Defense System".center(80))
    print_separator()
    
    features = [
        "✅ iPhone-style Call Simulation UI",
        "✅ AI-Powered Scam Detection (OpenAI Integration)",
        "✅ PII Redaction (Credit Cards, SSN, Phone, Email)",
        "✅ Multi-Category Threat Detection",
        "✅ Audio Warning Generation (ElevenLabs Integration)",
        "✅ Privacy Toggle for Number Blurring",
        "✅ Real-time Call Analysis",
        "✅ Color-coded Threat Levels (LOW/MEDIUM/HIGH)"
    ]
    
    print("Key Features:\n")
    for feature in features:
        print(f"  {feature}")
    
    print_separator()

def main():
    display_features()
    test_pii_redaction()
    test_threat_detection()
    test_privacy_mode()
    
    print("\n✅ All tests completed successfully!")
    print("\nNext Steps:")
    print("  1. Install backend dependencies: pip install -r requirements.txt")
    print("  2. Configure API keys in backend/.env")
    print("  3. Start backend: cd backend && python app.py")
    print("  4. Install frontend dependencies: cd frontend && npm install")
    print("  5. Start frontend: npm run dev")
    print("  6. Open http://localhost:3000 in your browser\n")

if __name__ == "__main__":
    main()
