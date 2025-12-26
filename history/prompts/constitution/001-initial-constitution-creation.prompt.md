---
id: PHR-001
title: Initial Constitution Creation
stage: constitution
date: 2025-12-20T17:42:02.863Z
surface: project-level
model: claude-sonnet-4
feature: N/A
branch: main
user: Noman traders
command: /sp.constitution (agent-driven)
labels: [constitution, initialization, phase-1, phase-2]
links:
  spec: N/A
  ticket: N/A
  adr: N/A
  pr: N/A
files:
  - path: .specify/memory/constitution.md
    status: created
    lines_added: 246
    lines_removed: 56
tests:
  - N/A (constitution document, no executable tests)
---

## Prompt

Create the project constitution for an AI/Spec-Driven Book Creation with Integrated RAG Chatbot project.

Project: AI/Spec-Driven Book Creation with Integrated RAG Chatbot

Overview:
This project is executed in two phases.
Phase 1 focuses on writing and publishing a high-quality, AI-assisted technical book using Spec-Kit Plus, Claude Code, and Docusaurus, deployed to GitHub Pages.
Phase 2 enhances the published book by embedding an interactive Retrieval-Augmented Generation (RAG) chatbot capable of answering questions about the book content, including user-selected text.

────────────────────────
Core Principles:
────────────────────────
- Accuracy: All technical explanations, code examples, and architectural decisions must be factually correct and verified.
- Spec-Driven Development: Every chapter, feature, and enhancement must be derived from explicit specifications.
- Clarity for Non-Expert and Semi-Technical Readers: Concepts must be explained clearly with progressive complexity.
- Reproducibility: All steps, commands, configurations, and deployments must be reproducible by readers.
- Modularity: Book content, code, and chatbot components must be cleanly separable and reusable.
- AI-Native Design: Demonstrate how AI tools (Claude Code, OpenAI Agents) are first-class development collaborators.
- Minimal Assumptions: Do not assume prior familiarity with Spec-Kit Plus, Docusaurus, RAG, or cloud infrastructure.

────────────────────────
Writing Standards:
────────────────────────
- Tone: Professional, instructional, and practical
- Style: Clear headings, step-by-step explanations, diagrams where appropriate
- Audience: Students, self-taught developers, and early professionals
- Language: Simple English, avoiding unnecessary jargon
- File Format: Markdown (.md) compatible with Docusaurus
- Structure: Introduction → Concepts → Implementation → Deployment → Troubleshooting
- Each chapter must include: Purpose, Key concepts, Practical steps, Code examples, Common mistakes, Summary

────────────────────────
Technical Standards (Phase 1 – Book):
────────────────────────
- Static site generator: Docusaurus
- Hosting: GitHub Pages
- Repository structure must follow Docusaurus best practices
- All commands must be runnable on Windows, macOS, or Linux
- No proprietary or paid services required to read the book
- Book must be navigable via sidebar and versionable

────────────────────────
Technical Standards (Phase 2 – RAG Chatbot):
────────────────────────
- Backend Framework: FastAPI
- AI SDKs: OpenAI Agents / ChatKit SDKs
- Database: Neon Serverless Postgres (free tier)
- Vector Database: Qdrant Cloud (free tier)
- RAG Capabilities: Answer questions about the entire book, answer questions using only user-selected text, source-aware responses
- API-first design with clean separation between: Ingestion, Embedding, Retrieval, Generation
- Security: No hard-coded secrets, environment variables used consistently
- Frontend: Embedded chatbot UI within the Docusaurus site

────────────────────────
Constraints:
────────────────────────
- Phase 1: Book length modular, multi-chapter; all content generated or refined using Claude Code
- Phase 2: Only free-tier services, no credit card required
- No plagiarism
- No copied documentation without transformation and explanation
- No broken links or non-functional code

────────────────────────
Verification & Quality Gates:
────────────────────────
- All code must be syntactically correct
- All shell commands must be tested conceptually
- Architecture decisions must be justified
- Each feature must map back to a written specification
- Chatbot answers must be grounded in retrieved context only
- Hallucinated answers are unacceptable

────────────────────────
Success Criteria:
────────────────────────
Phase 1 Success:
- Book builds successfully with Docusaurus
- Book deploys correctly to GitHub Pages
- Content is readable, structured, and educational

Phase 2 Success:
- RAG chatbot successfully answers book-related questions
- Selected-text-only questioning works correctly
- Backend APIs are stable and documented
- Chatbot is embedded and usable inside the book site

────────────────────────
Non-Goals:
────────────────────────
- No paid infrastructure
- No closed-source dependencies
- No unexplained "magic" steps
- No vague AI-generated filler content

## Response snapshot

Constitution created at `.specify/memory/constitution.md` version 1.0.0

**Structure**:
- 7 Core Principles (4 NON-NEGOTIABLE)
  - I. Accuracy & Correctness (NON-NEGOTIABLE)
  - II. Spec-Driven Development (NON-NEGOTIABLE)
  - III. Clarity for the Target Audience (NON-NEGOTIABLE)
  - IV. Reproducibility (NON-NEGOTIABLE)
  - V. Modularity & Clean Separation
  - VI. AI-Native Design
  - VII. Test-First & Quality Gates
- Technical Standards (Phase 1 & Phase 2)
- Quality Gates & Verification
- Governance (amendment process, compliance, versioning)

**Sync Impact Report** (prepended as HTML comment):
- Version: 1.0.0 (initial ratification)
- All placeholders filled with concrete values
- Templates validated for alignment
- No TODOs or deferred items

## Outcome

- ✅ Impact: Constitution established with 7 principles covering accuracy, spec-driven development, clarity, reproducibility, modularity, AI-native design, and quality gates. Foundation for all future feature development.
- 🧪 Tests: N/A (governance document)
- 📁 Files: 1 file created (.specify/memory/constitution.md)
- 🔁 Next prompts: Create first feature spec for Phase 1 (Docusaurus book setup), or begin with project initialization spec
- 🧠 Reflection: Constitution successfully maps user requirements to testable, declarative principles. All 7 principles have clear enforcement rules and rationales. Technical standards separated by phase for clarity. Quality gates explicitly defined for both phases.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (initial constitution)
- Prompt variant (if applicable): N/A (first constitution)
- Next experiment (smallest change to try): Test constitution principles against first feature spec to validate completeness and clarity of enforcement rules
