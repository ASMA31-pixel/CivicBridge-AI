# IBM Bob Usage

## How IBM Bob was used in CivicBridge AI

IBM Bob was used as an AI-assisted development tool during the design and implementation of CivicBridge AI.

The project started with a broad idea: helping citizens discover government welfare schemes. We refined this into a more focused workflow centred around accessibility and digital literacy.

Bob was used to help structure the application into smaller development components:

- Citizen information input
- Profile extraction
- Scheme matching
- Eligibility reasoning
- Missing-document guidance
- Citizen-friendly explanations

A key part of the design was the voice-first interaction. Instead of requiring a citizen to complete several fields manually, the prototype allows a natural-language statement such as:

> "எனக்கு 52 வயசு. நான் விவசாயம் செய்கிறேன். எனக்கு வருட வருமானம் 80 ஆயிரம்."

The application extracts relevant information such as age, occupation and income and uses the resulting profile during scheme matching.

IBM Bob also assisted with refining the application structure, implementation workflow and documentation while developing the prototype.

## Important limitation

The prototype does not directly access Aadhaar, biometric systems or government databases.

Any real-world implementation would require authorised APIs, explicit citizen consent, authentication, secure data handling and appropriate privacy controls.

## Development approach

The final prototype combines:

- Python
- Streamlit
- Scikit-learn
- Natural-language profile extraction
- A local scheme knowledge base
- Explainable matching logic

IBM Bob was therefore used as part of the development process rather than being presented as the government-data provider itself.
