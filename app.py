import streamlit as st
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="CivicBridge AI",
    page_icon="🌉",
    layout="wide"
)

# -----------------------------
# Sample scheme knowledge base
# -----------------------------

schemes = [
    {
        "name": "PM-KISAN",
        "description": "Financial support for eligible farmers and agricultural families.",
        "occupation": ["farmer", "agriculture", "agricultural"],
        "max_income": 500000,
        "min_age": 18,
        "benefit": "Income support for eligible farmer families.",
        "documents": ["Aadhaar", "Land records", "Bank account"],
        "category": "Farmer"
    },
    {
        "name": "PM Fasal Bima Yojana",
        "description": "Crop insurance support for farmers against crop loss and agricultural risks.",
        "occupation": ["farmer", "agriculture", "agricultural"],
        "max_income": 1000000,
        "min_age": 18,
        "benefit": "Crop insurance and financial protection.",
        "documents": ["Aadhaar", "Land records", "Bank account"],
        "category": "Farmer"
    },
    {
        "name": "Post-Matric Scholarship",
        "description": "Financial assistance for eligible students pursuing education after school.",
        "occupation": ["student", "college student"],
        "max_income": 300000,
        "min_age": 16,
        "benefit": "Educational financial assistance.",
        "documents": ["Aadhaar", "Income certificate", "Student ID"],
        "category": "Student"
    },
    {
        "name": "PMAY-Gramin",
        "description": "Housing assistance for eligible rural households.",
        "occupation": ["farmer", "worker", "labourer", "agriculture"],
        "max_income": 300000,
        "min_age": 18,
        "benefit": "Support towards construction of a rural house.",
        "documents": ["Aadhaar", "Income certificate", "Address proof"],
        "category": "Rural Household"
    },
    {
        "name": "PM-SYM",
        "description": "Pension support for eligible unorganised workers with limited income.",
        "occupation": ["worker", "labourer", "self employed", "shopkeeper"],
        "max_income": 180000,
        "min_age": 18,
        "max_age": 40,
        "benefit": "Pension support for eligible unorganised workers.",
        "documents": ["Aadhaar", "Bank account"],
        "category": "Worker"
    },
    {
        "name": "National Means-cum-Merit Scholarship",
        "description": "Scholarship assistance for eligible students to continue secondary education.",
        "occupation": ["student", "school student"],
        "max_income": 350000,
        "min_age": 10,
        "benefit": "Financial assistance for education.",
        "documents": ["Income certificate", "Student ID", "Bank account"],
        "category": "Student"
    }
]


# -----------------------------
# Voice/profile extraction
# -----------------------------

def extract_profile(text):
    text_lower = text.lower()

    profile = {
        "age": None,
        "income": None,
        "occupation": "",
        "raw_text": text
    }

    # Age
    age_match = re.search(r'(\d{1,3})\s*(?:years?|yrs?|வயது|வயசு)', text_lower)
    if age_match:
        profile["age"] = int(age_match.group(1))

    # Income
    income_match = re.search(
        r'(?:income|வருமானம்).*?(\d[\d,]*)',
        text_lower
    )

    if income_match:
        profile["income"] = int(income_match.group(1).replace(",", ""))

    # Occupation
    occupation_map = {
        "farmer": ["farmer", "farming", "agriculture", "விவசாயி", "விவசாயம்"],
        "student": ["student", "college", "school", "மாணவர்", "மாணவி"],
        "worker": ["worker", "labour", "labor", "தொழிலாளி"],
        "shopkeeper": ["shopkeeper", "shop", "கடை"],
        "self employed": ["self employed", "business", "சுய தொழில்"]
    }

    for occupation, keywords in occupation_map.items():
        if any(keyword in text_lower for keyword in keywords):
            profile["occupation"] = occupation
            break

    # Tamil number example: "80 ஆயிரம்"
    thousand_match = re.search(r'(\d+)\s*(?:ஆயிரம்|thousand)', text_lower)

    if thousand_match and profile["income"] is None:
        profile["income"] = int(thousand_match.group(1)) * 1000

    return profile


# -----------------------------
# AI-style scheme matching
# -----------------------------

def match_schemes(profile):
    profile_text = (
        f"{profile['occupation']} "
        f"{profile['age'] or ''} "
        f"{profile['income'] or ''}"
    )

    scheme_texts = [
        f"{s['name']} {s['description']} {s['category']} "
        f"{' '.join(s['occupation'])}"
        for s in schemes
    ]

    documents = [profile_text] + scheme_texts

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(matrix[0:1], matrix[1:]).flatten()

    results = []

    for i, scheme in enumerate(schemes):

        score = float(similarity[i]) * 100
        reasons = []
        missing = []

        # Occupation match
        if profile["occupation"] in scheme["occupation"]:
            score += 40
            reasons.append(
                f"Occupation matches the scheme's target group ({scheme['category']})."
            )

        # Age
        if profile["age"] is not None:
            if profile["age"] >= scheme["min_age"]:
                reasons.append("Age requirement appears to be satisfied.")
            else:
                score -= 40
                reasons.append("Age requirement may not be satisfied.")

            if "max_age" in scheme and profile["age"] > scheme["max_age"]:
                score -= 40
                reasons.append("Age is above the stated maximum.")

        # Income
        if profile["income"] is not None:
            if profile["income"] <= scheme["max_income"]:
                score += 20
                reasons.append("Income is within the prototype threshold.")
            else:
                score -= 30
                reasons.append("Income appears to exceed the prototype threshold.")

        # Documents
        for doc in scheme["documents"]:
            missing.append(doc)

        results.append({
            "scheme": scheme,
            "score": max(0, min(100, score)),
            "reasons": reasons,
            "missing": missing
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results


# -----------------------------
# Interface
# -----------------------------

st.title("🌉 CivicBridge AI")
st.subheader("Bridging Citizens to the Benefits They Deserve")

st.write(
    "An AI-powered, voice-first citizen benefits navigator "
    "for discovering government schemes and understanding eligibility."
)

st.divider()

st.markdown("### 🎙️ Tell CivicBridge about yourself")

st.info(
    "Example: எனக்கு 52 வயசு. நான் விவசாயம் செய்கிறேன். "
    "எனக்கு வருட வருமானம் 80 ஆயிரம்."
)

voice_text = st.text_area(
    "Voice transcript / citizen statement",
    placeholder="Type or paste what the citizen would say...",
    height=120
)

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=0, max_value=120, value=0)

with col2:
    income = st.number_input(
        "Annual income (₹)",
        min_value=0,
        value=0,
        step=10000
    )

occupation = st.selectbox(
    "Occupation",
    [
        "",
        "farmer",
        "student",
        "worker",
        "shopkeeper",
        "self employed"
    ]
)

if st.button("🔎 Find Relevant Schemes", type="primary"):

    if voice_text.strip():
        profile = extract_profile(voice_text)
    else:
        profile = {
            "age": age if age > 0 else None,
            "income": income if income > 0 else None,
            "occupation": occupation,
            "raw_text": ""
        }

    # Manual fields override extracted values
    if age > 0:
        profile["age"] = age

    if income > 0:
        profile["income"] = income

    if occupation:
        profile["occupation"] = occupation

    st.divider()

    st.markdown("### 👤 Citizen Profile")

    p1, p2, p3 = st.columns(3)

    p1.metric("Age", profile["age"] or "Not provided")
    p2.metric(
        "Annual Income",
        f"₹{profile['income']:,}" if profile["income"] else "Not provided"
    )
    p3.metric(
        "Occupation",
        profile["occupation"].title() if profile["occupation"] else "Not provided"
    )

    results = match_schemes(profile)

    st.markdown("### 🎯 Potentially Relevant Schemes")

    for result in results[:4]:

        scheme = result["scheme"]

        with st.container(border=True):

            st.markdown(f"## {scheme['name']}")

            st.progress(
                int(result["score"]),
                text=f"Relevance score: {result['score']:.0f}%"
            )

            st.write(scheme["description"])

            st.success(
                f"Potential benefit: {scheme['benefit']}"
            )

            if result["reasons"]:
                st.markdown("**Why this may match:**")

                for reason in result["reasons"]:
                    st.write("✓ " + reason)

            st.markdown("**Documents commonly required:**")

            st.write(", ".join(scheme["documents"]))

            st.caption(
                "Prototype result — eligibility should be verified "
                "against the official scheme rules before applying."
            )

st.divider()

st.caption(
    "CivicBridge AI is a prototype. It does not access Aadhaar, "
    "biometric systems or government databases."
  )
