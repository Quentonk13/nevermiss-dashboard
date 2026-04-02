#!/usr/bin/env python3
"""
NeverMiss Twilio Handler
- Listens for incoming calls
- Detects missed calls
- Sends auto SMS reply
"""

import os
import json
from flask import Flask, request, Response

app = Flask(__name__)

# Configuration
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')
REPLY_MESSAGE = os.environ.get('REPLY_MESSAGE', 'Thanks for calling! We\'ll text you back shortly. - NeverMiss')

@app.route('/webhook/call', methods=['POST'])
def handle_call():
    """Handle incoming call status callbacks"""
    call_status = request.form.get('CallStatus')
    from_number = request.form.get('From')
    call_sid = request.form.get('CallSid')
    
    print(f"[CALL] Status: {call_status} | From: {from_number} | SID: {call_sid}")
    
    # Log to database
    log_call(call_sid, from_number, call_status)
    
    # If missed call, send SMS
    if call_status == 'no-answer' or call_status == 'busy' or call_status == 'failed':
        send_auto_reply(from_number)
    
    return Response('', status=200)

@app.route('/webhook/sms', methods=['POST'])
def handle_sms():
    """Handle incoming SMS"""
    from_number = request.form.get('From')
    body = request.form.get('Body')
    
    print(f"[SMS] From: {from_number} | Body: {body}")
    
    # Log to database
    log_sms(from_number, body)
    
    # Forward to owner
    forward_to_owner(from_number, body)
    
    return Response('', status=200)

def send_auto_reply(to_number):
    """Send automatic SMS reply to missed caller"""
    import requests
    
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("[ERROR] Twilio credentials not set")
        return False
    
    url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
    
    data = {
        'To': to_number,
        'From': TWILIO_PHONE_NUMBER,
        'Body': REPLY_MESSAGE
    }
    
    auth = (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    try:
        response = requests.post(url, data=data, auth=auth)
        if response.status_code == 201:
            print(f"[SMS] Auto-reply sent to {to_number}")
            return True
        else:
            print(f"[ERROR] Failed to send SMS: {response.text}")
            return False
    except Exception as e:
        print(f"[ERROR] Exception sending SMS: {e}")
        return False

def log_call(call_sid, from_number, status):
    """Log call to database"""
    import sqlite3
    from datetime import datetime
    
    try:
        conn = sqlite3.connect('/app/data/nevermiss.db')
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO calls (call_sid, from_number, status, created_at)
            VALUES (?, ?, ?, ?)
        """, (call_sid, from_number, status, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to log call: {e}")

def log_sms(from_number, body):
    """Log incoming SMS"""
    import sqlite3
    from datetime import datetime
    
    try:
        conn = sqlite3.connect('/app/data/nevermiss.db')
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO sms_log (from_number, body, direction, created_at)
            VALUES (?, ?, 'inbound', ?)
        """, (from_number, body, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to log SMS: {e}")

def forward_to_owner(from_number, body):
    """Forward SMS to owner via Telegram"""
    # This will be handled by the main bot
    print(f"[FORWARD] SMS from {from_number}: {body}")

def init_db():
    """Initialize database tables"""
    import sqlite3
    
    conn = sqlite3.connect('/app/data/nevermiss.db')
    cur = conn.cursor()
    
    # Calls table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            call_sid TEXT,
            from_number TEXT,
            status TEXT,
            created_at TEXT
        )
    """)
    
    # SMS log table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sms_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_number TEXT,
            body TEXT,
            direction TEXT,
            created_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print("[DB] Database initialized")

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)