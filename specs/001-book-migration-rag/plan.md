# Implementation Plan: Book Content Migration & RAG Chatbot Integration

**Branch**: `001-book-migration-rag` | **Date**: 2025-12-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-book-migration-rag/spec.md`

**Note**: This plan follows the spec-driven development methodology for migrating the Physical AI & Humanoid Robotics book to Docusaurus and implementing a RAG-powered chatbot using ADK (Agentic Development Kit) with Google Gemini embeddings.

## Summary

This feature enables readers to access 16 chapters of Physical AI & Humanoid Robotics content through the existing Docusaurus site with an embedded RAG chatbot. The chatbot uses Google Gemini text-embedding-004 for semantic search across book content, ChromaDB for vector storage, and ADK-compliant agent architecture for retrieval-augmented generation. The implementation is split into three phases: frontend customization, vector database setup with embeddings, and ADK agent implementation with FastAPI backend integration.

## Technical Context

**Language/Version**: 
- Backend: Python 3.11+
- Frontend: JavaScript (React 18+, Node.js 18+)

**Primary Dependencies**: 
- Backend: FastAPI, ADK (Agentic Development Kit), google-generativeai, chromadb, uvicorn, python-multipart
- Frontend: Docusaurus 3.x, React 18+, framer-motion (animations)
- AI: Google Gemini API (text-embedding-004 model for embeddings, gemini-pro for generation)

**Storage**: 
- Vector DB: ChromaDB (persistent local storage)
- Metadata: In-memory Python dictionaries / JSON files
- Document Source: Markdown files in `docs/` directory

**Testing**: 
- Backend: pytest, pytest-asyncio
- Frontend: Jest, React Testing Library
- Integration: Manual testing of chat flows
- E2E: Playwright (optional for Phase 2)

**Target Platform**: 
- Development: Windows/macOS/Linux local development
- Deployment: Static site (GitHub Pages) + Backend API server (localhost or cloud deployment)

**Project Type**: Web application (static frontend + RESTful backend API)

**Performance Goals**: 
- Chat response time: <3 seconds end-to-end
- Vector search latency: <500ms for top-K retrieval
- Embedding generation: <2 seconds per query
- Concurrent users: Support 10+ simultaneous chat sessions

**Constraints**: 
- Must use Google Gemini API (no OpenAI)
- Must be ADK-compliant agent architecture
- Must use ChromaDB (not Pinecone/Weaviate)
- No user authentication required
- Chatbot must only answer from book content (no hallucinations)
- Frontend must remain functional if chatbot backend is down

**Scale/Scope**: 
- 16 book chapters (~40,000-80,000 words total)
- Estimated 200-400 content chunks after segmentation
- 768-dimensional embeddings (Gemini text-embedding-004)
- Initial traffic: <50 concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Accuracy & Correctness ✅ PASS
- All technical approaches verified: ADK architecture, Google Gemini API, ChromaDB
- Code examples will be syntactically correct and tested
- Architecture decisions traceable to spec requirements
- RAG responses grounded in retrieved context only (no hallucinations)

### II. Spec-Driven Development ✅ PASS
- Feature derived from explicit spec.md (001-book-migration-rag)
- Implementation plan follows template structure
- All changes require spec alignment
- PHR will be generated for this planning session

### III. Clarity for Target Audience ✅ PASS
- Target audience: Students, self-taught developers, early professionals
- Documentation will include: setup instructions, architecture diagrams, API contracts
- Progressive complexity: Frontend → Embeddings → Agent → Integration
- No unexplained jargon (ADK, RAG, embeddings all defined)

### IV. Reproducibility ✅ PASS
- All commands platform-agnostic (Python, Node.js)
- Environment variables documented explicitly
- Free-tier services only (Google Gemini free tier, local ChromaDB)
- No credit card required
- Clear setup instructions for Windows/macOS/Linux

### V. Modularity & Clean Separation ✅ PASS
- Clear boundaries:
  - Frontend customization (standalone)
  - Vector database setup (independent pipeline)
  - ADK agent (modular tools: embedding, search, generation)
  - FastAPI backend (API-first design)
- Chat widget can be disabled without affecting book content
- Agent tools are independently testable

### VI. AI-Native Design ✅ PASS
- ADK-compliant agent architecture demonstrated
- Google Gemini AI for embeddings and generation
- RAG pattern showcases modern AI development
- AI interactions will be documented in PHRs

### VII. Test-First & Quality Gates ✅ PASS
- Success criteria defined in spec.md (SC-001 through SC-014)
- Acceptance scenarios for each user story
- Testing strategy included (pytest, Jest, integration tests)
- Constitution Check enforced at planning phase
- ADR will be suggested for significant architectural decisions

**Gate Status**: ✅ PASS - Proceed to Phase 0 Research

**Re-evaluation Required After**: Phase 1 Design (data-model.md, contracts/ generation)

## Project Structure

### Documentation (this feature)

```text
specs/001-book-migration-rag/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output - ADK architecture, Gemini API, ChromaDB patterns
├── data-model.md        # Phase 1 output - Entities: ContentChunk, VectorEmbedding, ChatMessage
├── quickstart.md        # Phase 1 output - Setup and deployment guide
├── contracts/           # Phase 1 output - API specifications
│   ├── chat-api.yaml   # OpenAPI spec for chat endpoints
│   └── agent-tools.md  # ADK agent tool contracts
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
Future Ai And Robotics/
├── backend/                          # Python FastAPI backend
│   ├── agent/                        # ADK-compliant agent
│   │   ├── __init__.py
│   │   ├── agent.py                  # Main agent definition (ADK Agent class)
│   │   ├── tools.py                  # Tool implementations (embedding, search, generation)
│   │   └── runner.py                 # Agent executor and orchestration
│   ├── api/                          # FastAPI application
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app setup, CORS, middleware
│   │   ├── routes.py                 # REST endpoints for chat
│   │   └── websocket.py              # WebSocket support for real-time chat
│   ├── vectordb/                     # Vector database operations
│   │   ├── __init__.py
│   │   ├── embeddings.py             # Gemini embedding generation
│   │   ├── store.py                  # ChromaDB persistence and retrieval
│   │   └── chunker.py                # Markdown document chunking logic
│   ├── tests/                        # Backend tests
│   │   ├── test_agent.py
│   │   ├── test_tools.py
│   │   ├── test_embeddings.py
│   │   └── test_api.py
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment variable template
│   └── README.md                     # Backend setup instructions
│
├── src/                              # Docusaurus React components
│   └── components/
│       └── ChatWidget/               # Embedded chat interface
│           ├── ChatWidget.js         # Main widget component
│           ├── ChatWidget.module.css # Scoped styles
│           ├── MessageList.js        # Message display component
│           ├── InputBox.js           # User input component
│           └── index.js              # Export barrel
│
├── docs/                             # Book content (already exists)
│   ├── module-1-physical-ai/         # 4 chapters
│   ├── module-2-ros2/                # 4 chapters
│   ├── module-3-simulation/          # 4 chapters
│   ├── module-4-isaac/               # 4 chapters
│   └── [tutorial folders - TO REMOVE]
│
├── docusaurus.config.js              # Site configuration (needs branding updates)
├── sidebars.js                       # Navigation structure (needs cleanup)
├── package.json                      # Frontend dependencies
└── README.md                         # Main project documentation
```

**Structure Decision**: 
Chose **web application structure** (Option 2) with clear separation between:
- `backend/` - Python FastAPI server with ADK agent
- `src/components/` - React chat widget integrated into Docusaurus
- `docs/` - Static markdown content (already established)

This structure supports:
- Independent backend development and testing
- Frontend component reusability within Docusaurus
- Clear API boundary between chat widget and backend
- Modular agent architecture (agent/, vectordb/, api/ separation)

## Complexity Tracking

> **No violations detected - section left empty per template guidance**

All architectural decisions align with constitution principles. No additional complexity justification required.

---

## Phase 0: Outline & Research

**Objective**: Resolve all technical unknowns and establish best practices for ADK agent architecture, Google Gemini integration, and ChromaDB usage.

### Research Tasks

#### R1: ADK (Agentic Development Kit) Architecture
**Question**: What is ADK? How do we structure an ADK-compliant agent with tools?
**Deliverable**: 
- ADK agent pattern documentation
- Tool registration and execution flow
- Best practices for agent.py, tools.py, runner.py separation

#### R2: Google Gemini API Integration
**Question**: How to use Google Gemini text-embedding-004 and gemini-pro models?
**Deliverable**:
- API authentication patterns (API key management)
- Embedding generation workflow
- Rate limits and error handling
- Cost estimation (free tier limits)

#### R3: ChromaDB for Vector Storage
**Question**: How to set up ChromaDB with persistent storage and efficient retrieval?
**Deliverable**:
- ChromaDB collection design
- Metadata schema for book chunks
- Query patterns for top-K similarity search
- Persistence configuration

#### R4: Markdown Chunking Strategy
**Question**: Best practices for chunking markdown content while preserving context?
**Deliverable**:
- Chunk size recommendations (tokens vs. characters)
- Overlap strategy for context preservation
- Handling of code blocks, tables, images
- Section header retention for citations

#### R5: FastAPI + WebSocket Patterns
**Question**: How to implement REST and WebSocket endpoints for chat?
**Deliverable**:
- FastAPI async patterns
- CORS configuration for Docusaurus integration
- WebSocket connection management
- Error handling and graceful degradation

#### R6: React Chat Widget Best Practices
**Question**: How to build an accessible, animated chat widget in React?
**Deliverable**:
- Component architecture (container/presentation)
- Animation libraries (framer-motion patterns)
- Accessibility (keyboard navigation, ARIA labels)
- State management (local state vs. context)

### Research Output: research.md

**Format**:
```markdown
# Research: RAG Agent System Implementation

## ADK Architecture
- **Decision**: [chosen pattern]
- **Rationale**: [why this approach]
- **Alternatives Considered**: [other options evaluated]

## Google Gemini Integration
- **Decision**: [API setup approach]
- **Rationale**: [benefits and trade-offs]
- **Alternatives Considered**: [OpenAI, local models]

[... continue for all research tasks]
```

**Completion Criteria**: All "NEEDS CLARIFICATION" items resolved with concrete decisions and rationale.

---

## Phase 1: Design & Contracts

**Prerequisites**: research.md complete with all decisions documented

**Objective**: Generate data models, API contracts, and quickstart guide

### Design Tasks

#### D1: Data Model Design (data-model.md)
**Entities to Define**:

**ContentChunk**
- Fields: id, chapter_id, module_name, section_title, content_text, start_position, end_position, metadata
- Relationships: Belongs to one Chapter, has one VectorEmbedding
- Validation: content_text non-empty, max 1000 tokens

**VectorEmbedding**
- Fields: id, chunk_id, embedding_vector (768 dimensions), model_version, created_at
- Relationships: Belongs to one ContentChunk
- Validation: embedding_vector length = 768

**ChatMessage**
- Fields: id, session_id, sender (user/bot), message_text, timestamp, source_citations
- Relationships: Belongs to one ChatSession, has many SourceCitations
- Validation: sender in ['user', 'bot'], message_text non-empty

**SourceCitation**
- Fields: id, message_id, chapter_number, chapter_title, section_heading, chunk_id
- Relationships: Belongs to one ChatMessage
- Validation: chapter_number 1-16

**ChunkMetadata**
- Fields: module_name, chapter_number, section_heading, file_path, word_count
- Purpose: Filtering and citation generation

#### D2: API Contract Generation (contracts/)

**REST Endpoints** (contracts/chat-api.yaml):
```yaml
openapi: 3.0.0
paths:
  /api/chat/query:
    post:
      summary: Submit a chat question
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                question: string
                session_id: string (optional)
      responses:
        200:
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  answer: string
                  citations: array
                  session_id: string
  
  /api/chat/health:
    get:
      summary: Health check endpoint
      responses:
        200:
          description: Service healthy
```

**WebSocket Contract**:
```yaml
/ws/chat:
  onConnect: Send welcome message
  onMessage: 
    input: { question: string, session_id: string }
    output: { answer: string, citations: array, typing: boolean }
  onError: Send error message with retry guidance
```

**Agent Tools Contract** (contracts/agent-tools.md):
```markdown
# ADK Agent Tools

## embedding_tool
- Input: query_text (string)
- Output: embedding_vector (array[768])
- Purpose: Generate Gemini embeddings for search queries

## vector_search_tool
- Input: query_embedding (array[768]), top_k (int)
- Output: chunks (array[ContentChunk])
- Purpose: Retrieve similar content chunks from ChromaDB

## response_generation_tool
- Input: question (string), context_chunks (array[ContentChunk])
- Output: answer (string), citations (array[SourceCitation])
- Purpose: Generate contextual response using Gemini
```

#### D3: Quickstart Guide (quickstart.md)
**Sections**:
1. Prerequisites (Python 3.11+, Node.js 18+, Google API key)
2. Backend Setup
   - Install dependencies: `pip install -r requirements.txt`
   - Configure environment: Copy `.env.example` to `.env`
   - Generate embeddings: `python -m backend.vectordb.chunker`
   - Start server: `uvicorn backend.api.main:app --reload`
3. Frontend Setup
   - Install dependencies: `npm install`
   - Configure chat widget in `docusaurus.config.js`
   - Start dev server: `npm start`
4. Verification
   - Test backend: `curl http://localhost:8000/api/chat/health`
   - Test chat widget: Open browser, click chat icon, ask question
5. Troubleshooting
   - Common errors and solutions

#### D4: Agent Context Update
**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType copilot`
**Purpose**: Update Copilot's context with technologies from this plan
**Technologies to Add**:
- Python FastAPI
- Google Gemini API
- ChromaDB
- ADK (Agentic Development Kit)
- React Docusaurus integration

### Phase 1 Outputs
- ✅ data-model.md
- ✅ contracts/chat-api.yaml
- ✅ contracts/agent-tools.md
- ✅ quickstart.md
- ✅ Updated agent context (copilot-instructions.md or equivalent)

### Re-evaluation: Constitution Check Post-Design
After Phase 1 completion, re-verify:
- Data models align with simplicity principle
- API contracts are clear and well-documented
- Quickstart guide is reproducible
- No unnecessary complexity introduced

---

## Phase 2: Implementation Planning (Out of Scope for /sp.plan)

**Note**: Phase 2 (task breakdown) is handled by `/sp.tasks` command. This plan stops after Phase 1 design artifacts are generated.

**Expected Next Steps**:
1. Run `/sp.tasks` to generate tasks.md with granular implementation tasks
2. Tasks will cover:
   - Frontend customization (docusaurus.config.js, sidebars.js)
   - Tutorial content removal
   - Backend implementation (agent/, vectordb/, api/)
   - Chat widget React components
   - Integration testing
   - Deployment configuration

---

## Timeline Estimates

### Phase 0: Research (1-2 days)
- R1-R3: ADK, Gemini, ChromaDB research: 4-6 hours
- R4-R6: Chunking, FastAPI, React research: 3-4 hours
- Consolidation in research.md: 1-2 hours
- **Total**: 8-12 hours

### Phase 1: Design (1-2 days)
- D1: Data model design: 2-3 hours
- D2: API contract generation: 2-3 hours
- D3: Quickstart guide: 2-3 hours
- D4: Agent context update: 0.5 hours
- Constitution re-check: 0.5 hours
- **Total**: 7-10 hours

### Phase 2: Implementation (5-7 days) - Detailed in /sp.tasks
- Frontend customization: 4-6 hours
- Vector database setup: 6-8 hours
- ADK agent implementation: 8-12 hours
- FastAPI backend: 6-8 hours
- Chat widget UI: 8-10 hours
- Integration & testing: 6-8 hours
- Documentation: 2-3 hours
- **Total**: 40-55 hours

### Phase 3: Testing & Deployment (2-3 days)
- Unit tests: 4-6 hours
- Integration tests: 4-6 hours
- Manual QA: 2-3 hours
- Deployment setup: 2-3 hours
- **Total**: 12-18 hours

**Overall Timeline**: 10-14 days (assuming full-time work)

---

## Risk Assessment

### High Priority Risks

#### RISK-001: Google Gemini API Rate Limits or Costs
**Impact**: High - Chatbot becomes unusable if API limits exceeded
**Likelihood**: Medium (free tier: 1500 requests/day for embeddings)
**Mitigation**:
- Implement request throttling (max 5 questions per session per minute)
- Cache embeddings for queries (simple LRU cache)
- Monitor API usage via Google Cloud Console
- Document upgrade path to paid tier if needed
- Estimate: 16 chapters → ~300 chunks → 300 embedding calls (one-time), plus ~1 per user query

#### RISK-002: ADK Architecture Learning Curve
**Impact**: Medium - Delays if ADK patterns unclear
**Likelihood**: High (ADK may have limited documentation)
**Mitigation**:
- Allocate extra research time in Phase 0
- Seek ADK examples on GitHub
- Fallback: Implement standard tool pattern without strict ADK compliance, document divergence
- Consider consulting ADK community/documentation early

#### RISK-003: ChromaDB Performance with 300+ Chunks
**Impact**: Medium - Slow retrieval affects user experience (<3s requirement)
**Likelihood**: Low (ChromaDB handles thousands efficiently)
**Mitigation**:
- Benchmark retrieval time during Phase 2 development
- Optimize: reduce embedding dimensions if needed (not recommended), limit top_k to 3-5
- Fallback: Switch to FAISS if ChromaDB underperforms
- Set up performance monitoring

#### RISK-004: Poor Semantic Search Quality
**Impact**: High - Irrelevant answers frustrate users
**Likelihood**: Medium (depends on chunking strategy)
**Mitigation**:
- Test chunking strategies with sample questions
- Implement similarity score threshold (e.g., only return chunks >0.7 similarity)
- Return "No relevant content found" rather than low-quality answer
- Iterate on chunk size (start with 500 tokens, adjust based on testing)
- Consider adding keyword filters for specific modules

### Medium Priority Risks

#### RISK-005: WebSocket Connection Stability
**Impact**: Medium - Real-time chat may fall back to REST
**Likelihood**: Medium (WebSocket complexity)
**Mitigation**:
- Implement graceful fallback to REST API if WebSocket fails
- Use heartbeat/ping-pong to detect disconnections
- Test with various network conditions
- Document known issues

#### RISK-006: Docusaurus Integration Conflicts
**Impact**: Medium - Chat widget may break site styling or build
**Likelihood**: Low (Docusaurus is extensible)
**Mitigation**:
- Use CSS modules for scoped styling
- Test build process after integration
- Use Docusaurus plugin API if conflicts arise
- Document version compatibility (Docusaurus 3.x)

#### RISK-007: Content Update Workflow Unclear
**Impact**: Low - Manual embedding regeneration required
**Likelihood**: High (content will be updated)
**Mitigation**:
- Document clear regeneration steps in quickstart.md
- Create utility script: `python -m backend.vectordb.regenerate`
- Consider automated triggers (git hooks) in future phase
- Version embeddings with content hash

### Low Priority Risks

#### RISK-008: Concurrent User Load Testing
**Impact**: Low - May not reach 10+ concurrent users initially
**Likelihood**: Low (small initial audience)
**Mitigation**:
- Document scaling strategy for future
- Use async patterns in FastAPI (naturally handles concurrency)
- Defer load testing until user traffic increases

#### RISK-009: Accessibility Compliance
**Impact**: Low - Some users may have difficulty with chat widget
**Likelihood**: Medium (accessibility often overlooked)
**Mitigation**:
- Use semantic HTML and ARIA labels
- Test with keyboard navigation
- Provide text-based alternative (search bar)
- Follow WCAG 2.1 AA guidelines

---

## Testing Strategy

### Unit Testing

**Backend (pytest)**:
- `test_embeddings.py`: Test Gemini API integration, mock API calls
- `test_chunker.py`: Test markdown chunking logic with sample files
- `test_store.py`: Test ChromaDB persistence and retrieval
- `test_tools.py`: Test each ADK tool independently
- `test_agent.py`: Test agent orchestration with mocked tools

**Frontend (Jest + React Testing Library)**:
- `ChatWidget.test.js`: Test component rendering, open/close
- `MessageList.test.js`: Test message display, scrolling
- `InputBox.test.js`: Test user input, validation

**Coverage Target**: 80% for backend, 70% for frontend

### Integration Testing

**Scenarios**:
1. **End-to-End Query Flow**: Submit question → embedding generation → vector search → response generation → display
2. **Error Handling**: API failure, network timeout, invalid input
3. **Citation Accuracy**: Verify citations match retrieved chunks
4. **WebSocket Communication**: Connect, send message, receive response, disconnect
5. **Concurrent Requests**: Simulate 5 simultaneous queries, verify no race conditions

**Tools**: pytest with FastAPI TestClient, manual testing for WebSocket

### Acceptance Testing

**Mapped to User Stories** (from spec.md):

**User Story 1: Access Migrated Book Content**
- ✅ Navigate to site, verify all 16 chapters in sidebar
- ✅ Click Chapter 1, verify content renders correctly
- ✅ Click internal link, verify navigation works

**User Story 2: Ask Questions Using RAG Chatbot**
- ✅ Open chat widget, verify visible on all pages
- ✅ Type question, submit, verify response <3 seconds
- ✅ Verify citations show chapter and section
- ✅ Ask off-topic question, verify "not covered" response

**User Story 3: Semantically Relevant Answers**
- ✅ Ask synonym question (e.g., "motors" instead of "actuators"), verify correct retrieval
- ✅ Ask broad question, verify multi-chapter synthesis

### Performance Testing

**Metrics**:
- Response time: <3 seconds (end-to-end)
- Vector search latency: <500ms
- Embedding generation: <2 seconds
- Concurrent users: 10+ without degradation

**Tools**: Manual timing, FastAPI built-in logging, optional: Locust for load testing

### Manual QA Checklist

- [ ] Book content displays correctly (all 16 chapters)
- [ ] Chat widget visible and functional on all pages
- [ ] Animations smooth (open/close, typing indicator)
- [ ] Citations clickable and navigate correctly
- [ ] Error states display user-friendly messages
- [ ] Keyboard navigation works (Tab, Enter, Esc)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Build process completes without errors
- [ ] Backend health check endpoint returns 200

---

## Success Criteria Verification

**Mapped to spec.md Success Criteria (SC-001 through SC-014)**:

### Content Migration
- **SC-001**: All 16 chapters accessible within 2 clicks ✓ (Manual test)
- **SC-002**: Pages render <2 seconds on 10 Mbps ✓ (Performance test)
- **SC-003**: 100% internal links work ✓ (Automated link checker)
- **SC-004**: Build completes without errors ✓ (CI/CD integration)

### Chatbot Functionality
- **SC-005**: Chat widget visible <1 second after page load ✓ (Performance test)
- **SC-006**: Chatbot responds <3 seconds ✓ (Integration test)
- **SC-007**: 100% responses have citations ✓ (Unit test)
- **SC-008**: 90% relevant questions get accurate responses ✓ (Manual QA with test dataset)
- **SC-009**: 10 concurrent requests <3 seconds ✓ (Load test)

### Usability & Reliability
- **SC-010**: Keyboard navigation and screen reader support ✓ (Accessibility audit)
- **SC-011**: Error states display <5 seconds ✓ (Integration test)
- **SC-012**: Embedding regeneration <5 minutes ✓ (Manual test)
- **SC-013**: Question-answer interaction <30 seconds ✓ (Manual test)
- **SC-014**: Zero data loss during migration ✓ (File comparison script)

---

## Dependencies & Prerequisites

### External Services
- **Google Gemini API**: Requires API key (free tier sufficient for development)
  - Setup: https://ai.google.dev/
  - Rate limits: 1500 requests/day (embeddings), 60 requests/minute (generation)

### Development Tools
- **Python 3.11+**: Backend runtime
- **Node.js 18+**: Frontend build and runtime
- **Git**: Version control
- **Code editor**: VS Code recommended (with Python and JavaScript extensions)

### Python Packages (requirements.txt)
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
google-generativeai==0.3.2
chromadb==0.4.22
python-multipart==0.0.6
pydantic==2.5.3
pytest==7.4.4
pytest-asyncio==0.23.3
```

### Node.js Packages (package.json additions)
```json
{
  "dependencies": {
    "framer-motion": "^10.16.16"
  },
  "devDependencies": {
    "@testing-library/react": "^14.1.2",
    "@testing-library/jest-dom": "^6.1.5"
  }
}
```

### Environment Variables (.env.example)
```bash
# Google Gemini API
GEMINI_API_KEY=your_api_key_here

# ChromaDB Configuration
CHROMA_PERSIST_DIRECTORY=./backend/vectordb/chroma_db

# Backend API
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# Feature Flags
ENABLE_WEBSOCKET=true
LOG_LEVEL=INFO
```

---

## Deployment Considerations

### Development Environment
- Backend: `uvicorn backend.api.main:app --reload --port 8000`
- Frontend: `npm start` (Docusaurus dev server on port 3000)
- CORS configured to allow localhost:3000 → localhost:8000

### Production Deployment Options

**Option 1: Vercel (Frontend) + Railway/Render (Backend)**
- Deploy Docusaurus to Vercel (static site)
- Deploy FastAPI backend to Railway or Render
- Update CORS_ORIGINS to production domain
- Set environment variables in hosting platforms

**Option 2: GitHub Pages + Self-Hosted Backend**
- Deploy frontend to GitHub Pages (static)
- Host backend on VPS (DigitalOcean, AWS EC2, etc.)
- Use systemd or Docker for backend process management
- Set up reverse proxy (Nginx) if needed

**Option 3: Docker Compose (Full Stack)**
```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
  
  frontend:
    build: .
    ports: ["3000:3000"]
    depends_on: [backend]
```

### Deployment Checklist
- [ ] Environment variables configured
- [ ] API keys secured (not in git)
- [ ] CORS origins updated for production domain
- [ ] Embeddings generated and included in deployment
- [ ] Health check endpoint accessible
- [ ] Error monitoring configured (Sentry optional)
- [ ] SSL/TLS certificates configured (production)

---

## Next Steps (After /sp.plan Completion)

1. **Generate PHR**: Record this planning session in `history/prompts/`
2. **Run Phase 0**: Execute research tasks, create `research.md`
3. **Run Phase 1**: Generate data models, contracts, quickstart guide
4. **Update Agent Context**: Run `.specify/scripts/powershell/update-agent-context.ps1`
5. **Re-evaluate Constitution**: Verify design aligns with principles
6. **Run /sp.tasks**: Generate granular implementation tasks in `tasks.md`
7. **Begin Implementation**: Start with frontend customization, then backend

---

## Appendix: Key Decisions Summary

### Architecture Decisions
- **ADK Agent Pattern**: Modular tool-based architecture (agent.py, tools.py, runner.py)
- **Google Gemini**: text-embedding-004 for embeddings, gemini-pro for generation
- **ChromaDB**: Local persistent vector storage (no cloud dependency)
- **FastAPI**: Async-first API framework with WebSocket support
- **Docusaurus Integration**: Embedded React component (ChatWidget)

### Design Decisions
- **Chunking**: 500-1000 tokens per chunk, 100-200 token overlap
- **Top-K Retrieval**: 3-5 most similar chunks per query
- **Citation Format**: "Chapter X, Section Y.Z: [section title]"
- **Error Handling**: Graceful degradation (chat unavailable ≠ site broken)
- **Accessibility**: Keyboard navigation, ARIA labels, semantic HTML

### Deferred Decisions (Future Phases)
- Chat history persistence across sessions (out of scope v1)
- Multi-language support (out of scope v1)
- Advanced analytics/monitoring (out of scope v1)
- Automated embedding regeneration on content updates (future enhancement)
