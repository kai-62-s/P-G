# P&G Performance Dashboard

An interactive dashboard analyzing Procter & Gamble's financial performance (FY2021–FY2026)
and progress toward its public Ambition 2030 sustainability goals, built from P&G's own
Annual Reports and Ambition 2030 Mid-Point Progress Update.

**Live demo:** _add your deployed Streamlit Cloud link here once deployed_

## What's inside

- **Financial Performance** — 6-year trend in net sales, EPS, operating cash flow, and
  margins, pulled from P&G's audited Consolidated Statements of Earnings.
- **Ambition 2030 Sustainability** — progress toward all 16 of P&G's public 2030
  environmental goals (Climate, Waste, Water, Nature), with a multi-year trend view.
- **Segment & Geographic Mix** — where P&G's revenue and earnings come from, by
  business segment and region.

All data lives in `data/*.csv` and is sourced directly from P&G's public filings —
see the in-app captions for exact page/report citations.

## Run it locally

```bash
git clone https://github.com/<your-username>/pg-dashboard.git
cd pg-dashboard
pip install -r requirements.txt
streamlit run app.py
```

This opens the dashboard at `http://localhost:8501`.

## Deploy it for free (Streamlit Community Cloud)

1. **Push this folder to a new GitHub repo.**
   ```bash
   cd pg-dashboard
   git init
   git add .
   git commit -m "Initial commit: P&G performance dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/pg-dashboard.git
   git push -u origin main
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.

3. Click **"New app"**, select this repo, branch `main`, and file path `app.py`.

4. Click **Deploy**. Streamlit Cloud installs `requirements.txt` automatically and gives
   you a live URL like `https://<your-app-name>.streamlit.app` within a minute or two.

5. **Add that link to your résumé/CV** — e.g.:
   > Built and deployed an interactive dashboard analyzing P&G's financial performance
   > and sustainability progress against its public 2030 goals (Python, Streamlit,
   > Plotly) — [live link]

Any time you push a new commit to `main`, Streamlit Cloud auto-redeploys.

## Data sources

- P&G Annual Report, Fiscal Year 2025
- P&G Annual Report, Fiscal Year 2026
- P&G Ambition 2030: A Mid-Point Update on Our Environmental Sustainability Progress
  and Path Forward (August 2025)

## Disclaimer

This is an independent analysis built from P&G's public filings and reports. It is not
affiliated with, endorsed by, or produced in partnership with Procter & Gamble.
