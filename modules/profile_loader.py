import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROFILE_PATH = PROJECT_ROOT / "data" / "profile.json"
RESUME_PATH = PROJECT_ROOT / "assets" / "resume.pdf"


def load_profile():
    if not PROFILE_PATH.exists():
        raise FileNotFoundError("data/profile.json was not found.")

    with PROFILE_PATH.open("r", encoding="utf-8") as file:
        profile = json.load(file)

    if not isinstance(profile, dict):
        raise ValueError("data/profile.json must contain a JSON object.")

    required = ["name", "headline", "about", "skills"]
    missing = [field for field in required if not profile.get(field)]
    if missing:
        raise ValueError(f"Missing required profile fields: {', '.join(missing)}")
    for field in ("name", "headline", "about"):
        if not isinstance(profile[field], str):
            raise ValueError(f"The {field} field in data/profile.json must be text.")
    if not isinstance(profile["skills"], dict):
        raise ValueError("The skills field in data/profile.json must be an object.")
    if not all(
        isinstance(category, str)
        and isinstance(items, list)
        and all(isinstance(item, str) for item in items)
        for category, items in profile["skills"].items()
    ):
        raise ValueError("Skills must map text categories to lists of text values.")

    optional_defaults = {
        "location": "",
        "availability": "",
        "experience_summary": "—",
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
        "career_interests": [],
    }
    for field, default in optional_defaults.items():
        if profile.get(field) is None:
            profile[field] = default

    for field in ("experience", "education", "projects", "certifications", "career_interests"):
        if not isinstance(profile[field], list):
            raise ValueError(f"The {field} field in data/profile.json must be a list.")
    if not all(isinstance(item, dict) for item in profile["experience"]):
        raise ValueError("Each experience entry in data/profile.json must be an object.")
    if not all(isinstance(item, dict) for item in profile["education"]):
        raise ValueError("Each education entry in data/profile.json must be an object.")
    if not all(isinstance(item, dict) for item in profile["projects"]):
        raise ValueError("Each project entry in data/profile.json must be an object.")
    if not all(isinstance(item, (str, dict)) for item in profile["certifications"]):
        raise ValueError("Each certification entry must be text or an object.")
    if not all(isinstance(item, str) for item in profile["career_interests"]):
        raise ValueError("Each career interest in data/profile.json must be text.")
    return profile
