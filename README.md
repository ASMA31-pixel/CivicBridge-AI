# CivicBridge AI

### Bridging Citizens to the Benefits They Deserve

CivicBridge AI is an AI-powered citizen benefits navigator designed to make government welfare schemes, subsidies, scholarships and public services easier to discover and understand.

## Problem

Many citizens may be eligible for government schemes but struggle to identify the right schemes or understand eligibility requirements. Existing digital platforms can also require users to manually search and enter several personal details, creating barriers for people with limited digital literacy.

## Our Solution

CivicBridge AI creates a simple citizen profile from information provided through voice, documents or structured input. The system then analyses the profile to identify potentially relevant government schemes.

For each recommendation, CivicBridge AI provides:

- Relevant scheme recommendations
- Eligibility reasoning
- Matching criteria
- Missing information or documents
- Application guidance
- Multilingual citizen-friendly explanations

### Voice-First Approach

Instead of filling multiple fields, a citizen could simply say:

> "எனக்கு 52 வயசு. நான் விவசாயம் செய்கிறேன். எனக்கு வருட வருமானம் 80 ஆயிரம்."

The system converts the information into structured values such as age, occupation and annual income, which can then be used for scheme matching.

## Key Features

1. **Voice-first citizen interaction**
2. **Citizen profile extraction**
3. **Intelligent scheme matching**
4. **Explainable eligibility results**
5. **Missing-document detection**
6. **Multilingual guidance**
7. **Privacy-by-design approach**

## Prototype Architecture

Citizen Input  
↓  
Voice / Document / Structured Information  
↓  
Information Extraction  
↓  
Citizen Profile  
↓  
AI Scheme Matching Engine  
↓  
Eligibility & Relevance Analysis  
↓  
Explanation + Missing Documents  
↓  
Application Guidance

## Technology Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- Natural Language Processing
- IBM Bob
- JSON-based scheme knowledge base

## Privacy & Security

The prototype does **not** directly access Aadhaar, biometric systems or government databases.

Any real-world integration would require authorised government APIs, explicit citizen consent, authentication, secure data handling and appropriate privacy controls.

## Project Status

This repository contains a prototype demonstrating the core concept of CivicBridge AI.

## Team

**The Frontline**

Built for the SkillUp Hackathon in collaboration with IBM SkillsBuild.
