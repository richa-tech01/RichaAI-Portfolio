import streamlit as st
from html import escape
from urllib.parse import quote, urlsplit
from modules.profile_loader import load_profile, RESUME_PATH
from modules.chatbot import answer_profile_question, ChatUnavailableError
from modules.resume_reader import extract_resume_text

st.set_page_config(
    page_title="Richa Singh | Professional Portfolio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Soft, minimal, responsive visual style
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
:root { color-scheme: light; }
.stApp { background: #F1F4F1; color: #1F3027; }
[data-testid="stHeader"] { background: rgba(241,244,241,.96); }
[data-testid="stMain"] { background: #F1F4F1; }
.block-container { max-width: 1120px; padding: 2rem 1.5rem 3rem; }
h1, h2, h3, h4 { color: #1F3027; font-weight: 700; }
h1 { font-family: 'Playfair Display', serif !important; }
h2, h3 { margin-top: 1.45rem; margin-bottom: .8rem; }
h3 { position: relative; padding-bottom: .55rem; }
h3::after { content: ''; position: absolute; left: 0; bottom: 0; width: 2.2rem;
             height: 3px; border-radius: 3px; background: #829586; }
p, li, [data-testid="stCaptionContainer"] { color: #68756D; }
.hero {
  background: linear-gradient(118deg,#E5EDE6 0%,#F3F0E9 100%);
  border: 1px solid #D9E2DA; border-radius: 22px;
  box-shadow: 0 8px 24px rgba(31,48,39,.07);
  padding: 2rem; margin: .5rem 0 1.3rem;
}
.eyebrow { color: #496B57; text-transform: uppercase; letter-spacing: 2px;
           font-size: .75rem; font-weight: 700; }
.hero-name { font-family: 'Playfair Display',serif; font-size: 2.8rem;
             color: #1F3027; font-weight: 700; line-height: 1.15; margin: .35rem 0; }
.hero-sub { color: #68756D; font-size: 1.04rem; line-height: 1.65; }
.hero-designation { color: #496B57; font-weight: 700; }
[data-testid="stPopoverButton"] {
  background:#DCE8DF !important; color:#365541 !important;
  border:1px solid #C8D9CC !important; border-radius:999px !important;
  padding:.38rem .75rem; font-size:.86rem; font-weight:600; min-height:2.4rem;
}
[data-testid="stPopoverButton"] p {
  color:#365541 !important; font-weight:600;
}
[data-testid="stPopoverButton"]:hover {
  background:#D2E2D6 !important; border-color:#829586 !important;
  color:#365541 !important;
}
.skill-pill { display:inline-block; background:#EAF0EA; color:#1F3027;
              border:1px solid #D9E2DA; border-radius:999px;
              padding:7px 12px; margin:4px 6px 4px 0; font-size:.88rem;
              font-weight:600; }
.project-skills-label { color:#496B57; font-size:.8rem; font-weight:700;
                        letter-spacing:.04em; margin:.8rem 0 .25rem; }
[data-testid="stMetric"] { background:#FFFFFF; border:1px solid #D9E2DA;
  box-shadow:0 4px 14px rgba(31,48,39,.06); padding:1rem 1.1rem;
  border-radius:16px; }
[data-testid="stMetricLabel"] { color:#68756D; font-weight:600; }
[data-testid="stMetricValue"] { color:#1F3027; font-weight:700; }
[data-testid="stVerticalBlock"][data-test-wrap="false"] {
  background:#FFFFFF; border:1px solid #D9E2DA; border-radius:16px;
  box-shadow:0 4px 14px rgba(31,48,39,.05); padding:1rem 1.1rem;
}
[role="tablist"] {
  gap:.25rem; border-bottom:1px solid #D9E2DA; flex-wrap:nowrap;
}
[role="tablist"] [data-testid="stTab"] {
  color:#68756D; font-weight:600; border-radius:10px 10px 0 0;
  padding:.65rem .9rem; border-bottom:3px solid transparent;
  transition:background-color .18s ease, color .18s ease;
}
[role="tablist"] [data-testid="stTab"]:hover {
  background:#E8EEE9; color:#365541;
}
[role="tablist"] [data-testid="stTab"][aria-selected="true"] {
  color:#365541; background:#DCE8DF; font-weight:700;
  border-bottom:3px solid #496B57;
}
[role="tablist"] [data-testid="stTab"][aria-selected="true"] [data-testid="stMarkdownContainer"] p {
  color:#365541 !important; font-weight:700 !important;
}
div.stButton > button, div.stDownloadButton > button,
[data-testid="stLinkButton"] a {
  border-radius:12px; border:1px solid #C9D8CC; min-height:2.65rem;
  transition:background-color .18s ease, border-color .18s ease, transform .18s ease;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
  border-color:#829586; color:#365541; transform:translateY(-1px);
}
[data-testid="stLinkButton"] a {
  background:#496B57; border-color:#496B57; color:#FFFFFF;
}
[data-testid^="stBaseLinkButton"] [data-testid="stMarkdownContainer"] p {
  color:#FFFFFF !important;
}
[data-testid="stLinkButton"] a:hover {
  background:#365541; border-color:#365541; color:#FFFFFF;
}
div.stDownloadButton > button {
  background:#496B57; border-color:#496B57; color:#FFFFFF;
  font-weight:700; min-height:3rem;
}
div.stDownloadButton > button:hover {
  background:#365541; border-color:#365541; color:#FFFFFF;
}
[data-testid="stChatMessage"] {
  background:#FFFFFF; border:1px solid #D9E2DA; border-radius:16px;
  padding:.65rem .9rem; margin:.45rem 0;
}
[data-testid="stChatInput"] textarea {
  border:1px solid #C9D8CC; border-radius:14px; background:#FFFFFF;
}
[data-testid="stChatInput"] textarea:focus {
  border-color:#496B57; box-shadow:0 0 0 2px rgba(73,107,87,.14);
}
[data-testid="stChatInput"] {
  background:rgba(241,244,241,.96);
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
  color:#1F3027;
}
@media (max-width: 760px) {
  .block-container { padding:1.2rem .85rem 2rem; }
  .hero { border-radius:18px; padding:1.4rem; }
  .hero-name { font-size:2.25rem; }
  [role="tablist"] { overflow-x:auto; }
  [role="tablist"] [data-testid="stTab"] { padding:.55rem .65rem; font-size:.82rem; }
}
@media (max-width: 480px) {
  .hero-name { font-size:1.9rem; }
  [data-testid="stMetric"] { padding:.8rem; }
}
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

try:
    profile = load_profile()
except (OSError, ValueError) as exc:
    st.error(f"Could not load your profile: {exc}")
    st.stop()

st.markdown(
    f"""
    <section class="hero">
      <div class="eyebrow">PERSONAL PORTFOLIO · AI / MACHINE LEARNING</div>
      <div class="hero-name">{escape(profile['name'])}</div>
      <div class="hero-sub">{escape(profile['headline']).replace('Associate AI/ML Engineer', '<span class="hero-designation">Associate AI/ML Engineer</span>')}</div>
      <div style="color:#68756D;margin-top:10px;">{escape(profile.get('location',''))}</div>
    </section>
    """,
    unsafe_allow_html=True,
)

col_a, col_b = st.columns([3, 1])
with col_a:
    linkedin_url = profile.get("linkedin_url", "")
    parsed_linkedin_url = urlsplit(linkedin_url) if isinstance(linkedin_url, str) else None
    if parsed_linkedin_url and parsed_linkedin_url.scheme == "https" and parsed_linkedin_url.netloc:
        st.link_button("Connect on LinkedIn", linkedin_url)
with col_b:
    with st.popover(profile.get("availability", ""), key="career_interest_popover"):
        st.markdown("### Career interests")
        st.write(" · ".join(profile.get("career_interests", [])))

tabs = st.tabs([
    "Overview", "Experience", "Education", "Skills",
    "Projects & Certifications", "Ask RichaAI", "Resume"
])

with tabs[0]:
    st.markdown("### A little about me")
    st.write(profile["about"])
    c1, c2, c3 = st.columns(3)
    c1.metric("Experience", profile.get("experience_summary", "—"))
    c2.metric("Education degrees", str(len(profile.get("education", []))))
    c3.metric("Key skill areas", f"{len(profile.get('skills', {}))}+")
    st.markdown("### Career interests")
    st.write(" · ".join(profile.get("career_interests", [])))

with tabs[1]:
    st.markdown("### Professional experience")
    for job in profile.get("experience", []):
        with st.container(border=True):
            st.subheader(job.get("role", "Role"))
            st.write(f"**{job.get('company','')}** · {job.get('employment_type','')}")
            details = " | ".join(x for x in [
                job.get("duration", ""), job.get("location", ""), job.get("project", "")
            ] if x)
            st.caption(details)
            for item in job.get("responsibilities", []):
                st.markdown(f"- {item}")

with tabs[2]:
    st.markdown("### Education")
    for item in profile.get("education", []):
        with st.container(border=True):
            st.subheader(item.get("degree", ""))
            if item.get("institution"):
                st.write(item["institution"])
            st.write(item.get("status", ""))
            if item.get("description"):
                st.write(item["description"])
            details = " | ".join(
                value for value in [item.get("duration", ""), item.get("location", "")]
                if value
            )
            if details:
                st.caption(details)
            if item.get("score"):
                st.markdown(f"**Grade:** {item['score']}")
            education_skills = item.get("skills", [])
            if education_skills:
                st.markdown('<div class="project-skills-label">Skills</div>', unsafe_allow_html=True)
                st.markdown(
                    "".join(
                        f'<span class="skill-pill">{escape(skill)}</span>'
                        for skill in education_skills
                    ),
                    unsafe_allow_html=True,
                )

with tabs[3]:
    st.markdown("### Key Skills")
    for category, skills in profile.get("skills", {}).items():
        st.markdown(f"**{escape(category)}**")
        st.markdown(
            "".join(
                f'<span class="skill-pill">{escape(skill)}</span>'
                for skill in skills
            ),
            unsafe_allow_html=True,
        )

with tabs[4]:
    st.markdown("### Projects")
    projects = profile.get("projects", [])
    if projects:
        for project in projects:
            with st.container(border=True):
                st.subheader(project.get("name", "Project"))
                metadata = " · ".join(
                    value
                    for value in [
                        project.get("organization", ""),
                        project.get("location", ""),
                        project.get("duration", ""),
                    ]
                    if value
                )
                if metadata:
                    st.caption(metadata)
                st.write(project.get("description", ""))
                project_skills = project.get("skills", [])
                if project_skills:
                    st.markdown('<div class="project-skills-label">Skills</div>', unsafe_allow_html=True)
                    st.markdown(
                        "".join(
                            f'<span class="skill-pill">{escape(skill)}</span>'
                            for skill in project_skills
                        ),
                        unsafe_allow_html=True,
                    )
    else:
        st.info("Projects will be added soon.")

    st.markdown("### Certifications")
    certs = profile.get("certifications", [])
    if certs:
        month_abbreviations = {
            "January": "Jan", "February": "Feb", "March": "Mar",
            "April": "Apr", "May": "May", "June": "Jun",
            "July": "Jul", "August": "Aug", "September": "Sep",
            "October": "Oct", "November": "Nov", "December": "Dec",
        }
        certification_lines = []
        for cert in certs:
            if isinstance(cert, str):
                certification_lines.append(f"- {cert}")
                continue
            name = cert.get("name", "Certification")
            issuer = cert.get("issuer", "")
            issue_date = cert.get("issue_date", "")
            if issue_date:
                date_parts = issue_date.split(maxsplit=1)
                if len(date_parts) == 2:
                    month, year = date_parts
                    issue_date = f"{month_abbreviations.get(month, month)} {year}"
            line = f"**{escape(name)}**"
            if issuer:
                line += f" — {escape(issuer)}"
            if issue_date:
                line += f" ({escape(issue_date)})"
            credential_url = cert.get("credential_url", "")
            parsed_url = urlsplit(credential_url) if isinstance(credential_url, str) else None
            if parsed_url and parsed_url.scheme == "https" and parsed_url.netloc:
                safe_url = quote(credential_url, safe=":/?#[]@!$&'*+,;=%")
                line += f" · [View Certificate]({safe_url})"
            certification_lines.append(f"- {line}")
        st.markdown("\n".join(certification_lines))
    else:
        st.caption("Certifications have not been added yet.")

with tabs[5]:
    st.markdown("### Ask RichaAI")
    st.write(
        "Recruiters can ask questions about Richa's professional experience, "
        "education, skills and projects. Answers use the profile information "
        "published on this website."
    )

    examples = [
        "Could you introduce Richa?",
        "What is her professional experience?",
        "Which computer vision skills does she have?",
        "What are her educational qualifications?",
        "What roles is she interested in?",
    ]
    button_cols = st.columns(2)
    for idx, prompt in enumerate(examples):
        if button_cols[idx % 2].button(
            prompt, key=f"example_{idx}", use_container_width=True
        ):
            st.session_state["portfolio_question"] = prompt

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = st.chat_input("Ask a professional question about Richa...")
    if st.session_state.get("portfolio_question"):
        question = st.session_state.pop("portfolio_question")

    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        resume_text = ""
        if RESUME_PATH.is_file():
            try:
                resume_text = extract_resume_text(RESUME_PATH.read_bytes())
            except (OSError, RuntimeError):
                st.error(
                    "The resume PDF could not be read. RichaAI will answer "
                    "using the profile information only."
                )

        with st.chat_message("assistant"):
            with st.spinner("Preparing an answer..."):
                try:
                    answer = answer_profile_question(
                        profile, question, resume_text=resume_text
                    )
                except ChatUnavailableError as exc:
                    answer = str(exc)
                    st.info(answer)
                else:
                    st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

with tabs[6]:
    st.markdown("### Resume")
    if RESUME_PATH.exists():
        pdf_bytes = RESUME_PATH.read_bytes()
        st.success("Resume PDF is ready.")
        st.download_button(
            "Download Richa's resume",
            data=pdf_bytes,
            file_name="Richa_Singh_Resume.pdf",
            mime="application/pdf",
            use_container_width=True,
        )
    else:
        st.info("Add your latest PDF at assets/resume.pdf to enable the download button.")

    st.markdown("### Preview PDF text")
    uploaded_pdf = st.file_uploader(
        "Upload a PDF to extract its text for checking",
        type=["pdf"],
        key="pdf_check",
    )
    if uploaded_pdf:
        try:
            extracted = extract_resume_text(uploaded_pdf.getvalue())
            st.text_area("Extracted text", extracted, height=260)
        except (OSError, RuntimeError):
            st.error("Could not read this PDF. Please check the file and try again.")

st.divider()
st.caption("Richa Singh · Professional Portfolio · Profile information supplied by the owner.")
