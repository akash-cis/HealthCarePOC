// Mock Healthcare Meeting Transcript
// For POC Testing - De-identified (no real patient data)
// Use this as test data for Claude summarization and Salesforce storage

const mockHealthcareTranscript = `
MEETING METADATA:
Date: April 15, 2024
Time: 10:00 AM - 10:45 AM
Duration: 45 minutes
Meeting Type: Clinical Handoff & Care Coordination
Location: Clinic Conference Room B
Attendees: Dr. Smith (Primary Care Physician), Nurse Sarah (RN Care Coordinator), Dr. Patel (Cardiologist Consultant)

---

MEETING TRANSCRIPT:

Dr. Smith: "Alright, let's do our morning handoff. We have three patients to discuss. First is Patient ID: PT-0847 - 68-year-old male, came in yesterday with chest pain."

Nurse Sarah: "Yes, I pulled his chart. Chief complaint was exertional chest pain for the past week. EKG showed some ST changes. Troponin levels were elevated at 0.08."

Dr. Patel: "Okay, so that's concerning. Has he been admitted?"

Dr. Smith: "Yes, admitted to cardiology floor yesterday evening. I wanted your input on next steps. His family history is significant - father had MI at 65."

Dr. Patel: "The troponin elevation and ST changes are indicative of acute coronary syndrome. I'd recommend cardiac catheterization within the next 12 hours. We should also start him on dual antiplatelet therapy if he's not already on it."

Nurse Sarah: "I'll make a note. Should I notify the lab for the cath prep?"

Dr. Patel: "Yes, and make sure interventional cardiology is on standby. Also check his renal function - need creatinine clearance before contrast."

Dr. Smith: "Good point. Nurse Sarah, can you also coordinate with dietary? Patient needs to be NPO after midnight for the procedure."

Nurse Sarah: "Will do. I'll place the orders now."

---

Dr. Smith: "Next patient - PT-1223. 42-year-old female, follow-up on hypertension management. Last visit was three months ago."

Nurse Sarah: "Her home BP readings have been inconsistent. She reported readings ranging from 128/82 to 145/94. She says she's been taking her medication but sometimes forgets doses."

Dr. Smith: "Okay, medication adherence is the issue. What's she on?"

Nurse Sarah: "Lisinopril 10mg daily and Amlodipine 5mg daily."

Dr. Patel: "Those are reasonable starting doses. Has she had any side effects reported?"

Dr. Smith: "She mentioned occasional dizziness, but she's not sure if it's medication-related or stress."

Nurse Sarah: "I documented that she's been under work stress recently."

Dr. Smith: "Let's check her BP in office today and get a basic metabolic panel. If the dizziness persists, we might need to adjust the amlodipine. But first, let's address the adherence - maybe we can set up automated reminders or a pill organizer. Sarah, can you schedule a follow-up in 4 weeks?"

Nurse Sarah: "Absolutely. I'll also send her educational materials on hypertension management."

Dr. Patel: "And if the BP remains elevated at the next visit, we might consider adding a third agent like hydrochlorothiazide."

---

Dr. Smith: "Last one - PT-0512. 34-year-old male with Type 2 diabetes, here for routine follow-up."

Nurse Sarah: "His recent labs came back. A1C is 7.2%, which is pretty good. Fasting glucose was 118. Lipid panel shows total cholesterol 185, LDL 110, HDL 48, triglycerides 125."

Dr. Smith: "A1C is good - that's in target range. LDL is acceptable but could be better. Is he on a statin?"

Nurse Sarah: "No, he's not currently on a statin. He was started on Metformin 1000mg twice daily about a year ago."

Dr. Patel: "Given his LDL and family history of early CAD, I'd recommend we start atorvastatin. Maybe 20mg daily to start."

Dr. Smith: "Agreed. Sarah, add that to his medication list. Also, how's his lifestyle? Any exercise or dietary changes?"

Nurse Sarah: "He mentioned he's been trying to exercise more - about 3-4 times a week. Says he's cut back on sugary drinks."

Dr. Smith: "That's excellent progress. Let's reinforce that at his next visit. Schedule him for 3 months out, and we'll recheck A1C and lipids then to assess response to the statin."

Nurse Sarah: "Will do. I'll also send him diabetes education resources and a referral to our nutritionist."

---

Dr. Smith: "Alright, I think we've covered everything. Sarah, can you make sure all these orders are in the system and send follow-up notifications to the patients?"

Nurse Sarah: "Will take care of it right now."

Dr. Patel: "Good session. Let's touch base again tomorrow about Patient PT-0847's cath results."

Dr. Smith: "Absolutely. Thanks for joining."

---

KEY CLINICAL POINTS DISCUSSED:
- Acute coronary syndrome management for PT-0847
- Hypertension medication adjustment for PT-1223
- Diabetes and cardiovascular risk management for PT-0512
- Medication adherence counseling
- Follow-up scheduling and patient education

NEXT ACTIONS:
1. PT-0847: Cardiac catheterization within 12 hours
2. PT-1223: In-office BP check, BMP labs, 4-week follow-up
3. PT-0512: Start statin therapy, 3-month follow-up with labs
4. All patients: Educational materials and follow-up notifications

---

END OF TRANSCRIPT
`;

module.exports = mockHealthcareTranscript;
