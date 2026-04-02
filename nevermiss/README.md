# NeverMiss Twilio Integration

## Overview
Replaces OpenPhone with Twilio for missed-call text-back automation.

## Setup

### 1. Get Twilio Credentials
- Sign up at twilio.com
- Get Account SID and Auth Token from console
- Buy a phone number (~$1/mo)

### 2. Set Environment Variables
In Railway:
- `TWILIO_ACCOUNT_SID` = your account SID
- `TWILIO_AUTH_TOKEN` = your auth token  
- `TWILIO_PHONE_NUMBER` = your Twilio phone number (e.g., +15551234567)

### 3. Configure Webhooks
In Twilio Console → Phone Numbers → Your Number:
- Voice URL: `https://your-app.railway.app/webhook/call`
- Messaging URL: `https://your-app.railway.app/webhook/sms`

## How It Works

1. **Incoming call** → Twilio sends status callback to `/webhook/call`
2. **If missed** (`no-answer`, `busy`, `failed`) → Auto-reply SMS sent
3. **Incoming SMS** → Logged to database and forwarded to owner

## Deploy

```bash
# Or deploy via Railway dashboard by linking the /nevermiss/ folder
```

## Reply Message
Default: "Thanks for calling! We'll text you back shortly. - NeverMiss"

Override with `REPLY_MESSAGE` env var.