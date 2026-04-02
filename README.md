# What's Your Internet Era?

A viral quiz app that diagnoses your relationship with the internet. 8 questions, 8 personality eras, shareable results.

**Architecture:**
- Frontend: Static HTML/JS/CSS (deployed on Cloudflare Pages — FREE, no sleep)
- Backend: FastAPI + OpenAI (deployed on Google Cloud Run — $0 until scale)

## Quick Deploy (20 minutes)

### Step 1: Google Cloud Setup (5 min)

1. Go to console.cloud.google.com
2. Create a new project (e.g., "internet-era-12345")
3. Open Cloud Shell (terminal icon at top right)
4. Run these commands:

```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com

# Create service account
gcloud iam service-accounts create internet-era \
  --display-name="Internet Era Backend"

# Set environment variables
export GCP_PROJECT_ID=your-project-id-here  # REPLACE with your actual project ID
export OPENROUTER_API_KEY=sk-or-v1-...       # Your OpenRouter API key

# Deploy backend using the deploy script
chmod +x deploy.sh
./deploy.sh
```

### Step 2: Cloudflare Pages Setup (5 min)

1. Go to dash.cloudflare.com
2. Go to Workers & Pages > Create Application > Pages
3. Connect your GitHub repo (push this project to GitHub first)
4. Build settings:
   - Build command: leave empty (static site)
   - Build output directory: `static`
5. Deploy

### Step 3: Connect Frontend to Backend (2 min)

After Cloud Run deploys, it gives you a URL like:
`https://internet-era-xxxxx-uc.a.run.app`

Open `static/index.html`, find the `const API` line:
```javascript
const API = 'https://internet-era-xxxxx-uc.a.run.app/analyze';
```

### Step 4: Custom Domain (optional, $10/year)

1. Buy domain on Cloudflare Registrar
2. In Cloudflare Pages > Custom domains > Add domain
3. Points to your Pages site automatically

## Local Development

```bash
# Backend
cd backend
export OPENROUTER_API_KEY=sk-or-v1-...
uvicorn main:app --reload --port 8001

# Frontend
# Just open static/index.html in browser
# Or: python3 -m http.server 8080 --directory static
```

## API Reference

**POST /analyze**
```json
{
  "answers": [0, 2, 1, 3, 0, 2, 1, 0],
  "name": ""
}
```

Response includes era name, emoji, colors, gradient, description, tagline, aesthetic, spirit website, spirit animal, trait scores, AI-generated roast, horoscope, and advice.

## Cost Breakdown

- Cloudflare Pages: $0 (free forever)
- Cloud Run: $0 for first ~2M requests/month
- OpenRouter API: ~$0.0003 per quiz (100K users = $30)
- Domain: $10/year (optional)

**Total to launch: $10**
**100K users: approximately $30**

## Monitization Ideas

1. Extended vibe report ($3 unlock)
2. Sponsored results (brand placements in "Spirit Website" field)
3. Premium shareable cards ($1-2)
4. Cross-promote with other quiz apps
