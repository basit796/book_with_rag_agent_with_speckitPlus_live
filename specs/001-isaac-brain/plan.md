# Technical Execution Plan: Physical AI & Humanoid Robotics Book

**Branch**: `001-isaac-brain` | **Date**: 2025-12-22 | **Spec**: [spec.md](./spec.md)
**Input**: Book project with Module 1-4 specifications

**Note**: This is a planning artifact defining the technical approach to creating the book and supporting systems.

## Summary

This plan translates feature specifications for a technical book on Physical AI and Humanoid Robotics into a concrete technical execution strategy. The book covers Module 1 (Physical AI fundamentals), Module 2 (ROS 2), Module 3 (Robot Simulation), and Module 4 (NVIDIA Isaac AI-driven robotics). This plan defines architecture, research approach, quality gates, and phase organization without writing content or code.

## Technical Context

**Content Format**: Markdown (.md)  
**Static Site Generator**: Docusaurus  
**Hosting**: GitHub Pages  
**Version Control**: Git/GitHub  
**Target Platform**: Web (cross-browser, responsive)
**Project Type**: Documentation-focused educational content system  
**Readability Goals**: Accessible to students, self-taught developers, early professionals  
**Content Scale**: 4 modules × 3-5 chapters each = ~12-20 chapters, ~150-250 pages  
**Tooling**: Spec-Kit Plus (SDD workflow), Claude Code (content generation), GitHub Actions (CI/CD)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

✅ **I. Accuracy & Correctness**: Technical content must be verified against official documentation (ROS 2, Gazebo, NVIDIA Isaac). No hallucinated examples. All explanations grounded in real systems.

✅ **II. Spec-Driven Development**: All modules backed by explicit specifications (Module 1-4 specs exist in `/specs/`). This plan derives from those specifications.

✅ **III. Clarity for Target Audience**: Content targets students, self-taught developers, early professionals. Progressive complexity: Module 1 (concepts) → Module 2 (ROS 2) → Module 3 (simulation) → Module 4 (AI-driven robotics). No unexplained jargon.

✅ **IV. Reproducibility**: Conceptual content does not require hardware. Phase 1 (book only) has no paid dependencies. Docusaurus builds locally on Windows/macOS/Linux.

✅ **V. Modularity & Clean Separation**: Phase 1 (book) separate from Phase 2 (RAG chatbot). Modules structured independently. Readers can skip ahead with forward references.

✅ **VI. AI-Native Design**: Claude Code used for content generation, refinement. Prompt History Records (PHRs) track AI interactions. Process itself is instructional.

✅ **VII. Test-First & Quality Gates**: Each module has success criteria (SC-001 through SC-040+). Acceptance scenarios define testable outcomes. ADRs required for significant decisions.

**Result**: PASS - Project aligns with all seven constitution principles.

## 1. Architecture Sketch

### High-Level System Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                     CONTENT CREATION LAYER                       │
│                                                                  │
│  Spec-Kit Plus        Claude Code         Module Specs          │
│  (SDD Workflow)  →  (Content Gen)   →   (001-intro-physical-ai) │
│                                          (001-ros2-nervous...)   │
│                                          (001-robot-simulation)  │
│                                          (001-isaac-brain)       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   BOOK CONTENT SYSTEM (Phase 1)                  │
│                                                                  │
│  Markdown Files   →   Docusaurus   →   GitHub Pages             │
│  (docs/*.md)          (Build/Nav)      (Static Hosting)         │
│                                                                  │
│  Structure:                                                      │
│  - Module sections (1-4)                                         │
│  - Chapter-based navigation                                      │
│  - Sidebar organization                                          │
│  - Search functionality                                          │
│  - Responsive design                                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓ (Future: Phase 2)
┌─────────────────────────────────────────────────────────────────┐
│              RAG CHATBOT ENHANCEMENT (Phase 2 - Future)          │
│                                                                  │
│  Ingestion    →   Embedding   →   Retrieval   →   Generation    │
│  (Content)        (Vectors)       (Search)        (Answers)      │
│                                                                  │
│  Backend: FastAPI + OpenAI Agents SDK                            │
│  Storage: Neon Postgres + Qdrant Vector DB                       │
│  Frontend: Embedded chatbot UI in Docusaurus                     │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

**Content Creation Layer**:
- **Spec-Kit Plus**: Enforces spec-driven development workflow, PHR tracking, constitution compliance
- **Claude Code**: AI-assisted content generation, technical accuracy verification, diagram creation
- **Module Specs**: Source of truth for requirements, acceptance criteria, success metrics

**Book Content System** (Phase 1 - Current Focus):
- **Markdown Files**: Human-readable source format for chapters and sections
- **Docusaurus**: Static site generator providing navigation, search, theming, build system
- **GitHub Pages**: Free hosting with CI/CD via GitHub Actions
- **Separation**: Conceptual content strictly separated from implementation/code examples

**RAG Chatbot** (Phase 2 - Future Extension):
- **NOT in scope for this planning phase**
- Future extensibility built in via clean content separation
- Content ingestion will read from same Markdown files
- API-first design ensures frontend/backend decoupling

### Documentation Flow

```text
Module Spec (spec.md)
    ↓
Technical Plan (plan.md)  ←  You Are Here
    ↓
Research Notes (research.md)
    ↓
Data Model (data-model.md) - if applicable
    ↓
Contracts (contracts/) - if applicable
    ↓
Tasks Breakdown (tasks.md)
    ↓
Chapter Markdown Files (docs/module-X/chapter-Y.md)
    ↓
Docusaurus Build (npm run build)
    ↓
GitHub Pages Deployment
```

### Tooling Roles

- **Spec-Kit Plus**: Project governance, workflow enforcement, PHR/ADR tracking
- **Claude Code**: Content ideation, draft generation, technical validation, diagram assistance
- **GitHub**: Version control, CI/CD, hosting, collaboration
- **Docusaurus**: Build system, navigation, search, theming, responsive design

### Extensibility for Phase 2

**Design Principles Enabling Future RAG**:
- Markdown files remain single source of truth
- Clean section/chapter boundaries enable chunk-based ingestion
- Metadata (module, chapter, priority) can be extracted from frontmatter
- Content does not depend on chatbot presence
- Chatbot can be added non-invasively as embedded widget

## 2. Section & Module Structure

### Module-to-Section Mapping

```text
Book Title: Physical AI & Humanoid Robotics — From Simulation to Reality

├── Introduction (Landing Page)
│   ├── Who This Book Is For
│   ├── Prerequisites
│   ├── How to Use This Book
│   └── Learning Path
│
├── PART I: FOUNDATIONS
│   │
│   ├── Module 1: Introduction to Physical AI
│   │   ├── Chapter 1: What is Physical AI?
│   │   ├── Chapter 2: The Physical World Constraint
│   │   ├── Chapter 3: Robot Architecture Fundamentals
│   │   └── Chapter 4: Why Humanoid Robotics?
│   │
│   └── Module 2: ROS 2 – The Robotic Nervous System
│       ├── Chapter 1: Why Middleware Matters
│       ├── Chapter 2: Nodes, Topics, and Messages
│       ├── Chapter 3: Services and Actions
│       ├── Chapter 4: ROS 2 System Architecture
│       └── Chapter 5: Python Integration with ROS 2
│
├── PART II: SIMULATION & AI-DRIVEN ROBOTICS
│   │
│   ├── Module 3: Digital Twins & Simulation
│   │   ├── Chapter 1: Why Simulation Comes First
│   │   ├── Chapter 2: Physics Engines and Digital Twins
│   │   ├── Chapter 3: Simulated Sensors and Perception
│   │   └── Chapter 4: Simulation Tools Landscape
│   │
│   └── Module 4: The AI-Robot Brain (NVIDIA Isaac)
│       ├── Chapter 1: Why AI Needs Better Simulation
│       ├── Chapter 2: Isaac Sim Overview
│       ├── Chapter 3: Isaac ROS Pipelines
│       └── Chapter 4: Mapping & Navigation
│
└── PART III: FUTURE EXTENSIONS (Placeholders)
    ├── Module 5: Vision-Language-Action Models (VLA)
    ├── Module 6: Sim-to-Real Transfer
    └── Module 7: Deployment & Production
```

### Docusaurus Organization Strategy

**Directory Structure**:
```text
docs/
├── intro.md                              # Landing page
├── how-to-use.md                         # Guide for readers
│
├── module-1-physical-ai/
│   ├── _category_.json                   # "Module 1: Physical AI"
│   ├── 01-what-is-physical-ai.md
│   ├── 02-physical-constraints.md
│   ├── 03-robot-architecture.md
│   └── 04-why-humanoids.md
│
├── module-2-ros2/
│   ├── _category_.json                   # "Module 2: ROS 2"
│   ├── 01-why-middleware.md
│   ├── 02-nodes-topics-messages.md
│   ├── 03-services-actions.md
│   ├── 04-system-architecture.md
│   └── 05-python-integration.md
│
├── module-3-simulation/
│   ├── _category_.json                   # "Module 3: Simulation"
│   ├── 01-why-simulation-first.md
│   ├── 02-physics-digital-twins.md
│   ├── 03-simulated-sensors.md
│   └── 04-tools-landscape.md
│
└── module-4-isaac/
    ├── _category_.json                   # "Module 4: Isaac AI"
    ├── 01-why-better-simulation.md
    ├── 02-isaac-sim-overview.md
    ├── 03-isaac-ros-pipelines.md
    └── 04-mapping-navigation.md
```

**Sidebar Configuration** (`sidebars.js`):
```javascript
module.exports = {
  bookSidebar: [
    'intro',
    'how-to-use',
    {
      type: 'category',
      label: 'Part I: Foundations',
      collapsed: false,
      items: [
        {
          type: 'category',
          label: 'Module 1: Physical AI',
          link: {type: 'generated-index'},
          items: [
            'module-1-physical-ai/01-what-is-physical-ai',
            'module-1-physical-ai/02-physical-constraints',
            'module-1-physical-ai/03-robot-architecture',
            'module-1-physical-ai/04-why-humanoids'
          ]
        },
        {
          type: 'category',
          label: 'Module 2: ROS 2',
          link: {type: 'generated-index'},
          items: [
            'module-2-ros2/01-why-middleware',
            'module-2-ros2/02-nodes-topics-messages',
            'module-2-ros2/03-services-actions',
            'module-2-ros2/04-system-architecture',
            'module-2-ros2/05-python-integration'
          ]
        }
      ]
    },
    {
      type: 'category',
      label: 'Part II: Simulation & AI',
      collapsed: false,
      items: [
        // Module 3 and 4...
      ]
    }
  ]
};
```

### Progression Logic

**Linear Dependency Chain**:
1. **Module 1** → Establishes "what" (Physical AI concepts, robot architecture)
2. **Module 2** → Establishes "how" (ROS 2 communication, distributed systems)
3. **Module 3** → Establishes "where" (Simulation environments, digital twins)
4. **Module 4** → Establishes "AI-driven" (Perception, navigation, Isaac ecosystem)

**Forward References**:
- Module 1 previews ROS 2 (Module 2) when discussing sense-think-act architecture
- Module 2 references simulation (Module 3) when explaining testing workflows
- Module 3 previews Isaac Sim (Module 4) when comparing simulation tools
- Module 4 prepares for VLA (Module 5) and sim-to-real (Module 6)

**Backward References**:
- Each module includes "Prerequisites" section referencing prior modules
- Consistent terminology enforced via glossary
- Diagrams reused and extended across modules

### Navigation Features

- **Prev/Next buttons**: Linear chapter progression within modules
- **Breadcrumbs**: Part → Module → Chapter
- **Search**: Full-text search across all content
- **Table of Contents**: Right sidebar showing current chapter sections
- **Mobile-friendly**: Hamburger menu for sidebar on small screens


### Phase 2: Analysis (Concept Development)

**Goal**: Develop core conceptual content for each module

**Activities**:
1. **Module 1: Physical AI**
   - Draft Chapters 1-4 based on FR-001 through FR-030+
   - Create diagrams (robot architecture, sense-think-act loop)
   - Write thought experiments (chatbot vs robot)
   - Include real-world examples (robot failures, success stories)

2. **Module 2: ROS 2**
   - Draft Chapters 1-5 based on FR specs
   - Create ROS 2 graph diagrams (nodes, topics, messages)
   - Design communication pattern comparison tables
   - Write Python code snippets (minimal, illustrative)

3. **Module 3: Simulation**
   - Draft Chapters 1-4 based on FR specs
   - Create digital twin concept diagrams
   - Develop simulation tool comparison matrix
   - Write sensor modeling explanations

4. **Module 4: Isaac AI**
   - Draft Chapters 1-4 based on FR-001 through FR-074
   - Create Isaac ecosystem diagram
   - Design perception pipeline diagrams
   - Develop navigation system architecture visuals
   - Write SLAM and Nav2 conceptual explanations

**Quality Checks per Chapter**:
- ✅ Addresses all assigned FR requirements
- ✅ Includes required diagrams and visuals
- ✅ Contains thought experiments or case studies
- ✅ Has "Common Misconceptions" section
- ✅ Includes "Check Your Understanding" questions

**Outputs**:
- Draft Markdown files in /docs/module-X/
- Diagram source files (draw.io, mermaid, or similar)
- Research notes updated with synthesis decisions

**Acceptance**: All chapters drafted, peer-reviewed, test-reader approved

---

### Phase 3: Synthesis (Final Content Assembly)

**Goal**: Refine, integrate, and finalize all content for publication

**Activities**:
1. **Cross-Module Integration**
   - Ensure consistent terminology (glossary audit)
   - Verify forward/backward references accurate
   - Check prerequisite statements align with actual content
   - Standardize diagram styles and notation

2. **Quality Validation** (per Section 5)
   - Level 1: Spec alignment verification
   - Level 2: Technical accuracy peer review
   - Level 3: Internal consistency audit
   - Level 4: Beginner accessibility test
   - Level 5: Complexity jump detection

3. **Acceptance Testing** (per Section 6)
   - Module-level acceptance checks
   - Chapter readiness verification
   - Build validation (Docusaurus)
   - Navigation and structure testing
   - Reader outcome verification

4. **Final Polish**
   - Copyedit for grammar, style, clarity
   - Optimize images and diagrams
   - Add metadata (frontmatter, SEO)
   - Generate PDF version (optional)

**Outputs**:
- Production-ready Markdown files
- Final diagrams and visuals
- Deployed GitHub Pages site
- Quality assurance sign-off documents

**Acceptance**: All modules pass acceptance criteria, site live and functional

---

### Phase Interdependencies

`	ext
Phase 0: Research
   ↓ (research.md complete, no blockers)
Phase 1: Foundation
   ↓ (structure ready, specs validated)
Phase 2: Analysis
   ↓ (content drafted, peer-reviewed)
Phase 3: Synthesis
   ↓ (integrated, polished, validated)
Deployment
`

**Critical Path**:
- Research (Phase 0) must resolve all NEEDS CLARIFICATION before content creation
- Foundation (Phase 1) structure must exist before content written
- Analysis (Phase 2) requires iterative peer review to prevent rework
- Synthesis (Phase 3) benefits from early integration (don't wait until end)

**Recommended Approach**:
- Phase 0: 1-2 weeks (research all modules concurrently)
- Phase 1: 3-5 days (setup and validation)
- Phase 2: 4-6 weeks (1-1.5 weeks per module, some overlap)
- Phase 3: 2-3 weeks (integration, testing, polish)
- **Total**: ~8-10 weeks from start to publication

---

## Project Structure

### Documentation (This Feature)

`	ext
specs/001-isaac-brain/
├── spec.md              # Module 4 specification (existing)
├── plan.md              # This file (technical plan)
├── research.md          # Phase 0 output (research notes)
├── quickstart.md        # Phase 1 output (contributor guide)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan)

specs/001-intro-physical-ai/
├── spec.md
├── plan.md              # To be created (similar structure)
├── research.md
└── tasks.md

specs/001-ros2-nervous-system/
├── spec.md
├── plan.md              # To be created
├── research.md
└── tasks.md

specs/001-robot-simulation/
├── spec.md
├── plan.md              # To be created
├── research.md
└── tasks.md
`

### Book Content (Repository Root)

`	ext
docs/
├── intro.md                              # Landing page
├── how-to-use.md                         # Reader guide
│
├── module-1-physical-ai/
│   ├── _category_.json
│   ├── 01-what-is-physical-ai.md
│   ├── 02-physical-constraints.md
│   ├── 03-robot-architecture.md
│   └── 04-why-humanoids.md
│
├── module-2-ros2/
│   ├── _category_.json
│   ├── 01-why-middleware.md
│   ├── 02-nodes-topics-messages.md
│   ├── 03-services-actions.md
│   ├── 04-system-architecture.md
│   └── 05-python-integration.md
│
├── module-3-simulation/
│   ├── _category_.json
│   ├── 01-why-simulation-first.md
│   ├── 02-physics-digital-twins.md
│   ├── 03-simulated-sensors.md
│   └── 04-tools-landscape.md
│
└── module-4-isaac/
    ├── _category_.json
    ├── 01-why-better-simulation.md
    ├── 02-isaac-sim-overview.md
    ├── 03-isaac-ros-pipelines.md
    └── 04-mapping-navigation.md

static/
├── img/                                   # Diagrams, screenshots
│   ├── module-1/
│   ├── module-2/
│   ├── module-3/
│   └── module-4/
└── diagrams/                              # Source files (draw.io, etc.)

src/
├── css/                                   # Custom Docusaurus styling
└── pages/                                 # Custom React pages (if needed)

.github/
└── workflows/
    └── deploy.yml                         # GitHub Pages CI/CD

docusaurus.config.js                       # Docusaurus configuration
sidebars.js                                # Sidebar navigation
package.json                               # Node dependencies
`

**Structure Decision**: Documentation project using Docusaurus static site generator. Book content in /docs/ organized by module. Specifications in /specs/ organized by feature branch. Clean separation between planning artifacts (specs/) and published content (docs/).

---

## Stop Condition & Deliverables

### This Plan Ends Here

**Scope of This Document**:
- ✅ Architecture and structure defined
- ✅ Research approach documented
- ✅ Quality validation strategy established
- ✅ Testing and acceptance criteria defined
- ✅ Phase organization explained
- ✅ Technical decisions documented

**Out of Scope**:
- ❌ Writing book content (Modules 1-4 chapters)
- ❌ Creating diagrams or visuals
- ❌ Implementing Docusaurus site
- ❌ Task breakdown (separate /sp.tasks command)

**Next Steps**:
1. Review and approve this plan
2. Execute Phase 0 (Research) - create esearch.md per module
3. Execute Phase 1 (Foundation) - set up Docusaurus structure
4. Run /sp.tasks command to break down into executable tasks
5. Execute Phase 2 (Analysis) - write content
6. Execute Phase 3 (Synthesis) - integrate and polish

---

## Summary of Key Decisions

| Decision | Chosen Option | ADR Required? |
|----------|---------------|---------------|
| Static Site Generator | Docusaurus | Yes |
| Hosting | GitHub Pages | No (standard) |
| Development Approach | Simulation-first | Yes |
| Ecosystem | ROS 2 + Isaac | Yes |
| Pedagogy | Conceptual-first | No |
| Hardware | Generic humanoid | No |
| Research Model | Concurrent with writing | No |

---

## Constitution Re-Check

**After Phase 1 Design, verify**:
- ✅ Accuracy: Research validation process defined
- ✅ Spec-Driven: All content traces to FR requirements
- ✅ Clarity: Test reader program ensures accessibility
- ✅ Reproducibility: Docusaurus builds on all platforms
- ✅ Modularity: Modules independent, Phase 2 (RAG) separate
- ✅ AI-Native: PHRs track AI interactions
- ✅ Quality Gates: Multi-level validation strategy

**Result**: Constitution compliance maintained through design phase.

---

**Plan Complete**: This technical plan is ready for review and Phase 0 execution.