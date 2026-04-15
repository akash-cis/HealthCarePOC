# Clinical Call Intelligence Pipeline

An end-to-end AI-powered Medical Call processing pipeline that takes raw clinical transcripts, extracts actionable insights via Groq (LLaMA-3.3-70b), and securely pushes the structured data into Salesforce as an **Opportunity**.

This system features a premium, responsive glassmorphism web interface served natively via a Python **FastAPI** backend with automated **PKCE OAuth** security.

---

## 🏗️ Architecture Flow

1. **Frontend (Vanilla HTML/CSS/JS):** A sleek GUI served by FastAPI allows users to review the localized mock clinical transcript.
2. **AI Processing Engine (Groq):** An API request forces `llama-3.3-70b-versatile` to process the transcript using strict JSON schema adherence to extract Clinical Summaries, Action Items, and Sentiment.
3. **Salesforce OAuth (PKCE Flow):** Natively redirects the user to the Salesforce login wall, handles the Authorization Code Grant, and securely caches an `sf_token.json`.
4. **Data Sync:** Post API payload directly to Salesforce (`/services/data/v58.0/sobjects/Opportunity/`), creating a new Salesforce Opportunity containing the summarized metrics.

---

## 🚀 Setup Instructions

### 1. Environment Config
Create a `.env` file in the project's root folder utilizing the `.env.example` file. You must provide:
```bash
# Groq
GROQ_API_KEY=your_groq_api_key

# Salesforce
SALESFORCE_INSTANCE_URL=https://your-org.develop.my.salesforce.com
SALESFORCE_CONSUMER_KEY=your_connected_app_client_id
SALESFORCE_CONSUMER_SECRET=your_connected_app_secret
```

### 2. Salesforce Connected App Configuration
To properly securely route authentication, you must configure a Connected App inside Salesforce:
- Navigate to **Setup -> App Manager -> New Connected App**.
- Enable OAuth Settings.
- **Callback URL MUST exact match:** `http://localhost:8000/auth/salesforce/callback`
- **Selected OAuth Scopes:** 
  1. `Manage user data via APIs (api)`
  2. `Perform requests at any time (refresh_token, offline_access)`
- *CRITICAL:* After saving, wait ~10 minutes for Salesforce to propagate the new Redirect URI internally.

---

## 🧪 Testing Steps

Everything runs seamlessly via the local Uvicorn server utilizing the mock transcript.

### Step 1: Start the Backend Server
Run the FastAPI application locally:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 2: Acquire Salesforce OAuth Token
Before pushing data, the script must verify identity. 
- Open your browser and navigate to: `http://localhost:8000/auth/salesforce/login`
- The screen will seamlessly route you through Salesforce's secure login framework (generating a PKCE Challenge automatically in Python).
- Click **"Allow Access"**.
- You will be sent back to a success screen stating `Success! Token securely saved`. A `sf_token.json` file is now secretly cached in your project root!

### Step 3: Run the User Interface (The Demo!)
With the token securely in hand, open the premium Web Demo:
- Navigate to: `http://localhost:8000/`

**Execution Flow within the App:**
1. **Analyze Transcript:** Review the generated simulated Zoom recording transcript on screen.
2. **Summarize Call:** Click the `✨ Analyze Call via Groq AI (Llama-3.3)` button. The AI will spin up, process the clinical data, and dynamically display the predicted Sentiment Analysis and Markdown-formatted Clinical Summary output.
3. **Push to Salesforce:** Click the `☁️ Seamlessly Push Opportunity to Salesforce` button on the bottom. The Python backend will pass the OAuth packet and create a new **Opportunity**.

### Step 4: Verification
Log into your Salesforce instance, navigate to the **Opportunities** Tab, and look for an Opportunity named **"Call Intelligence: WEB-DEMO-UI-102"**.
Open it and review the beautifully organized AI data stored inside the **Description** field!
# HealthCarePOC
