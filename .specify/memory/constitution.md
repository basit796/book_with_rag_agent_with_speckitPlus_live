<!--
SYNC IMPACT REPORT
==================
Version Change: None → 1.0.0 (Initial Constitution)
Ratification Date: 2025-12-20

Modified Principles:
- All principles created from scratch (initial version)

Added Sections:
- Core Principles (7 principles)
- Technical Standards
- Quality Gates & Verification
- Governance

Removed Sections:
- None (initial version)

Templates Requiring Updates:
- ✅ plan-template.md: Constitution Check section references this file
- ✅ spec-template.md: Requirements aligned with principles
- ✅ tasks-template.md: Task structure supports phase-based, testable development
- ⚠️ No command templates found to update

Follow-up TODOs:
- None - all placeholders filled with concrete values
-->

# AI/Spec-Driven Book with RAG Chatbot Constitution

## Core Principles

### I. Accuracy & Correctness (NON-NEGOTIABLE)

All technical explanations, code examples, architectural decisions, commands, and configurations MUST be factually correct and verified. No hallucinated content, no unchecked AI-generated filler, no vague approximations.

**Rationale**: This project teaches technical concepts and serves as executable documentation. Incorrect information undermines the educational mission and breaks reader trust. Accuracy is the foundational non-negotiable principle.

**Enforcement**:
- All code must be syntactically correct
- All shell commands must be conceptually tested
- Architecture decisions must be justified and traceable
- RAG chatbot answers must be grounded in retrieved context only

### II. Spec-Driven Development (NON-NEGOTIABLE)

Every chapter, feature, enhancement, and technical decision MUST be derived from explicit written specifications. No ad-hoc changes without specification updates.

**Rationale**: Spec-Driven Development ensures clarity, traceability, and reproducibility. This project exists to demonstrate SDD methodology applied to book creation and AI-enhanced education platforms.

**Enforcement**:
- All features map back to a written spec
- Changes require spec amendments with version control
- Specifications precede implementation
- Prompt History Records (PHRs) track all decisions

### III. Clarity for the Target Audience (NON-NEGOTIABLE)

Content MUST be clear, instructional, and accessible to students, self-taught developers, and early professionals. Progressive complexity from fundamentals to advanced topics. No unexplained jargon, no assumed expertise in Spec-Kit Plus, Docusaurus, RAG, or cloud infrastructure.

**Rationale**: Educational effectiveness requires meeting learners where they are. The book's value is measured by reader comprehension and ability to reproduce results.

**Enforcement**:
- Tone: Professional, instructional, practical
- Language: Simple English, jargon explained on first use
- Structure: Introduction → Concepts → Implementation → Deployment → Troubleshooting
- Each chapter includes: Purpose, Key concepts, Practical steps, Code examples, Common mistakes, Summary

### IV. Reproducibility (NON-NEGOTIABLE)

All steps, commands, configurations, and deployments MUST be reproducible by readers on Windows, macOS, or Linux. No "magic" steps, no platform-specific undocumented quirks, no paid services required for core functionality.

**Rationale**: Readers must be able to follow along and achieve the same results. Reproducibility validates accuracy and builds confidence.

**Enforcement**:
- Commands tested conceptually across platforms
- Environment variables documented explicitly
- No hard-coded secrets or platform assumptions
- Free-tier services only (Neon, Qdrant Cloud free tiers)
- No credit card required for Phase 2

### V. Modularity & Clean Separation

Book content, code, Docusaurus configuration, and RAG chatbot components MUST be cleanly separable and reusable. Clear boundaries between Phase 1 (book publication) and Phase 2 (RAG chatbot enhancement).

**Rationale**: Modular design enables independent testing, incremental delivery, and component reuse. Readers should be able to adopt parts of the system without requiring the whole.

**Enforcement**:
- Phase 1 deliverable: Self-contained static book site
- Phase 2 deliverable: API-first RAG chatbot with clear ingestion/embedding/retrieval/generation separation
- Frontend chatbot embedded cleanly within Docusaurus
- No tight coupling between book content and chatbot logic

### VI. AI-Native Design

Demonstrate AI tools (Claude Code, OpenAI Agents, ChatKit SDKs) as first-class development collaborators. Explicitly document how AI assists specification, coding, testing, and deployment.

**Rationale**: This project is a living example of AI-augmented development. The process itself is instructional content showing how AI can accelerate spec-driven workflows.

**Enforcement**:
- AI interactions recorded in PHRs
- AI-generated content refined and verified by human review
- Claude Code used for content generation and refinement
- OpenAI Agents SDK used for RAG chatbot

### VII. Test-First & Quality Gates

All features requiring verification MUST include explicit success criteria. Architectural decisions require ADR documentation. Quality gates enforce accuracy, completeness, and alignment with specifications.

**Rationale**: Quality cannot be inspected in after the fact. Test-first thinking ensures features are designed for verification from the start.

**Enforcement**:
- Each feature spec includes success criteria
- Constitution Check gates in planning phase
- Architectural decisions trigger ADR suggestions
- Chatbot answers validated against retrieved context
- No broken links or non-functional code in published book

## Technical Standards

### Phase 1: Book Publication

- **Static Site Generator**: Docusaurus
- **Hosting**: GitHub Pages
- **Repository Structure**: Follow Docusaurus best practices
- **Cross-Platform**: All commands runnable on Windows, macOS, Linux
- **Navigation**: Sidebar-based with versioning support
- **File Format**: Markdown (.md) compatible with Docusaurus
- **No Proprietary Services**: Book readable without paid subscriptions

### Phase 2: RAG Chatbot

- **Backend Framework**: FastAPI
- **AI SDKs**: OpenAI Agents SDK / ChatKit SDKs
- **Database**: Neon Serverless Postgres (free tier)
- **Vector Database**: Qdrant Cloud (free tier)
- **API Design**: Clean separation:
  - Ingestion pipeline
  - Embedding generation
  - Retrieval logic
  - Response generation
- **Security**: No hard-coded secrets, environment variables only
- **Frontend**: Embedded chatbot UI within Docusaurus site
- **RAG Capabilities**:
  - Full-book question answering
  - Selected-text-only question answering
  - Source-aware responses (chapter/section references)
  - Grounded responses only (no hallucinations)

## Quality Gates & Verification

### Content Quality Gates

- **Accuracy**: All technical content verified, code syntactically correct
- **Clarity**: Language accessible to target audience
- **Completeness**: Each chapter includes required sections
- **Links**: No broken internal or external links
- **Examples**: All code examples functional

### Phase 1 Success Criteria

- Book builds successfully with `npm run build` (or equivalent)
- Book deploys correctly to GitHub Pages
- Content is readable, structured, and educational
- Navigation works via sidebar
- No console errors on page load

### Phase 2 Success Criteria

- RAG chatbot answers book-related questions accurately
- Selected-text questioning works correctly
- Backend APIs stable and documented
- Chatbot embedded and usable inside book site
- Responses grounded in retrieved context only
- Source attribution functional (chapter/section references)

### Prohibited

- Plagiarism or unattributed copied documentation
- Hallucinated or unchecked AI-generated content
- Broken links or non-functional code
- Paid services or credit card requirements
- Unexplained "magic" steps or undocumented assumptions

## Governance

This constitution supersedes all other development practices and guidelines. All features, content, and technical decisions MUST comply with the principles and standards defined herein.

**Amendment Process**:
- Amendments require explicit documentation with rationale
- Version incremented per semantic versioning:
  - **MAJOR**: Backward-incompatible governance changes, principle removals/redefinitions
  - **MINOR**: New principles added, materially expanded guidance
  - **PATCH**: Clarifications, wording improvements, non-semantic refinements
- Constitution amendments trigger review of dependent templates (plan, spec, tasks)
- Architectural Decision Records (ADRs) document significant technical choices

**Compliance Review**:
- Constitution Check gate enforced in planning phase
- All feature specs must align with principles
- Complexity must be justified against constitution standards
- PHRs track adherence to spec-driven workflow

**Conflict Resolution**:
- When principles appear to conflict, accuracy and correctness take precedence
- Ambiguities resolved in favor of clarity and reproducibility
- Governance questions escalated to constitution amendments

**Version**: 1.0.0 | **Ratified**: 2025-12-20 | **Last Amended**: 2025-12-20
