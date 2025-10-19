# Hanuman Interactive Voice Agent — Product Requirements Document (PRD)

## 1. Overview
- **Product**: Hanuman Interactive Voice Agent for Kids
- **Goal**: Deliver an immersive, culturally rooted, and educational voice experience where children interact with Hanuman to learn Hanuman Chalisa and hear age-appropriate stories.
- **Primary Users**: Children (5–12 years) and their parents/guardians
- **Platforms**: ESP32-S3 hardware device (push-to-talk), Cloud services (Deepgram Voice Agent + Flask backend)
- **Reference Diagram**: See the Mermaid system diagram in `README.md`.

## 2. Objectives & Success Metrics
- **Educational Progress**: Consistent improvement in Chalisa mastery (0–5 scale) and verse completion over time
- **Engagement**: Session completion rate > 70%; average session duration 3–8 minutes for target age
- **Retention**: 3+ sessions per week per child
- **Quality**: STT/TTS latency < 2.2s end-to-end in typical conditions; < 1% critical failures per session
- **Safety**: 100% adherence to kid-safe, culturally sensitive responses; no PII leaks

## 3. User Personas & Scenarios
- **Child Learner (5–7)**: Prefers short stories and repetition; needs slower pace and playful prompts
- **Child Learner (8–12)**: Tolerates longer stories; enjoys quizzes and deeper meaning of verses
- **Parent/Guardian**: Wants progress tracking, safe content, and configurable session limits

### Example Scenarios
1) “Teach me Hanuman Chalisa” → revises last verse, teaches next, asks to repeat
2) “Tell me a Hanuman story” → selects short story aligned with age and interests
3) “Play the Hanuman Chalisa” → streams pre-recorded audio (Hanuman persona only)

## 4. Scope
### In Scope (MVP)
- Push-to-talk device, debounced; WiFi 2.4GHz upload
- STT (EN/HI), T2T agent (GPT-4o-mini), TTS (Aura EN; HI TBD)
- Tools: `teach_hanuman_chalisa`, `tell_a_story`, `play_hanuman_chalisa`
- Memory Store (PostgreSQL): profiles, interests, chalisa & story progress, interactions
- Conversation pruning and summaries for context control
- Observability (CloudWatch logs, Datadog metrics)

### Out of Scope (MVP)
- Pronunciation accuracy scoring
- Offline mode on device
- Parent mobile app (beyond initial web links or placeholders)

## 5. Functional Requirements
### 5.1 Audio Input & Transport
- R1: Device records 44.1kHz 16-bit mono audio via I2S MEMS mic
- R2: PTT debounced (30–80ms) to avoid double triggers
- R3: Audio chunked (e.g., 20–50ms) and uploaded over WiFi 2.4GHz

### 5.2 Speech-to-Text & Utterance Handling
- R4: STT provides partial and final transcripts
- R5: Push-to-talk session defines utterance boundaries; optional silence guard
- R6: Model supports EN and HI (with domain vocabulary plan)

### 5.3 T2T Agent & Tool Use
- R7: System prompt enforces Hanuman persona; kid-safe language
- R8: Tool selection policy:
  - teach_hanuman_chalisa for learning/revision requests
  - tell_a_story for storytelling requests
  - play_hanuman_chalisa only for persona=Hanuman with valid audio path
- R9: Agent keeps responses short, asks engagement questions, and offers to continue

### 5.4 Memory Store
- R10: `profiles`, `interests`, `chalisa_progress`, `story_progress`, `interactions` tables
- R11: Progress updates transactional; avoid duplicate entries (unique keys)
- R12: PII masking and encryption-at-rest; TLS in-transit

### 5.5 Text-to-Speech & Playback
- R13: TTS in voice aligned to Hanuman persona; stream to device
- R14: Device plays PCM stream via I2S DAC/speaker with volume control

### 5.6 Privacy & Safety
- R15: Parental consent; Right-to-Deletion workflow
- R16: Content filters for unsafe inputs; culturally sensitive outputs
- R17: Logging redaction for PII

### 5.7 Observability & Ops
- R18: CloudWatch logs for request/response traces
- R19: Datadog metrics for latency, error rates, STT/TTS usage
- R20: Alerts on elevated latency, error spikes, API quota thresholds

## 6. Non-Functional Requirements
- **Latency**: Typical end-to-end ≤ 2.2s; 95th percentile ≤ 3s
- **Uptime**: 99% monthly for backend APIs
- **Scalability**: Horizontal scale of stateless services; DB read replicas as needed
- **Security**: IAM-scoped secrets; KMS-backed encryption; least-privilege access

## 7. Data Model (Summary)
- See `README.md` for detailed Postgres DDL
- Key entities: `profiles`, `interests`, `chalisa_progress`, `story_progress`, `interactions`

## 8. APIs & Tool Contracts
- Tool contracts defined in code for:
  - `teach_hanuman_chalisa` (step-wise verse, translation, engagement, next index)
  - `tell_a_story` (topic selection, story text, available topics)
  - `play_hanuman_chalisa` (validated persona, WAV chunk streaming)
- The Voice Agent wraps these contracts via function-calling

## 9. UX & Conversation Design
- Persona greetings tailored to children (playful, encouraging, gentle)
- Teach flows: revise one verse, teach next, ask to repeat; offer continue/stop
- Story flows: short 3–5 minute stories; pauses for reactions; “What happens next?” prompts
- Bedtime mode (future): softer prosody, calmer narratives

## 10. Telemetry & Analytics
- Metrics: latency breakdown, tool invocation counts, verse completion rates, story completion rates
- Engagement: session frequency, duration, interactive prompts answered
- Error classes: STT/TTS/API failures, network issues, timeouts

## 11. Risks & Mitigations
- **Noisy environments**: Encourage PTT; test in common noise scenarios
- **Cultural accuracy**: Expert review board for stories and verses
- **Privacy compliance**: Parental consent, retention policies, deletion API
- **Model drift**: Fixed tool contracts, regression tests on prompts

## 12. Release Plan
- Alpha: Internal tests with curated stories and 4–6 verses
- Beta: 20 pilot families; expand to all Chalisa verses; collect feedback
- GA: Public release with 10+ stories and full Chalisa; add parent dashboard stub

## 13. Open Questions
- Hindi TTS voice selection and quality target
- Offline fallback feasibility (edge buffering, limited local logic)
- Parent dashboard scope and roadmap (progress visualization, controls)

---
Owner: Product + Eng Team
Reviewers: Education/Cultural Advisors, Security/Privacy Lead, QA Lead
Last Updated: <set on commit>
