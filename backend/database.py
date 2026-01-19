"""
VocalGuard Database Module
Persistent storage for call analysis and user data
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

class VocalGuardDB:
    """SQLite database for VocalGuard"""
    
    def __init__(self, db_path='vocalguard.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calls table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                caller_name TEXT,
                caller_number TEXT,
                transcript TEXT,
                is_scam BOOLEAN,
                confidence REAL,
                threat_level TEXT,
                detected_threats TEXT,
                redacted_transcript TEXT,
                detected_pii TEXT,
                warning_message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                duration INTEGER,
                language TEXT DEFAULT 'en',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT,
                google_id TEXT UNIQUE,
                auth_provider TEXT DEFAULT 'email',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_calls_analyzed INTEGER DEFAULT 0,
                scams_blocked INTEGER DEFAULT 0
            )
        ''')
        
        # Reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                call_id INTEGER,
                report_type TEXT,
                report_data TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(call_id) REFERENCES calls(id)
            )
        ''')
        
        # Statistics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE,
                total_calls INTEGER,
                scams_detected INTEGER,
                confidence_avg REAL,
                top_threat TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_call(self, call_data):
        """Save analyzed call to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO calls 
            (caller_name, caller_number, transcript, is_scam, confidence, 
             threat_level, detected_threats, redacted_transcript, detected_pii, 
             warning_message, duration, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            call_data.get('caller_name'),
            call_data.get('caller_number'),
            call_data.get('transcript'),
            call_data.get('is_scam'),
            call_data.get('confidence'),
            call_data.get('threat_level'),
            json.dumps(call_data.get('detected_threats', [])),
            call_data.get('redacted_transcript'),
            json.dumps(call_data.get('detected_pii', [])),
            call_data.get('warning_message'),
            call_data.get('duration', 0),
            call_data.get('language', 'en')
        ))
        
        conn.commit()
        call_id = cursor.lastrowid
        conn.close()
        return call_id
    
    def get_all_calls(self, limit=50):
        """Get all calls from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM calls ORDER BY timestamp DESC LIMIT ?
        ''', (limit,))
        
        columns = [description[0] for description in cursor.description]
        calls = []
        for row in cursor.fetchall():
            call = dict(zip(columns, row))
            call['detected_threats'] = json.loads(call['detected_threats'])
            call['detected_pii'] = json.loads(call['detected_pii'])
            calls.append(call)
        
        conn.close()
        return calls
    
    def get_statistics(self):
        """Get overall statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM calls')
        total_calls = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM calls WHERE is_scam = 1')
        scams_detected = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(confidence) FROM calls')
        avg_confidence = cursor.fetchone()[0] or 0
        
        cursor.execute('''
            SELECT detected_threats FROM calls 
            WHERE is_scam = 1 ORDER BY timestamp DESC LIMIT 10
        ''')
        
        threat_counts = {}
        for row in cursor.fetchall():
            threats = json.loads(row[0])
            for threat in threats:
                threat_counts[threat] = threat_counts.get(threat, 0) + 1
        
        conn.close()
        
        return {
            'total_calls': total_calls,
            'scams_detected': scams_detected,
            'safe_calls': total_calls - scams_detected,
            'detection_rate': round((scams_detected / total_calls * 100) if total_calls > 0 else 0, 2),
            'average_confidence': round(avg_confidence, 2),
            'top_threats': threat_counts
        }
    
    def search_calls(self, query):
        """Search calls by transcript, caller name, or number"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        search_pattern = f'%{query}%'
        cursor.execute('''
            SELECT * FROM calls 
            WHERE transcript LIKE ? OR caller_name LIKE ? OR caller_number LIKE ?
            ORDER BY timestamp DESC
        ''', (search_pattern, search_pattern, search_pattern))
        
        columns = [description[0] for description in cursor.description]
        calls = []
        for row in cursor.fetchall():
            call = dict(zip(columns, row))
            call['detected_threats'] = json.loads(call['detected_threats'])
            call['detected_pii'] = json.loads(call['detected_pii'])
            calls.append(call)
        
        conn.close()
        return calls
    
    # === User Authentication Methods ===
    
    def create_user(self, email, password_hash=None, username=None, google_id=None, auth_provider='email'):
        """Create a new user (supports both email and Google auth)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (email, password_hash, username, google_id, auth_provider)
                VALUES (?, ?, ?, ?, ?)
            ''', (email, password_hash, username or email.split('@')[0], google_id, auth_provider))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None  # User already exists
    
    def get_user_by_email(self, email):
        """Get user by email"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            user = dict(zip(columns, row))
        else:
            user = None
        
        conn.close()
        return user
    
    def get_user_by_google_id(self, google_id):
        """Get user by Google ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE google_id = ?', (google_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            user = dict(zip(columns, row))
        else:
            user = None
        
        conn.close()
        return user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        
        if row:
            columns = [description[0] for description in cursor.description]
            user = dict(zip(columns, row))
        else:
            user = None
        
        conn.close()
        return user
    
    def get_user_calls(self, user_id, limit=50):
        """Get calls for a specific user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM calls 
            WHERE user_id = ?
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (user_id, limit))
        
        columns = [description[0] for description in cursor.description]
        calls = []
        for row in cursor.fetchall():
            call = dict(zip(columns, row))
            call['detected_threats'] = json.loads(call['detected_threats'])
            call['detected_pii'] = json.loads(call['detected_pii'])
            calls.append(call)
        
        conn.close()
        return calls
    
    def get_user_statistics(self, user_id):
        """Get statistics for a specific user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM calls WHERE user_id = ?', (user_id,))
        total_calls = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM calls WHERE user_id = ? AND is_scam = 1', (user_id,))
        scams_detected = cursor.fetchone()[0]
        
        cursor.execute('SELECT AVG(confidence) FROM calls WHERE user_id = ?', (user_id,))
        avg_confidence = cursor.fetchone()[0] or 0
        
        cursor.execute('''
            SELECT detected_threats FROM calls 
            WHERE user_id = ? AND is_scam = 1 
            ORDER BY timestamp DESC LIMIT 10
        ''', (user_id,))
        
        threat_counts = {}
        for row in cursor.fetchall():
            threats = json.loads(row[0])
            for threat in threats:
                threat_counts[threat] = threat_counts.get(threat, 0) + 1
        
        # Update user stats
        cursor.execute('''
            UPDATE users 
            SET total_calls_analyzed = ?, scams_blocked = ?
            WHERE id = ?
        ''', (total_calls, scams_detected, user_id))
        
        conn.commit()
        conn.close()
        
        return {
            'total_calls': total_calls,
            'scams_detected': scams_detected,
            'safe_calls': total_calls - scams_detected,
            'detection_rate': round((scams_detected / total_calls * 100) if total_calls > 0 else 0, 2),
            'average_confidence': round(avg_confidence, 2),
            'top_threats': threat_counts
        }
    
    def update_save_call(self, call_data, user_id=None):
        """Save analyzed call to database with user association"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO calls 
            (user_id, caller_name, caller_number, transcript, is_scam, confidence, 
             threat_level, detected_threats, redacted_transcript, detected_pii, 
             warning_message, duration, language)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            call_data.get('caller_name'),
            call_data.get('caller_number'),
            call_data.get('transcript'),
            call_data.get('is_scam'),
            call_data.get('confidence'),
            call_data.get('threat_level'),
            json.dumps(call_data.get('detected_threats', [])),
            call_data.get('redacted_transcript'),
            json.dumps(call_data.get('detected_pii', [])),
            call_data.get('warning_message'),
            call_data.get('duration', 0),
            call_data.get('language', 'en')
        ))
        
        conn.commit()
        call_id = cursor.lastrowid
        conn.close()
        return call_id

