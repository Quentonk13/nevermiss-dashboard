# NeverMiss n8n Workflows

Import these into your n8n instance at https://nevermiss-ops-production.up.railway.app

## Available Workflows

### 1. Lead Capture (`lead-capture.json`)
- Fetches leads from Apollo.io every 15 minutes
- Processes and deduplicates leads
- Saves to PostgreSQL database

### 2. Email Outreach (`email-outreach.json`)
- Runs every hour
- Gets new leads from database
- Sends personalized outreach emails
- Marks leads as contacted

### 3. Social Poster (`social-poster.json`)
- Runs every 4 hours
- Posts to Twitter and Bluesky
- Marks content as posted in queue

### 4. Payment Alerts (`payment-alerts.json`)
- Stripe webhook receiver
- Alerts you when payments succeed
- Logs revenue to database
- Sends welcome email to new customers

### 5. Reply Handler (`reply-handler.json`)
- Watches inbox for lead replies
- Detects "demo" requests → sends calendar link
- Detects "interested" → personal follow-up
- Alerts you of hot leads

## Setup Required

1. **Credentials needed in n8n:**
   - PostgreSQL (for leads, content_queue, revenue tables)
   - Gmail API (for sending/receiving email)
   - Twitter API
   - Bluesky API
   - Stripe webhook URL

2. **Environment variables:**
   - `APOLLO_API_KEY`
   - `DATABASE_URL`
   - `GMAIL_USER` / `GMAIL_APP_PASSWORD`
   - `TWITTER_API_KEY` / `TWITTER_API_SECRET`
   - `BLUESKY_APP_PASSWORD`
   - `STRIPE_WEBHOOK_SECRET`

## Database Schema

```sql
CREATE TABLE leads (
  id SERIAL PRIMARY KEY,
  name TEXT,
  email TEXT UNIQUE,
  phone TEXT,
  company TEXT,
  source TEXT,
  status TEXT DEFAULT 'new',
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE content_queue (
  id SERIAL PRIMARY KEY,
  content TEXT,
  platform TEXT,
  status TEXT DEFAULT 'pending',
  scheduled_at TIMESTAMP,
  posted_at TIMESTAMP
);

CREATE TABLE revenue (
  id SERIAL PRIMARY KEY,
  amount DECIMAL,
  customer_email TEXT,
  stripe_invoice TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## Import Workflows

1. Open n8n at https://nevermiss-ops-production.up.railway.app
2. Click "Import from File"
3. Select a workflow JSON file
4. Configure credentials
5. Activate