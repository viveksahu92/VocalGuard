"""
Test script to demonstrate the IMPROVED scam detection in VocalGuard
Run this to test the enhanced detection capabilities
"""

import requests
import json

# Backend URL
BACKEND_URL = "http://127.0.0.1:5000"

def test_scam_detection(transcript, description):
    """Test a scam transcript"""
    print(f"\n{'='*80}")
    print(f"TEST: {description}")
    print(f"{'='*80}")
    
    payload = {
        "transcript": transcript,
        "caller_name": "Unknown Caller",
        "caller_number": "+1-555-0000"
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/analyze",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n🎯 DETECTION RESULT:")
            print(f"   ✓ Is Scam: {result['is_scam']}")
            print(f"   ✓ Risk Score: {result['risk_score']}/100")
            print(f"   ✓ Confidence: {result['confidence']*100:.1f}%")
            print(f"   ✓ Threat Level: {result['threat_level']}")
            print(f"   ✓ Detected Patterns: {', '.join(result['detected_threats'])}")
            print(f"\n📋 Scam Category: {result['scam_category']}")
            print(f"\n⚠️  Warning: {result['warning_message']}")
            
            if result['auto_disconnect_recommended']:
                print("\n🔴 AUTO-DISCONNECT RECOMMENDED!")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Connection error: {e}")
        print("Make sure the backend is running on http://127.0.0.1:5000")


# Test Case 1: IRS Scam
test_scam_detection(
    """
    Hello, this is calling from the Internal Revenue Service. This is urgent and time sensitive.
    We have a warrant for your arrest due to unpaid taxes. You need to act immediately or 
    you will face criminal charges and jail time. We need you to go to the nearest store and 
    purchase Google Play cards immediately. Read me the code on the back of the card so we can 
    process your payment. Do not tell anyone about this call. This is confidential.
    """,
    "IRS TAX SCAM (HIGH RISK)"
)

# Test Case 2: Microsoft Tech Support Scam
test_scam_detection(
    """
    Hello, this is technical support calling from Microsoft. Your computer has a virus detected.
    We need remote access to your computer immediately. Please download TeamViewer and give me 
    the access code so I can fix this. We found suspicious activity and need your banking password 
    to verify your account. This is urgent - your account will be frozen if we don't act now.
    """,
    "MICROSOFT TECH SUPPORT SCAM (HIGH RISK)"
)

# Test Case 3: Amazon Refund Scam
test_scam_detection(
    """
    Hi, we're calling from Amazon regarding your order refund. You are eligible for a $500 refund
    but we need to confirm your credit card number and cvv. Please verify your social security 
    number and routing number so we can process this payment. This is a limited time offer - 
    you need to confirm within 24 hours or the refund will expire.
    """,
    "AMAZON REFUND SCAM (MEDIUM-HIGH RISK)"
)

# Test Case 4: Romance/Catfish Scam
test_scam_detection(
    """
    Darling, I need your help. I'm stranded overseas and need money urgently. Please send me 
    $2000 via Western Union right now. I need to come visit you but I'm stuck here. Can you 
    wire transfer the money to my account immediately? Please don't tell anyone about this.
    """,
    "ROMANCE SCAM (MEDIUM RISK)"
)

# Test Case 5: Legitimate Call (Should be LOW risk)
test_scam_detection(
    """
    Hello, this is John from the dental office calling to confirm your appointment tomorrow 
    at 2 PM. Please let us know if you need to reschedule. Thank you and we look forward to 
    seeing you.
    """,
    "LEGITIMATE CALL (SHOULD BE LOW RISK)"
)

print("\n" + "="*80)
print("✅ TEST COMPLETE - All scam detection tests finished!")
print("="*80)
