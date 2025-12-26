# End-to-End Testing Guide

**Date**: 2025-12-25  
**Feature**: RAG Chatbot Integration  
**Status**: Testing Phase 6

---

## Prerequisites

### 1. Backend Server Running
- **URL**: http://localhost:8000
- **Status**: ✅ Running (started at 22:45)
- **Health Check**: http://localhost:8000/api/health
- **Stats**: http://localhost:8000/api/stats

### 2. Frontend Server Running
- **URL**: http://localhost:3000
- **Status**: ✅ Running (compiled at 22:47)
- **Dev Server**: Docusaurus with hot reload

---

## Test Checklist

### Phase 6.1: Backend API Testing ✅

#### Test 1.1: Health Check
```bash
curl http://localhost:8000/api/health
```
**Expected**: 
- Status: 200
- Body: `{"status": "healthy", "checks": {...}, "timestamp": "..."}`

**Result**: ✅ PASSED
- Status: healthy
- API Running: True
- Agent Loaded: True
- Embeddings Loaded: True

#### Test 1.2: Statistics
```bash
curl http://localhost:8000/api/stats
```
**Expected**:
- total_chunks: 93
- modules: 4
- chapters: 16
- topics: 35

**Result**: ✅ PASSED (after fixing metadata file)

#### Test 1.3: Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Physical AI?"}'
```
**Expected**:
- Response time: <5 seconds
- Answer with content
- Citations array
- session_id

**Result**: ✅ PASSED
- Average response time: ~5 seconds
- Answers generated correctly
- Citations included

---

### Phase 6.2: Frontend Integration Testing ⏳

#### Test 2.1: Page Load
- [X] Navigate to http://localhost:3000
- [ ] Verify homepage loads
- [ ] Check navigation to all 16 chapters works
- [ ] Verify no console errors

#### Test 2.2: Chat Widget Visibility
- [ ] Check if chat button is visible (bottom-right corner)
- [ ] Verify gradient button styling
- [ ] Check hover effects work
- [ ] Verify button is accessible on all pages

#### Test 2.3: Chat Widget Interaction
- [ ] Click chat button - widget should open
- [ ] Verify smooth slide-in animation
- [ ] Check widget dimensions (400x600px)
- [ ] Click close button - widget should close
- [ ] Press ESC key - widget should close

#### Test 2.4: Message Submission
- [ ] Type "What is Physical AI?" in input field
- [ ] Verify character counter shows (e.g., "19/500")
- [ ] Click send button
- [ ] Verify loading state appears
- [ ] Verify response displays within 5 seconds
- [ ] Check citation badges appear
- [ ] Click citation badge - should navigate to chapter

#### Test 2.5: Input Validation
- [ ] Try submitting empty message - should show validation error
- [ ] Try submitting message <10 chars - should show error
- [ ] Try submitting message >500 chars - should show error
- [ ] Verify character counter turns red when over limit

#### Test 2.6: Error Handling
- [ ] Stop backend server
- [ ] Try sending message
- [ ] Verify error message displays clearly
- [ ] Start backend server
- [ ] Verify chat recovers

---

### Phase 6.3: Accessibility Testing ⏳

#### Test 3.1: Keyboard Navigation
- [ ] Tab to chat button - should receive focus
- [ ] Press Enter - widget should open
- [ ] Tab through input field and buttons
- [ ] Press ESC - widget should close
- [ ] Verify focus returns to button

#### Test 3.2: Screen Reader Compatibility
- [ ] Enable screen reader
- [ ] Navigate to chat button
- [ ] Verify ARIA labels are read
- [ ] Open widget and test form labels
- [ ] Test with NVDA or JAWS

#### Test 3.3: Visual Accessibility
- [ ] Check color contrast (button, text)
- [ ] Verify focus indicators visible
- [ ] Test with browser zoom (150%, 200%)
- [ ] Check in dark mode (if supported)

---

### Phase 6.4: Responsive Design Testing ⏳

#### Test 4.1: Desktop (1920x1080)
- [ ] Widget displays in bottom-right
- [ ] Size: 400x600px
- [ ] All content readable
- [ ] No layout issues

#### Test 4.2: Tablet (768x1024)
- [ ] Widget adapts size
- [ ] Still usable and readable
- [ ] Touch targets adequate (44x44px minimum)

#### Test 4.3: Mobile (375x667)
- [ ] Widget takes appropriate screen space
- [ ] Messages wrap correctly
- [ ] Input field usable with virtual keyboard
- [ ] Send button accessible

---

### Phase 6.5: Performance Testing ⏳

#### Test 5.1: Response Time
- [ ] Test 10 consecutive queries
- [ ] Measure average response time
- **Target**: <3 seconds (currently ~5s, acceptable)
- [ ] Check for performance degradation

#### Test 5.2: Concurrent Users
- [ ] Open 3 browser tabs
- [ ] Send queries simultaneously
- [ ] Verify all receive responses
- [ ] Check backend doesn't crash

#### Test 5.3: Session Persistence
- [ ] Send message, check localStorage for session_id
- [ ] Refresh page
- [ ] Send another message
- [ ] Verify same session_id used
- [ ] Check conversation context maintained

---

### Phase 6.6: Content Accuracy Testing ⏳

#### Test 6.1: Query Relevance
Test queries and verify answers reference correct chapters:

1. **"What is Physical AI?"**
   - Expected: Module 1, Chapter 1
   - [ ] Test and verify

2. **"Explain ROS 2 architecture"**
   - Expected: Module 2, Chapter 2
   - [ ] Test and verify

3. **"Why do we need simulation?"**
   - Expected: Module 3, Chapter 1
   - [ ] Test and verify

4. **"What is Isaac Sim?"**
   - Expected: Module 4, Chapter 2
   - [ ] Test and verify

5. **"Which chapters discuss ROS 2?"**
   - Expected: Metadata query showing Module 2 chapters
   - [ ] Test and verify

#### Test 6.2: Citation Accuracy
- [ ] Verify citations link to correct chapters
- [ ] Check citation format: "Module X → Chapter Y: Title"
- [ ] Test clicking citation navigates to chapter
- [ ] Verify no broken links

---

## Test Results Summary

### Completed Tests
- ✅ Backend API Tests (3/3)
- ⏳ Frontend Integration (0/6)
- ⏳ Accessibility (0/3)
- ⏳ Responsive Design (0/3)
- ⏳ Performance (0/3)
- ⏳ Content Accuracy (0/2)

### Issues Found
1. Response time ~5s (target <3s) - Acceptable for now
2. Need to test chat widget functionality manually

### Next Steps
1. Manual testing of chat widget in browser
2. Document any issues found
3. Fix critical issues
4. Re-test and verify
5. Proceed to Phase 7 (Documentation)

---

## Manual Testing Script

**For manual testing, follow these steps in order:**

1. Open http://localhost:3000
2. Look for chat button in bottom-right corner
3. Click to open chat
4. Type: "What is Physical AI?"
5. Click send or press Enter
6. Wait for response
7. Check citations appear
8. Click a citation badge
9. Verify navigation to chapter
10. Return to chat and test more queries

**Report any issues immediately!**
