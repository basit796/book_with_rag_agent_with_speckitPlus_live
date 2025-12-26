# Manual E2E Testing Guide

This document provides step-by-step instructions for manually testing the complete RAG chatbot integration.

## Prerequisites

Before starting, ensure:
- ✅ Backend dependencies installed (`pip install -r backend/requirements.txt`)
- ✅ FAISS index built (`python backend/vectordb/build_index.py`)
- ✅ `.env` file configured with `GEMINI_API_KEY`
- ✅ Frontend dependencies installed (`npm install` in `Future Ai And Robotics/`)

## Test Setup

### Terminal 1: Start Backend Server

```bash
cd backend
python3 -m uvicorn api.main:app --reload --port 8000
```

**Expected output:**
```
INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO: Started reloader process
INFO: Started server process
INFO: Waiting for application startup.
INFO: Application startup complete.
```

**Verify backend is running:**
```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "checks": {
    "api": "running",
    "agent": "loaded",
    "embeddings": "loaded"
  }
}
```

### Terminal 2: Start Frontend Server

```bash
cd "Future Ai And Robotics"
npm start
```

**Expected output:**
```
[SUCCESS] Serving "build" directory.
[INFO] Docusaurus website is running at: http://localhost:3000/
```

## E2E Test Cases

### Test 1: Widget Visibility ✅

**Steps:**
1. Open browser: `http://localhost:3000`
2. Look at bottom-right corner

**Expected:**
- ✅ Floating chat button visible (purple gradient, 💬 icon)
- ✅ Button has hover effect (scales to 1.1x)
- ✅ No console errors

**Screenshot:** Widget button in bottom-right corner

---

### Test 2: Open Chat Widget ✅

**Steps:**
1. Click the floating chat button

**Expected:**
- ✅ Chat window slides in from bottom-right
- ✅ Header shows "Book Assistant" title
- ✅ Subtitle: "Physical AI & Humanoid Robotics"
- ✅ Empty state message: "Ask me anything about the book!"
- ✅ Input box visible with placeholder text
- ✅ Close button (X) visible in header
- ✅ Smooth animation (300ms slide-in)

**Screenshot:** Open chat widget with empty state

---

### Test 3: Basic Question Submission ✅

**Steps:**
1. Open chat widget
2. Type in input: "What is physical AI?"
3. Click "Send" button (or press Enter)

**Expected:**
- ✅ User message appears on right side (blue bubble)
- ✅ Typing indicator appears (3 animated dots)
- ✅ Backend receives request (check Terminal 1)
- ✅ Bot response appears on left side (white bubble) within 3 seconds
- ✅ Response contains relevant information about physical AI
- ✅ Auto-scroll to latest message
- ✅ No console errors

**Backend log should show:**
```
INFO: POST /api/chat - 200 OK
```

**Screenshot:** Conversation with user question and bot response

---

### Test 4: Citation Display ✅

**Steps:**
1. Submit question: "What is physical AI?"
2. Check bot response

**Expected:**
- ✅ "Sources:" label visible under answer
- ✅ Citation badges displayed (e.g., "Physical AI Foundations → Introduction")
- ✅ Citations are clickable links
- ✅ Hover effect on citation badges

**Screenshot:** Bot response with citations

---

### Test 5: Citation Navigation ✅

**Steps:**
1. Click on a citation badge

**Expected:**
- ✅ New browser tab opens (or same tab navigates)
- ✅ Navigates to correct book chapter
- ✅ URL matches chapter path (e.g., `/module-1-physical-ai/01-introduction`)

---

### Test 6: Input Validation - Minimum Length ❌

**Steps:**
1. Type short message: "Hi"
2. Try to submit

**Expected:**
- ✅ Send button is disabled
- ✅ Character counter shows: "2/500 (min 10)"
- ✅ Hint message: "Please enter at least 10 characters"
- ✅ Counter text is yellow/warning color

**Screenshot:** Input validation error

---

### Test 7: Input Validation - Maximum Length ❌

**Steps:**
1. Type very long message (>500 characters)
2. Observe behavior

**Expected:**
- ✅ Input stops accepting characters at 500
- ✅ Character counter shows: "500/500" in red
- ✅ Cannot type more

---

### Test 8: Valid Input Submission ✅

**Steps:**
1. Type valid question (10-500 chars): "Explain humanoid robotics"
2. Press Enter key (not button)

**Expected:**
- ✅ Message submits (Enter key works)
- ✅ Input field clears
- ✅ Focus remains on input field
- ✅ Character counter resets to 0

---

### Test 9: Error Handling - Backend Down 🔴

**Steps:**
1. Stop backend server (Ctrl+C in Terminal 1)
2. Submit question in chat widget

**Expected:**
- ✅ User message appears
- ✅ Typing indicator shows
- ✅ After ~30 seconds, error message appears
- ✅ Error message: "Sorry, I encountered an error. Please make sure the backend server is running and try again."
- ✅ Error message has yellow/warning background
- ✅ Can submit new messages after error

**Screenshot:** Error message display

---

### Test 10: Multiple Messages ✅

**Steps:**
1. Restart backend server
2. Submit question 1: "What is ROS2?"
3. Wait for response
4. Submit question 2: "How does Isaac Sim work?"
5. Wait for response

**Expected:**
- ✅ Both conversations visible
- ✅ Messages alternate (user right, bot left)
- ✅ Timestamps visible on all messages
- ✅ Citations for both responses
- ✅ Auto-scroll to latest message
- ✅ Session ID persists (stored in localStorage)

**Check Terminal 1:**
```
INFO: POST /api/chat - session_id: session_xxxxx
INFO: POST /api/chat - session_id: session_xxxxx (same ID)
```

---

### Test 11: Close and Reopen Widget ✅

**Steps:**
1. With messages in chat, click close button (X)
2. Click floating button to reopen

**Expected:**
- ✅ Widget closes with animation
- ✅ Message history is cleared (fresh start)
- ✅ Empty state shown again
- ✅ Session ID persists (same ID used)

---

### Test 12: Keyboard Navigation ⌨️

**Steps:**
1. Close widget
2. Press Tab multiple times
3. When chat button is focused, press Enter
4. Press Tab to focus input field
5. Type message and press Enter
6. Press Escape key

**Expected:**
- ✅ Tab navigation works
- ✅ Focus outline visible on button
- ✅ Enter opens widget when button focused
- ✅ Input field receives focus when widget opens
- ✅ Enter submits message
- ✅ Escape closes widget

---

### Test 13: Multi-line Input 📝

**Steps:**
1. Type in input field: "What is"
2. Press Shift+Enter
3. Type: "physical AI?"
4. Press Enter (without Shift)

**Expected:**
- ✅ Shift+Enter creates new line (doesn't submit)
- ✅ Enter submits the multi-line message
- ✅ Message displays with line breaks preserved

---

### Test 14: Concurrent Requests ⏱️

**Steps:**
1. Open two browser windows side by side
2. In both windows, open chat widget
3. Submit different questions at same time

**Expected:**
- ✅ Both requests process successfully
- ✅ No race conditions
- ✅ Each window shows correct response
- ✅ Different session IDs in each window

**Check Terminal 1:**
```
INFO: POST /api/chat - session_id: session_aaa
INFO: POST /api/chat - session_id: session_bbb
```

---

### Test 15: Response Time ⏱️

**Steps:**
1. Submit question: "What is physical AI?"
2. Measure time from submit to response

**Expected:**
- ✅ Response appears within 3 seconds
- ✅ Typing indicator visible during wait
- ✅ Smooth transition from loading to response

**Check Terminal 1 for response_time_ms:**
```json
{
  "response_time_ms": 2458
}
```

---

### Test 16: Mobile Responsive 📱

**Steps:**
1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select "iPhone 12 Pro" preset
4. Interact with chat widget

**Expected:**
- ✅ Floating button visible (smaller: 56px)
- ✅ Chat window fills most of screen
- ✅ Messages readable
- ✅ Input field usable
- ✅ No horizontal scroll

**Test these viewports:**
- iPhone 12 Pro (390x844)
- iPad (768x1024)
- Desktop (1920x1080)

---

### Test 17: Widget on Different Pages 🔄

**Steps:**
1. Navigate to homepage (`/`)
2. Verify widget visible
3. Navigate to any chapter page
4. Verify widget visible
5. Navigate to blog page
6. Verify widget visible

**Expected:**
- ✅ Widget visible on all pages
- ✅ Widget position consistent
- ✅ No styling conflicts

---

### Test 18: Long Response Handling 📜

**Steps:**
1. Submit complex question requiring long answer
2. Observe bot response

**Expected:**
- ✅ Long text wraps correctly
- ✅ Message bubble scrollable if needed
- ✅ Citations still visible at bottom
- ✅ Auto-scroll works

---

### Test 19: Special Characters 🔤

**Steps:**
1. Submit question with special chars: "What's AI & ML?"
2. Observe response

**Expected:**
- ✅ Special characters handled correctly
- ✅ No encoding errors
- ✅ Response matches question context

---

### Test 20: Session Persistence 💾

**Steps:**
1. Open chat, submit question
2. Refresh page (F5)
3. Open chat again

**Expected:**
- ✅ New session starts (messages cleared)
- ✅ Same session ID used (from localStorage)
- ✅ No errors

**Check localStorage:**
```javascript
localStorage.getItem('chat_session_id') // should return same ID
```

---

## Performance Benchmarks

### Response Time Targets
- ✅ Widget open/close: <300ms
- ✅ Message submission: <100ms
- ✅ Backend processing: <3 seconds
- ✅ Total E2E: <3.5 seconds

### Resource Usage
- Initial bundle size: ~400KB (with framer-motion)
- API payload: ~2-5KB per request
- Backend memory: ~200MB

## Known Issues

### 1. Gemini API Rate Limits
- **Issue**: 429 errors after many requests
- **Workaround**: Wait a few minutes or upgrade API quota
- **Status**: Non-blocking (production should use higher quota)

### 2. Metadata Source Field
- **Issue**: Some citations show "source: Unknown"
- **Impact**: Minor (chapter info still displays correctly)
- **Status**: Non-blocking

## Success Criteria

All tests passing:
- ✅ 20/20 functional tests pass
- ✅ Response time <3 seconds
- ✅ No console errors
- ✅ Keyboard navigation works
- ✅ Mobile responsive
- ✅ Error handling graceful

## Test Report Template

```markdown
## E2E Test Report

**Date:** YYYY-MM-DD
**Tester:** [Name]
**Environment:** 
- OS: Windows/Mac/Linux
- Browser: Chrome/Firefox/Safari
- Node: vX.X.X
- Python: vX.X.X

### Results

| Test # | Test Name | Status | Notes |
|--------|-----------|--------|-------|
| 1 | Widget Visibility | ✅ | - |
| 2 | Open Chat Widget | ✅ | - |
| 3 | Basic Question | ✅ | Response time: 2.5s |
| ... | ... | ... | ... |

**Overall Status:** ✅ PASS / ❌ FAIL

**Issues Found:** None / [List issues]

**Recommendations:** [Any suggestions]
```

## Next Steps

After all tests pass:
1. ✅ Create Phase 5 completion PHR
2. ✅ Update IMPLEMENTATION_STATUS_RAG.md
3. ✅ Move to Phase 6 (Comprehensive Testing)
4. ✅ Move to Phase 7 (Documentation)
