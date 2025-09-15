# LinkedIn AI Auto Poster

This project automatically posts **daily Artificial Intelligence news** to your LinkedIn profile at **09:00 IST** using GitHub Actions.

---

## 📌 Features
- Fetches AI news from **NewsAPI** (with RSS fallback if no API key).
- Posts automatically to LinkedIn using the UGC API.
- Runs daily at **09:00 IST** (03:30 UTC).
- Can also be triggered manually from GitHub Actions.

---

## 🚀 Setup

1. **Create LinkedIn Developer App**
   - Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps).
   - Add a Redirect URI (example: `https://example.com/oauth-callback`).
   - Request scopes: `w_member_social r_liteprofile`.
   - Save your **Client ID** and **Client Secret**.

2. **Get an Access Token**
   - Follow instructions in `get_token_instructions.txt`.
   - Save the `access_token` into GitHub Secrets as `LINKEDIN_ACCESS_TOKEN`.

3. **Get NewsAPI key** (optional, improves quality).
   - Register at [https://newsapi.org](https://newsapi.org).
   - Save it in GitHub Secrets as `NEWSAPI_KEY`.

4. **Add GitHub Secrets**
   - In your repo → Settings → Secrets and variables → Actions.
   - Add:
     - `LINKEDIN_ACCESS_TOKEN`
     - `NEWSAPI_KEY` (optional)
     - `PROFILE_URN` (optional, e.g., `urn:li:person:xxxx`)

5. **Workflow**
   - GitHub Actions workflow file is in `.github/workflows/daily_post.yml`.
   - It runs daily at 09:00 IST.

---

## ⚡ Local Testing
Create a `.env` file:
Run locally:
---

## ⚠️ Notes
- LinkedIn tokens expire (often 60 days). You’ll need to refresh or re-generate tokens.
- Avoid spammy behavior — personalize posts when possible.
- You can switch fully to RSS feeds if you don’t want to use NewsAPI.
