# RichaAI – Personal Resume Portfolio + AI Chatbot

A responsive Streamlit portfolio with an AI assistant that answers using the public profile and, when provided, the public resume PDF.

## Local setup (Python 3.12)

Open PowerShell in this folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For local chatbot access, copy `.env.example` to `.env` and add your own OpenAI API key:

```env
OPENAI_API_KEY=your_real_api_key
OPENAI_MODEL=gpt-4.1-mini
```

Never put a real key in `.env.example`, source files, or GitHub. The `.env` file and Streamlit secrets file are ignored by Git.

Run the app:

```powershell
python -m streamlit run app.py
```

The portfolio remains available without an API key. In that case, the chatbot shows a friendly unavailable message. OpenAI API usage may be billed separately; set usage limits and monitor your account.

## Public profile and resume

Edit `data/profile.json` to update the professional profile. This file is displayed publicly when the site is deployed.

To enable resume downloads and allow the chatbot to use resume text, place a PDF you are comfortable publishing at `assets/resume.pdf`. A deployed resume is downloadable by anyone with the site URL. No resume PDF is currently included in this repository.

Do not publish private contact details, home addresses, passwords, API keys, identity documents, or other information you do not intend to make public.

## Deploy to Streamlit Community Cloud

1. Sign in to GitHub and create or select a repository named `RichaAI-Portfolio`. Choose **Public** if anyone should be able to access the source; the deployed app can be public independently of the source repository setting.
2. Upload the reviewed project files to the repository's `main` branch. Include the app, `modules/`, `data/profile.json`, `.streamlit/config.toml`, `requirements.txt`, `README.md`, `.gitignore`, and the placeholder-only `.env.example`. Exclude `.venv/`, all `__pycache__/`, `.env`, `.streamlit/secrets.toml`, editor files, logs, temporary files, and `assets/ADD_YOUR_RESUME_HERE.txt`. Only add `assets/resume.pdf` if you have verified it is safe for public download.
3. In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**, connect GitHub, and select the `main` branch and `app.py` as the main file.
4. In the app's **Settings → Secrets**, add your key securely:

   ```toml
   OPENAI_API_KEY = "your_real_api_key"
   OPENAI_MODEL = "gpt-4.1-mini"
   ```

   Do not add these values to GitHub. If no key is configured, the portfolio still runs and the chatbot displays its unavailable message.

5. In the app's **Settings → General**, select Python 3.12 if available, then deploy.
6. Open the public HTTPS URL shown by Streamlit. Test all tabs, the chatbot, and the resume button (if a public PDF was included). Check the URL on a phone/tablet and from another device or network.

Visitors need only the public URL; your computer does not need to stay on. Streamlit Community Cloud hosts the application.

## Project files

| Purpose | File |
|---|---|
| Streamlit application | `app.py` |
| Public profile, experience, education, projects, certificates | `data/profile.json` |
| AI answers and secure configuration lookup | `modules/chatbot.py` |
| Profile and resume paths | `modules/profile_loader.py` |
| PDF text extraction | `modules/resume_reader.py` |
| Dependencies | `requirements.txt` |
| Public theme | `.streamlit/config.toml` |
| Local environment template (placeholder only) | `.env.example` |

## Privacy and chatbot behavior

- The chatbot is instructed to answer only from the supplied profile and optional resume text and to say when information is not included.
- Do not upload a resume or certificate image unless it is yours and intended for public viewing.
- A public chatbot may incur API charges. Set API usage limits and monitor usage.
- Uploaded resume text is sent to OpenAI when needed to answer a chatbot question; do not include sensitive information in a public resume.
