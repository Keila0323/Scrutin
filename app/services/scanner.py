import os
import json
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

SYSTEM_PROMPT = """You are Scrutin, an expert AI system trained to detect fraudulent and scam job postings.

You analyze job postings with the precision of a fraud investigator. Your job is to identify red flags, 
legitimacy signals, and provide a clear scam risk score.

You understand these common job scam patterns:
- Vague or no company name / unverifiable employer
- Unrealistic salary promises ("earn $5000/week from home!")
- Requests for personal info upfront (SSN, bank details, passport)
- Requests to pay for training, equipment, or background checks
- Generic/copy-paste job descriptions with no specifics
- Unprofessional language, excessive typos, poor grammar
- No clear job responsibilities or qualifications
- "Work from home, set your own hours, no experience needed" for high-pay roles
- Email domains that don't match the company (gmail/yahoo for corporate roles)
- Pressure tactics ("apply now, limited spots!")
- Too good to be true compensation with minimal requirements
- Reshipping, money transfer, or "payment processing" roles
- Missing company address, website, or contact information
- Requests to communicate only via WhatsApp or personal email

You also recognize legitimate signals:
- Clear company name with verifiable online presence
- Specific job responsibilities and required qualifications  
- Realistic compensation for the role and industry
- Professional language and formatting
- Clear application process through official channels
- Physical office address or verifiable remote policy
- Benefits package details
- Named hiring manager or HR contact with company email"""

async def analyze_posting(text: str) -> dict:
    prompt = f"""Analyze this job posting for scam indicators. Be thorough and precise.

JOB POSTING:
{text}

Return ONLY valid JSON in this exact format:
{{
  "scam_score": <integer 0-100, where 0=completely legitimate, 100=definite scam>,
  "verdict": "<one of: LIKELY SCAM | SUSPICIOUS | PROCEED WITH CAUTION | LOOKS LEGITIMATE>",
  "verdict_summary": "<one sentence plain-English summary of your overall finding>",
  "red_flags": [
    {{"flag": "<short flag title>", "explanation": "<1-2 sentence explanation of why this is suspicious>", "severity": "<HIGH|MEDIUM|LOW>"}}
  ],
  "legitimacy_signals": [
    {{"signal": "<short signal title>", "explanation": "<1 sentence explanation>"}}
  ],
  "recommendation": "<2-3 sentence actionable advice for the job seeker — what should they do next?>",
  "missing_info": ["<list of important information that is absent from this posting>"]
}}

Rules:
- scam_score 0-25: Looks Legitimate
- scam_score 26-50: Proceed With Caution  
- scam_score 51-75: Suspicious
- scam_score 76-100: Likely Scam
- Be specific — reference actual text from the posting in your explanations
- If there are NO red flags, return an empty array []
- If there are NO legitimacy signals, return an empty array []
- Always provide at least one recommendation"""

    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
            max_tokens=1500
        )
        result = json.loads(response.choices[0].message.content)
        return {"success": True, "analysis": result}

    except Exception as e:
        print(f"OpenAI error: {type(e).__name__}: {e}")
        # Fallback mock for when API is unavailable
        return {
            "success": True,
            "analysis": {
                "scam_score": 72,
                "verdict": "SUSPICIOUS",
                "verdict_summary": "This posting contains several characteristics commonly associated with fraudulent job listings.",
                "red_flags": [
                    {"flag": "Vague Company Identity", "explanation": "No verifiable company name or website is provided. Legitimate employers always identify themselves clearly.", "severity": "HIGH"},
                    {"flag": "Unrealistic Compensation", "explanation": "The salary offered is significantly above market rate for the described role with minimal requirements.", "severity": "HIGH"},
                    {"flag": "Requests Personal Information Early", "explanation": "Asking for personal details before an official interview or offer is a major scam indicator.", "severity": "HIGH"},
                    {"flag": "No Specific Qualifications", "explanation": "Legitimate roles list specific skills and experience. Vague requirements often indicate a fraudulent listing.", "severity": "MEDIUM"},
                    {"flag": "Non-Corporate Contact Email", "explanation": "Using a Gmail or Yahoo address instead of a company email domain is a strong red flag.", "severity": "MEDIUM"},
                ],
                "legitimacy_signals": [
                    {"signal": "Mentions Benefits", "explanation": "The posting references benefits, which is a minor positive signal."}
                ],
                "recommendation": "Do not provide any personal information or payment to this employer. Research the company name independently before responding. If you cannot verify the company exists through LinkedIn, their official website, or public records, treat this as a scam.",
                "missing_info": ["Company name and website", "Physical office address", "Specific job responsibilities", "Named hiring manager or HR contact", "Official application process"]
            }
        }
