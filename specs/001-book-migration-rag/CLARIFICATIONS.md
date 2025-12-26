# Clarifications for RAG Agent Implementation

**Date**: 2025-12-25  
**Feature**: Book Content Migration & RAG Chatbot Integration  
**Branch**: `001-book-migration-rag`

---

## Questions Asked & Answers Provided

### 1. ADK Framework & Package Details ✅ RESOLVED

**Question**: What specific ADK framework are you referring to?

**Answer**: 
- **Package**: `google-adk` (v1.15.0) - Already installed ✅
- **Additional Package**: `google-genai` (v1.36.0) - Also installed ✅
- **Import Pattern**: 
  ```python
  from google.adk.agents import LlmAgent
  from google.adk import Runner
  ```

**Verification Results**:
```bash
# Installed packages confirmed:
google-adk                    1.15.0
google-genai                  1.36.0  
google-generativeai           0.8.5

# Import test passed:
from google.adk.agents import LlmAgent  # ✅ Works
from google.adk import Agent, Runner    # ✅ Works
```

**Agent Pattern** (from user example):
```python
def get_capital_city(country: str) -> str:
    """Retrieves the capital city for a given country."""
    capitals = {"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"}
    return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")

capital_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="You are an agent that provides the capital city of a country...",
    tools=[get_capital_city]  # Provide function directly
)
```

**Documentation Source**: Google ADK Python SDK documentation (to be researched in Phase 0)

---

### 2. Deployment Target ✅ RESOLVED

**Question**: Where will this be deployed?

**Answer**:
- **Current**: Local development (localhost)
  - Frontend: `http://localhost:3000` (Docusaurus)
  - Backend: `http://localhost:8000` (FastAPI)
- **Future**: GitHub Pages + separate backend hosting

**Implications**:
- Need environment-based API URL configuration
- Frontend must handle both localhost and production API URLs
- Backend needs CORS configuration for cross-origin requests
- Suggested env variable: `VITE_API_URL` or `REACT_APP_API_URL`

**Implementation Approach**:
```javascript
// Frontend config
const API_URL = process.env.VITE_API_URL || 'http://localhost:8000';
```

**Backend Deployment Options** (for future):
- Option A: Railway.app (free tier)
- Option B: Vercel serverless functions
- Option C: Google Cloud Run
- Option D: AWS Lambda + API Gateway

**Decision**: Start with localhost, add config for future deployment

---

### 3. Gemini API Key ✅ RESOLVED

**Question**: Where is the API key stored?

**Answer**:
- **Location**: `C:\Users\Noman traders\Desktop\Projects\Book_with_speckit\.env`
- **Variable Name**: `GEMINI_API_KEY`
- **Value**: `AIzaSyB4rLurfsRZLreZmAbmxct_pRvdAqn-tBg` ✅ Found
- **Status**: Already configured and ready to use

**Security Note**: 
- ⚠️ Never commit `.env` to git
- Create `.env.example` template without actual key
- Add `.env` to `.gitignore` (verify it's already there)

**Usage Pattern**:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
```

---

### 4. Book Content Updates ✅ RESOLVED

**Question**: Are there any updates needed to book content before creating embeddings?

**Answer**: "for now i have no updates for book if you think that we need to upgrade book then before creating embeddings update it"

**Current Content Status**:
- 16 chapters organized in 4 modules
- Module 1: Physical AI (4 chapters)
- Module 2: ROS2 (4 chapters)
- Module 3: Simulation (4 chapters)
- Module 4: Isaac (4 chapters)

**Action Items**:
1. ✅ **Phase 1 Task**: Quick content audit
   - Check for TODO markers
   - Verify all chapters are complete
   - Remove tutorial/sample content
   - Ensure consistent formatting

2. ✅ **Decision**: Proceed with existing content unless issues found during audit

**Suggested Audit Checklist**:
- [ ] All 16 chapters have substantive content (>500 words)
- [ ] No placeholder text like "TODO", "Coming soon"
- [ ] Code blocks are properly formatted
- [ ] Images have valid paths
- [ ] Internal links work correctly
- [ ] Markdown syntax is valid

---

### 5. Implementation Methodology ✅ RESOLVED

**Question**: What development approach should be followed?

**Answer**: "use speckit plus instructions as good approach verify changes on every steps and follow best practices"

**Interpreted Requirements**:

#### Spec-Driven Development (SDD-RI)
- ✅ Follow constitution principles (7 principles)
- ✅ Maintain PHR (Prompt History Records) for all user inputs
- ✅ Create ADRs for architecturally significant decisions
- ✅ Verify changes at each step
- ✅ Test-first approach

#### Verification Checkpoints
- After each phase completion
- Before moving to next phase
- Constitution check after Phase 1 design
- Test validation after each implementation task

#### Best Practices to Follow
1. **Modularity**: Separate agent, tools, runner files
2. **Type Safety**: Use Python type hints throughout
3. **Error Handling**: Graceful degradation
4. **Documentation**: Docstrings for all functions
5. **Testing**: Unit + integration tests
6. **Code Review**: Self-review before marking complete

#### ADR Triggers (Architecturally Significant Decisions)
- ✅ **ADR-001**: Chunking strategy (size, overlap, method)
- ✅ **ADR-002**: Vector DB schema and metadata design
- ✅ **ADR-003**: Agent tool architecture and interfaces
- ✅ **ADR-004**: API design (REST vs WebSocket)
- ✅ **ADR-005**: Chat widget animation approach

**Process**:
1. Implement feature
2. Run tests
3. Verify against spec
4. Document decision if architectural
5. Create PHR entry
6. Checkpoint review

---

## Additional Clarifications

### Environment Setup ✅ CONFIRMED

**Python Version**: 3.12.4 (64-bit) ✅
**Node.js Version**: (To be checked)
**Docusaurus Version**: 3.9.2 ✅

**Key Dependencies Installed**:
- ✅ `google-adk` 1.15.0
- ✅ `google-genai` 1.36.0
- ✅ `google-generativeai` 0.8.5
- ✅ Docusaurus 3.9.2
- ✅ React 19.0.0

**Still Needed**:
- FastAPI (`pip install fastapi uvicorn`)
- ChromaDB (`pip install chromadb`)
- python-dotenv (`pip install python-dotenv`)
- pytest (`pip install pytest pytest-asyncio`)

---

## Open Questions for Phase 0 Research

These will be addressed during research phase:

1. **Google ADK Documentation**:
   - What's the official documentation URL for `google-adk`?
   - Best practices for tool creation
   - Agent lifecycle management
   - Runner configuration options

2. **Chunking Strategy**:
   - Optimal chunk size for technical book content?
   - Overlap strategy to preserve context?
   - Handling of code blocks, tables, images?

3. **Vector DB Design**:
   - ChromaDB collection schema
   - Metadata fields to store
   - Indexing strategy
   - Query optimization

4. **Frontend Integration**:
   - Best animation library (framer-motion vs CSS-only)?
   - WebSocket vs REST for chat?
   - State management approach?

---

## Summary

| Question | Status | Answer Summary |
|----------|--------|----------------|
| ADK Framework | ✅ RESOLVED | `google-adk` + `google-genai` (already installed) |
| Deployment | ✅ RESOLVED | Local now, GitHub Pages + backend hosting later |
| API Key | ✅ RESOLVED | Found in `.env` as `GEMINI_API_KEY` |
| Content Updates | ✅ RESOLVED | Quick audit in Phase 1, proceed with existing |
| Methodology | ✅ RESOLVED | SDD-RI with checkpoints and ADRs |

**All blocking questions resolved ✅**

**Ready to proceed with**:
- Phase 0: Research (ADK docs, chunking, vector DB)
- Phase 1: Frontend audit + updates
- Phase 2+: Implementation as planned

---

**Next Action**: Update `plan.md` to incorporate these clarifications and proceed with Phase 0 research.
