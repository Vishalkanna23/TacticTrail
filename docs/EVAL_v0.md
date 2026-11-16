# TacticTrail — Retrieval Evaluation v0

Evaluation date (UTC): 2026-11-16T08:36:15.282033+00:00

## Evaluation methodology

- Knowledge base: NIST SP 800-53r5 and SP 800-61r3.
- Retrieval: MiniLM embeddings and PostgreSQL pgvector.
- Top-k: 3 chunks per question.
- Relevance labels: Gemini AI judge.
- Judgments are AI-assessed, not human ground truth.
- Missing retrieval slots count as not relevant.

## Results

- Questions: 10
- Relevant chunks: 21/30
- Hit Rate@3: 100.00%
- Precision@3: 70.00%

| Question | Relevant chunks | Hit@3 |
|---|---|---|
| 1 | 2/3 | Yes |
| 2 | 1/3 | Yes |
| 3 | 3/3 | Yes |
| 4 | 2/3 | Yes |
| 5 | 1/3 | Yes |
| 6 | 3/3 | Yes |
| 7 | 3/3 | Yes |
| 8 | 3/3 | Yes |
| 9 | 1/3 | Yes |
| 10 | 2/3 | Yes |

## Detailed AI judgments

### Question 1

**Question:** How should organizations prepare for cybersecurity incidents?

**Rank 1 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 12
- Similarity: 0.6750
- AI reason: The chunk discusses integrating incident response into organizational operations and practicing continuous improvement as part of cybersecurity risk management.
- Text preview: s were typically intermittent rather than continuous. However, the current state of incident response has greatly changed since then. Today, incidents occur frequently and cause far more damage. Recovering from them often takes weeks or months due to

**Rank 2 — Not relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 11
- Similarity: 0.6602
- AI reason: The chunk merely describes the table of contents and structure of a document without providing preparation steps for cybersecurity incidents.
- Text preview: Section 2 discusses how incident response has evolved to become a critical part of cybersecurity risk management, as well as how the concept of the incident response life cycle has changed to reflect that. • Section 3 presents incident response recom

**Rank 3 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 15
- Similarity: 0.6500
- AI reason: The chunk outlines specific incident response roles and responsibilities, such as leadership oversight and incident handlers, which are part of preparing and managing cybersecurity incidents.
- Text preview: NIST SP 800-61r3 Incident Response Recommendations and April 2025 Considerations for Cyber Risk Management 7 Examples of incident response roles and responsibilities include the following: • Leadership. The organization’s leadership team oversees inc

### Question 2

**Question:** What are the responsibilities of an incident response team?

**Rank 1 — Not relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 15
- Similarity: 0.7706
- AI reason: The chunk discusses the structure of multiple incident response teams in larger organizations and mentions other roles like technology professionals and legal, but does not detail the specific responsibilities of an incident response team.
- Text preview: stance with certain incidents. Larger organizations may have multiple incident response teams, with each team responsible for a particular logical or physical segment of the organization. When this model is employed, the teams should be part of a sin

**Rank 2 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 14
- Similarity: 0.7465
- AI reason: The chunk introduces section 2.2 on 'Incident Response Roles and Responsibilities' and mentions the involvement of incident handlers and other internal/external parties in incident response efforts.
- Text preview: kely to benefit more from using a framework or model emphasizing continuous improvement than other organizations would. Regardless of the incident response life cycle framework or model used, every organization should take incident response into cons

**Rank 3 — Not relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 179
- Similarity: 0.7329
- AI reason: The chunk discusses organizational capabilities, system design, and information sources for incidents, but does not specify the responsibilities of an incident response team.
- Text preview:  predictable across the organization. Discussion:  Organizations recognize that incident response capabilities are dependent on the capabilities of organizational systems and the mission and business processes being supported by those systems. Organi

### Question 3

**Question:** How can organizations improve their incident response processes?

**Rank 1 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 179
- Similarity: 0.7427
- AI reason: The chunk discusses integrating incident response into the definition, design, and development of mission and business processes and systems, as well as coordinating among multiple organizational entities for effective handling.
- Text preview:  predictable across the organization. Discussion:  Organizations recognize that incident response capabilities are dependent on the capabilities of organizational systems and the mission and business processes being supported by those systems. Organi

**Rank 2 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 15
- Similarity: 0.6958
- AI reason: The chunk explains how organizations (especially larger ones with multiple teams) can improve consistency by coordinating teams under a single entity, sharing information, and involving legal and technology professionals in incident response plans.
- Text preview: stance with certain incidents. Larger organizations may have multiple incident response teams, with each team responsible for a particular logical or physical segment of the organization. When this model is employed, the teams should be part of a sin

**Rank 3 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 14
- Similarity: 0.6934
- AI reason: The chunk highlights the importance of using a framework or model emphasizing continuous improvement and incorporating incident response into cybersecurity risk management activities.
- Text preview: kely to benefit more from using a framework or model emphasizing continuous improvement than other organizations would. Regardless of the incident response life cycle framework or model used, every organization should take incident response into cons

### Question 4

**Question:** How should organizations communicate during security incidents?

**Rank 1 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 38
- Similarity: 0.7008
- AI reason: The chunk directly categorizes types of communication during security incidents, including incident coordination, notification, public communication, and information sharing.
- Text preview: egories. Incident coordination involves communicating current and planned incident response activities for a particular incident among the internal and external parties with incident response roles and responsibilities. Incident notification involves

**Rank 2 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 39
- Similarity: 0.6144
- AI reason: The chunk discusses voluntary incident information sharing and coordinating with partner organizations, which are key aspects of communication during security incidents.
- Text preview: al and external stakeholders High N1: Voluntary incident information sharing is often mutually beneficial because the same threats and attacks simultaneously affect multiple organizations. An example is sharing information about observed TTPs with a

**Rank 3 — Not relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 14
- Similarity: 0.5858
- AI reason: The chunk discusses incident response frameworks, risk management, and roles/responsibilities, but does not explain how organizations should communicate during security incidents.
- Text preview: kely to benefit more from using a framework or model emphasizing continuous improvement than other organizations would. Regardless of the incident response life cycle framework or model used, every organization should take incident response into cons

### Question 5

**Question:** What should organizations consider during incident recovery?

**Rank 1 — Relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 15
- Similarity: 0.6699
- AI reason: The chunk mentions technology professionals, engineers, and administrators who may be involved in incident recovery efforts.
- Text preview: stance with certain incidents. Larger organizations may have multiple incident response teams, with each team responsible for a particular logical or physical segment of the organization. When this model is employed, the teams should be part of a sin

**Rank 2 — Not relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 179
- Similarity: 0.6623
- AI reason: The chunk discusses incident response capabilities, design, and monitoring, but does not provide details on what organizations should consider during incident recovery.
- Text preview:  predictable across the organization. Discussion:  Organizations recognize that incident response capabilities are dependent on the capabilities of organizational systems and the mission and business processes being supported by those systems. Organi

**Rank 3 — Not relevant**

- Document: NIST.SP.800-61r3.pdf
- Page: 14
- Similarity: 0.6341
- AI reason: The chunk discusses incident response frameworks, risk management, and roles/responsibilities, but does not cover considerations specifically for incident recovery.
- Text preview: kely to benefit more from using a framework or model emphasizing continuous improvement than other organizations would. Regardless of the incident response life cycle framework or model used, every organization should take incident response into cons

### Question 6

**Question:** What is the principle of least privilege?

**Rank 1 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 63
- Similarity: 0.7376
- AI reason: The chunk directly defines the principle of least privilege as allowing only authorized accesses for users and processes that are necessary to accomplish assigned organizational tasks.
- Text preview: he principle of least privilege, allowing only authorized accesses for users (or processes acting on behalf of users) that are necessary to accomplish assigned organizational tasks. Discussion:  Organizations employ least privilege for specific dutie

**Rank 2 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 314
- Similarity: 0.6543
- AI reason: The chunk explicitly states the principle of least privilege, explaining that each component is allocated sufficient privileges to accomplish its specified functions and no more.
- Text preview:  of the system, system component, or service. Related Controls:  SA-5, SA-11. (7) DEVELOPER SECURITY AND PRIVACY ARCHITECTURE AND DESIGN | STRUCTURE FOR LEAST PRIVILEGE Require the developer of the system, system component, or system service to struc

**Rank 3 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 289
- Similarity: 0.6399
- AI reason: The chunk provides a clear definition of the principle of least privilege, noting that each system component is allocated only the sufficient privileges needed to accomplish its specified functions.
- Text preview: impler system. Related Controls:  None. (14) SECURITY AND PRIVACY ENGINEERING PRINCIPLES | LEAST PRIVILEGE Implement the security design principle of least privilege in [Assignment: organization- defined systems or system components]. Discussion:  Th

### Question 7

**Question:** How should organizations implement multifactor authentication?

**Rank 1 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 160
- Similarity: 0.6894
- AI reason: The chunk discusses specific multifactor authentication solutions involving physical authenticators, smart cards, and application-level mechanisms, which relates to how organizations can implement MFA.
- Text preview: N]), something you have (e.g., a physical authenticator such as a cryptographic private key), or something you are (e.g., a biometric). Multi-factor authentication solutions that feature physical authenticators include hardware authenticators that pr

**Rank 2 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 160
- Similarity: 0.6868
- AI reason: The chunk explains that multifactor authentication requires two or more different factors (something you know, have, or are), directly addressing the definition and implementation approach for non-privileged accounts.
- Text preview: NIST SP 800-53, REV. 5                                                                                     SECURITY AND PRIVACY CONTROLS FOR INFORMATION SYSTEMS AND ORGANIZATIONS _______________________________________________________________________

**Rank 3 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 160
- Similarity: 0.6825
- AI reason: The chunk discusses using multi-factor options appropriate for the level of risk and providing additional security measures or rigorous authentication mechanisms for specific types of access.
- Text preview:  are authenticated using multi-factor options appropriate for the level of risk. Organizations can provide additional security measures, such as additional or more rigorous authentication mechanisms, for specific types of access. Related Controls:  A

### Question 8

**Question:** What security events should organizations audit and log?

**Rank 1 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 93
- Similarity: 0.7249
- AI reason: The chunk discusses how organizations determine which event types to log, such as file accesses, and how the types of logged events may change or be balanced with system performance.
- Text preview:  system. To balance monitoring and auditing requirements with other system needs, event logging requires identifying the subset of event types that are logged at a given point in time. For example, organizations may determine that systems need the ca

**Rank 2 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 93
- Similarity: 0.7058
- AI reason: The chunk mentions that event logging requirements include event types required by applicable laws, executive orders, directives, policies, regulations, standards, and guidelines.
- Text preview: s of logging events can reveal information about individuals that may give rise to privacy risk and how best to mitigate such risks. For example, there is the potential to reveal personally identifiable information in the audit trail, especially if t

**Rank 3 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 93
- Similarity: 0.7043
- AI reason: The chunk outlines control AU-2 on Event Logging, which requires organizations to identify the types of events that the system is capable of logging in support of the audit function.
- Text preview: NIST SP 800-53, REV. 5                                                                                     SECURITY AND PRIVACY CONTROLS FOR INFORMATION SYSTEMS AND ORGANIZATIONS _______________________________________________________________________

### Question 9

**Question:** How should organizations manage user access permissions?

**Rank 1 — Not relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 116
- Similarity: 0.5898
- AI reason: The chunk discusses authorizing officials, system operations, and risk acceptance, but does not provide guidance on managing user access permissions.
- Text preview: organizational systems; c. Ensure that the authorizing official for the system, before commencing operations: 1. Accepts the use of common controls inherited by the system; and 2. Authorizes the system to operate; d. Ensure that the authorizing offic

**Rank 2 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 55
- Similarity: 0.5854
- AI reason: The chunk discusses consulting privacy and legal counsel to determine appropriate mechanisms, access rights, and limitations, as well as enforcing mandatory and discretionary access control policies.
- Text preview: anizational personnel consult with the senior agency official for privacy and legal counsel to determine appropriate mechanisms and access rights or limitations. Related Controls:  IA-8, PM-22, PM-20, PM-21, PT-6. (15) ACCESS ENFORCEMENT | DISCRETION

**Rank 3 — Not relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 116
- Similarity: 0.5662
- AI reason: The chunk focuses on the responsibilities of authorizing officials and federal system authorizations rather than the management of user access permissions.
- Text preview: dividuals, other organizations, and the Nation based on the implementation of agreed-upon controls. Authorizing officials provide budgetary oversight for organizational systems and common controls or assume responsibility for the mission and business

### Question 10

**Question:** How should organizations assess the effectiveness of security controls?

**Rank 1 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 42
- Similarity: 0.6192
- AI reason: The chunk explains that organizations should consider evidence such as artifacts and documentation during control selection and implementation to support current and future assessments, which help determine if controls are implemented correctly and operating as intended.
- Text preview: onfidence that the system satisfies the stated security and privacy requirements while supporting the organization’s mission and business functions. Assurance- related controls are identified in the control summary tables in Appendix C. EVIDENCE OF C

**Rank 2 — Not relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 40
- Similarity: 0.6154
- AI reason: The chunk discusses control selection, managing risks, and implementation considerations, but does not explain how to assess the effectiveness of security controls.
- Text preview: overlap in responsibilities, the controls that organizations select to manage these security risks will generally be the same regardless of their designation as security or privacy controls in control baselines or program or system plans. There also

**Rank 3 — Relevant**

- Document: NIST.SP.800-53r5.pdf
- Page: 426
- Similarity: 0.6071
- AI reason: The chunk defines control assessment as testing or evaluating controls to determine if they are implemented correctly, operating as intended, and producing desired outcomes, and also defines control effectiveness.
- Text preview: ontrol or privacy control. control assessment [SP 800-37] The testing or evaluation of the controls in an information system or an organization to determine the extent to which the controls are implemented correctly, operating as intended, and produc

## Limitations

- Gemini may misjudge relevance.
- Similarity does not guarantee factual correctness.
- This evaluates retrieval, not the final answer.
- The evaluation uses only 10 questions and two PDFs.
- Human spot-checking is recommended.


## Human Spot-Check

Three AI-labeled relevant chunks were manually reviewed.

| Question | Rank | AI label | Review label |
|---|---|---|---|
| Q2 | 2 | Relevant | Not relevant |
| Q5 | 1 | Relevant | Not relevant |
| Q9 | 2 | Relevant | Relevant |

### Findings

- Gemini marked two weak matches as relevant.
- Mentioning a topic does not guarantee that a chunk answers the question.
- Fixed-character chunking sometimes splits words and sentences.
- Relevance evaluation requires more than semantic similarity.

### Provisional Adjusted Results

Assuming the other 28 AI judgments remain unchanged:

- Hit Rate@3: 80.00% (8/10)
- Precision@3: 63.33% (19/30)

These adjusted results are partially human-reviewed,
not a fully human-labeled benchmark.

### Future Improvements

1. Introduce sentence-aware chunking.
2. Retrieve more candidates before re-ranking.
3. Improve the relevance judge's evaluation criteria.
4. Expand human-labeled evaluation coverage.
