// EXAMPLE OUTPUT: What Claude Will Generate
// This is what lands in your Salesforce custom object

const exampleHealthcareOutput = `
MEETING SUMMARY OUTPUT:
Generated: 2024-04-15 10:47 AM
Processing Time: 12 seconds
Model: Claude Opus 4.6
Status: ✅ HIPAA Compliant

---

## Executive Summary
Morning clinical handoff session with three patients requiring varying levels of intervention. Primary focus on acute coronary syndrome management (PT-0847), hypertension optimization (PT-1223), and diabetes/cardiovascular risk assessment (PT-0512). All treatment plans established with clear follow-up timelines and owner assignments.

## Patients Discussed
- PT-0847: 68-year-old male with acute coronary syndrome, elevated troponin, scheduled for cardiac catheterization
- PT-1223: 42-year-old female with uncontrolled hypertension, medication adherence issues, home BP monitoring inconsistent
- PT-0512: 34-year-old male with Type 2 diabetes, good glycemic control (A1C 7.2%), new cardiovascular risk management initiated

## Clinical Findings by Patient

### PT-0847 (Acute Coronary Syndrome)
**Chief Complaint/Reason for Discussion:** 68-year-old admitted with exertional chest pain, EKG changes, elevated troponin
**Current Status:** Admitted to cardiology floor; symptomatic with concerning cardiac biomarkers
**Key Clinical Data:** 
- Chief complaint: Exertional chest pain x 7 days
- EKG: ST changes noted
- Troponin: 0.08 (elevated)
- Family history: Father with MI at age 65
**Clinical Assessment:** Acute coronary syndrome. Requires urgent intervention. Cardiology consultation confirms need for cardiac catheterization.

### PT-1223 (Hypertension Management)
**Chief Complaint/Reason for Discussion:** 3-month follow-up on hypertension management; medication adherence concerns
**Current Status:** Home BP readings inconsistent (128/82 to 145/94); reports occasional dizziness; work stress documented
**Key Clinical Data:**
- Current medications: Lisinopril 10mg daily, Amlodipine 5mg daily
- BP range: 128/82 to 145/94
- Reported side effect: Occasional dizziness (unclear if medication-related)
- Lifestyle factor: Recent work stress
**Clinical Assessment:** Suboptimal BP control secondary to medication non-adherence and possible side effects. Lifestyle factors contributing.

### PT-0512 (Type 2 Diabetes Follow-up)
**Chief Complaint/Reason for Discussion:** Routine diabetes management follow-up
**Current Status:** Good glycemic control; acceptable lipid profile; improved lifestyle habits (exercise, dietary changes)
**Key Clinical Data:**
- A1C: 7.2% (in target range - excellent control)
- Fasting glucose: 118
- Lipid panel: Total cholesterol 185, LDL 110, HDL 48, Triglycerides 125
- Current medications: Metformin 1000mg BID
- Lifestyle: Exercising 3-4x weekly, reduced sugary beverages
**Clinical Assessment:** Diabetes well-controlled. LDL slightly elevated given cardiovascular risk; statin therapy indicated.

## Treatment Decisions & Recommendations

### PT-0847
**Working Diagnosis:** Acute Coronary Syndrome (presumed NSTEMI based on troponin elevation and ST changes)
**Procedures/Tests:**
- Cardiac catheterization within 12 hours (interventional cardiology on standby)
- Renal function assessment (creatinine clearance) before contrast administration
**Medications:**
- Dual antiplatelet therapy to be initiated/continued
**Monitoring:**
- NPO after midnight (pre-procedure fasting)
- Lab coordination and cath prep
**Referral:** Cardiology (Dr. Patel) - primary interventional team
**Next Steps:** Cardiac catheterization; follow-up with cardiology team

### PT-1223
**Working Diagnosis:** Essential Hypertension, Stage 2 (with medication non-adherence and possible medication side effects)
**Medications (Current):**
- Lisinopril 10mg daily
- Amlodipine 5mg daily
**Medications (Potential Changes):**
- Amlodipine dose may be reduced if dizziness persists
- Hydrochlorothiazide 25mg daily may be added at next visit if BP remains elevated
**Tests/Monitoring:**
- In-office BP check (today)
- Basic metabolic panel ordered
- Home BP monitoring to continue
**Interventions:**
- Implement automated medication reminders or pill organizer
- Medication adherence counseling
**Education:** Hypertension management materials to be sent
**Lifestyle:** Stress management support

### PT-0512
**Working Diagnosis:** Type 2 Diabetes Mellitus, well-controlled; dyslipidemia (new)
**Medications (Current):**
- Metformin 1000mg BID (existing)
**Medications (New):**
- Atorvastatin 20mg daily (initiate for cardiovascular risk reduction)
**Tests (Next 3 months):**
- A1C recheck (assess diabetes control; currently 7.2%)
- Lipid panel recheck (assess statin response)
**Referrals:**
- Nutritionist consultation
- Diabetes education resources
**Monitoring:** A1C and lipid response to statin at 3-month follow-up
**Lifestyle:** Positive reinforcement on exercise and dietary changes

## Action Items (By Owner)

**Dr. Smith (Primary Care Physician):**
- [ ] PT-0847: Ensure dual antiplatelet therapy initiated and NPO orders placed (TODAY - URGENT)
- [ ] PT-1223: Review in-office BP and consider amlodipine adjustment if indicated (TODAY)
- [ ] PT-0512: Document statin initiation in EHR (TODAY)
- [ ] All patients: Follow-up on Nurse Sarah's coordination (ONGOING)

**Nurse Sarah (RN Care Coordinator):**
- [ ] PT-0847: Notify interventional cardiology; confirm renal function labs; order lab work; arrange NPO instructions; confirm cath prep timeline (TODAY - URGENT)
- [ ] PT-1223: Order basic metabolic panel; schedule 4-week follow-up appointment; send hypertension education materials; provide pill organizer/reminder options (TODAY)
- [ ] PT-0512: Place statin order (Atorvastatin 20mg daily); schedule 3-month follow-up appointment; refer to nutritionist; send diabetes education resources (TODAY)
- [ ] All patients: Send follow-up notifications and educational materials (TODAY)

**Dr. Patel (Cardiology/Consultant):**
- [ ] PT-0847: Lead cardiac catheterization procedure; keep interventional team on standby (WITHIN 12 HOURS)
- [ ] PT-0847: Reassess post-cath and communicate results to primary team (TOMORROW)
- [ ] PT-1223: Await reassessment at next visit; consider third-line agent if BP remains elevated (4-WEEK FOLLOW-UP)
- [ ] PT-0512: Reassess cardiovascular risk at 3-month follow-up (3-MONTH FOLLOW-UP)

## Patient Education & Coordination
- PT-0847: Pre-catheterization preparation and education; NPO instructions; what to expect during procedure
- PT-1223: Hypertension management and medication adherence strategies; automated reminder systems; stress management resources
- PT-0512: Diabetes management reinforcement; cardiovascular risk reduction education; nutritionist consultation; statin therapy education

## Follow-Up Scheduling
- **PT-0847:** Urgent (TODAY/TOMORROW) - Cardiac catheterization; cardiology follow-up post-procedure
- **PT-1223:** 4 weeks - BP reassessment, BMP results review, medication adjustment if needed, adherence check-in
- **PT-0512:** 3 months - A1C and lipid recheck; statin response assessment; diabetes control evaluation

## Urgent/Critical Items ⚠️
**PT-0847 - ACUTE CORONARY SYNDROME:**
- Troponin elevation + ST changes = ACS confirmed
- Cardiac catheterization required within 12 hours
- Critical timeline: Interventional cardiology must be notified immediately
- Pre-procedure labs (renal function) must be obtained STAT
- NPO status must be enforced from midnight tonight

**No other critical/urgent findings. PT-1223 and PT-0512 are stable but require optimization.**

## Compliance & Audit Trail Notes
✅ All patient identifiers de-identified (PT-XXXX format only)
✅ HIPAA-safe language used throughout (no real names, no MRNs)
✅ Clinical terminology accurate and standard
✅ All recommendations documented with clear owner and timeline
✅ Audit trail ready for compliance review
✅ No Protected Health Information (PHI) exposed in summary
✅ Appropriate for healthcare record storage

---

MEETING METADATA:
- Meeting Type: Clinical Handoff & Care Coordination
- Date: 2024-04-15
- Duration: 45 minutes
- Attendees: 3 (Dr. Smith, Nurse Sarah, Dr. Patel)
- Patient Records Referenced: 3 (de-identified)
- Treatment Decisions Made: 3
- Urgent Actions: 1 (PT-0847 cardiac cath)
- Follow-up Appointments Scheduled: 3
- Specialist Referrals: 1 (Nutritionist)

SUMMARY STATISTICS:
- Total action items: 14
- High priority (within 24 hours): 6
- Medium priority (within 1 week): 4
- Low priority (scheduled follow-ups): 4
- Clinical accuracy: ✅ Verified
- HIPAA compliance: ✅ Verified
`;

module.exports = exampleHealthcareOutput;
