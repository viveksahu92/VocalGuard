from database import VocalGuardDB
import json
from datetime import datetime, timedelta
import random

def seed_data():
    print("Seeding database with sample call history...")
    db = VocalGuardDB()
    
    # Sample data templates
    scam_templates = [
        {
            "transcript": "Hello, this is the IRS. You have unpaid taxes of $5000. If you do not pay immediately via gift card, we will issue a warrant for your arrest.",
            "caller_name": "IRS Officer Smith",
            "caller_number": "+12025550111",
            "is_scam": True,
            "confidence": 0.98,
            "threat_level": "HIGH",
            "detected_threats": ["urgency", "impersonation", "payment", "threats"],
            "warning_message": "⚠️ HIGH RISK SCAM DETECTED! This call shows multiple red flags: Pressure tactics detected, Possible impersonation, Payment request detected. DO NOT share personal information or make payments.",
            "scam_category": "IRS/Tax Scam"
        },
        {
            "transcript": "Congratulations! You have won a luxury cruise trip. Just pay the shipping fee of $50 to claim your prize now.",
            "caller_name": "Prize Center",
            "caller_number": "+18005550123",
            "is_scam": True,
            "confidence": 0.85,
            "threat_level": "MEDIUM",
            "detected_threats": ["too_good", "payment"],
            "warning_message": "⚠️ Potential scam detected: Unrealistic offers, Payment request detected. Exercise caution and verify the caller's identity.",
            "scam_category": "Prize/Lottery Scam"
        },
         {
            "transcript": "This is tech support. Your computer has a virus. Please give me remote access to fix it immediately.",
            "caller_name": "Windows Support",
            "caller_number": "+18885550199",
            "is_scam": True,
            "confidence": 0.92,
            "threat_level": "HIGH",
            "detected_threats": ["urgency", "impersonation"],
            "warning_message": "⚠️ HIGH RISK SCAM DETECTED! Tech support fraud indicators found.",
            "scam_category": "Tech Support Scam"
        }
    ]
    
    safe_templates = [
        {
            "transcript": "Hi mom, just calling to see how you are doing. Are we still on for dinner on Sunday?",
            "caller_name": "Mom",
            "caller_number": "+15551234567",
            "is_scam": False,
            "confidence": 0.02,
            "threat_level": "LOW",
            "detected_threats": [],
            "warning_message": "No scam indicators detected. Call appears legitimate.",
            "scam_category": None
        },
        {
            "transcript": "Hello, this is Dr. Jones' office confirming your appointment for tomorrow at 2 PM.",
            "caller_name": "Dr. Jones Office",
            "caller_number": "+15559876543",
            "is_scam": False,
            "confidence": 0.05,
            "threat_level": "LOW",
            "detected_threats": [],
            "warning_message": "No scam indicators detected. Call appears legitimate.",
            "scam_category": None
        }
    ]
    
    # Add 10 random calls
    calls_to_add = []
    
    # Add scams
    for t in scam_templates:
        calls_to_add.append(t)
        
    # Add safe calls
    for t in safe_templates:
        calls_to_add.append(t)
        
    # Add a few more random ones
    for _ in range(5):
        template = random.choice(scam_templates + safe_templates)
        new_call = template.copy()
        # Vary timestamp
        calls_to_add.append(new_call)

    # Insert into DB
    conn = db.init_db() # Re-init to ensure tables exist
    
    # We use the internal connection logic similar to save_call but manual to set timestamps
    import sqlite3
    conn = sqlite3.connect(db.db_path)
    cursor = conn.cursor()
    
    for i, call in enumerate(calls_to_add):
        # Time reverse order (newest first)
        call_time = datetime.now() - timedelta(hours=i*2)
        
        cursor.execute('''
            INSERT INTO calls 
            (user_id, caller_name, caller_number, transcript, is_scam, confidence, 
             threat_level, detected_threats, redacted_transcript, detected_pii, 
             warning_message, duration, language, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            None, # No user_id for public history
            call.get('caller_name'),
            call.get('caller_number'),
            call.get('transcript'),
            call.get('is_scam'),
            call.get('confidence'),
            call.get('threat_level'),
            json.dumps(call.get('detected_threats', [])),
            call.get('transcript'), # Using full transcript as redacted for this seed
            json.dumps([]),
            call.get('warning_message'),
            random.randint(30, 300),
            'en',
            call_time
        ))
    
    conn.commit()
    print(f"Successfully added {len(calls_to_add)} records to the database.")
    conn.close()

if __name__ == "__main__":
    seed_data()
