# Deployment Configuration Guide

**Last Updated**: December 25, 2025

This guide shows you exactly where to paste your URLs when deploying the application.

---

## 📋 What You Need

Before deploying, you'll need:
1. ✅ **Google API Key** - Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. ✅ **Frontend Host** - Vercel, Netlify, or GitHub Pages
3. ✅ **Backend Host** - Railway, Render, or Heroku

---

## 🎯 Configuration Locations

### 1️⃣ Frontend: Docusaurus Site URL

**When**: After you deploy to Vercel/Netlify  
**File**: `Future Ai And Robotics/docusaurus.config.js`  
**Lines**: 6-7

```javascript
module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Guide to Building Intelligent Physical Systems',
  
  // 👇 CHANGE THESE TO YOUR DEPLOYED URLS
  url: 'https://YOUR-SITE.vercel.app',        // ← PASTE YOUR FRONTEND URL HERE
  baseUrl: '/',                                // ← Keep as '/' (don't change)
  
  onBrokenLinks: 'throw',
  // ... rest stays the same
```

**Example:**
```javascript
url: 'https://physical-ai-book.vercel.app',
```

---

### 2️⃣ Backend: API URL in Chat Widget

**When**: After you deploy backend to Railway/Render  
**File**: `Future Ai And Robotics/src/components/ChatWidget/ChatWidget.js`  
**Line**: 46

**Current (Development):**
```javascript
const response = await fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: inputText, session_id: sessionId })
});
```

**Change To (Production):**
```javascript
// Add this at the top of the file (after imports)
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Then update the fetch call
const response = await fetch(`${API_URL}/api/chat`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: inputText, session_id: sessionId })
});
```

**Then set environment variable in Vercel/Netlify:**
```
REACT_APP_API_URL=https://your-backend.railway.app
```

---

### 3️⃣ Backend: CORS Configuration

**When**: After deploying frontend  
**Where**: Your hosting platform (Railway/Render)  
**Environment Variable**: `CORS_ORIGINS`

**Railway Example:**
```
CORS_ORIGINS=https://your-site.vercel.app,https://www.your-site.vercel.app
```

**Render Example:**
1. Go to Dashboard → Your Service
2. Environment → Add Environment Variable
3. Key: `CORS_ORIGINS`
4. Value: `https://your-site.vercel.app`

---

### 4️⃣ Backend: Google API Key

**When**: Before deploying backend  
**Where**: Your hosting platform (Railway/Render)  
**Environment Variable**: `GOOGLE_API_KEY`

**⚠️ NEVER COMMIT THIS TO GIT!**

**Railway:**
1. Dashboard → Your Service
2. Variables → New Variable
3. Name: `GOOGLE_API_KEY`
4. Value: `AIza...your_key_here`
5. Click "Add"

**Render:**
1. Dashboard → Your Service
2. Environment → Add Environment Variable
3. Key: `GOOGLE_API_KEY`
4. Value: `AIza...your_key_here`
5. Save

---

## 🚀 Step-by-Step Deployment

### Phase 1: Deploy Backend First

#### Option A: Railway (Recommended)

1. **Sign up**: https://railway.app
2. **Create New Project** → Deploy from GitHub
3. **Select Repository**: `Book_with_speckit`
4. **Root Directory**: Select `backend`
5. **Add Environment Variables**:
   ```
   GOOGLE_API_KEY=AIza...your_key_here
   CORS_ORIGINS=http://localhost:3000  (update later)
   ```
6. **Deploy** - Railway will auto-detect Python and run
7. **Get URL**: Something like `https://your-app.railway.app`
8. **Test**: Visit `https://your-app.railway.app/api/health`

#### Option B: Render

1. **Sign up**: https://render.com
2. **New** → Web Service
3. **Connect Repository**: `Book_with_speckit`
4. **Root Directory**: `backend`
5. **Build Command**: `pip install -r requirements.txt`
6. **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
7. **Add Environment Variables**:
   - `GOOGLE_API_KEY`
   - `CORS_ORIGINS`
8. **Create Web Service**
9. **Get URL**: Something like `https://your-app.onrender.com`

---

### Phase 2: Deploy Frontend

#### Option A: Vercel (Recommended)

1. **Sign up**: https://vercel.com
2. **New Project** → Import from GitHub
3. **Select Repository**: `Book_with_speckit`
4. **Root Directory**: `Future Ai And Robotics`
5. **Framework Preset**: Docusaurus
6. **Build Command**: `npm run build`
7. **Output Directory**: `build`
8. **Add Environment Variable**:
   ```
   REACT_APP_API_URL=https://your-backend.railway.app
   ```
9. **Deploy**
10. **Get URL**: Something like `https://your-site.vercel.app`

#### Option B: Netlify

1. **Sign up**: https://netlify.com
2. **New Site** → Import from GitHub
3. **Select Repository**: `Book_with_speckit`
4. **Base Directory**: `Future Ai And Robotics`
5. **Build Command**: `npm run build`
6. **Publish Directory**: `build`
7. **Environment Variables**:
   ```
   REACT_APP_API_URL=https://your-backend.railway.app
   ```
8. **Deploy**
9. **Get URL**: Something like `https://your-site.netlify.app`

---

### Phase 3: Update Configurations

After both are deployed, update these files:

#### 1. Update CORS in Backend

Go to Railway/Render dashboard:
```
CORS_ORIGINS=https://your-site.vercel.app,https://www.your-site.vercel.app
```

#### 2. Update Docusaurus Config

Edit `docusaurus.config.js`:
```javascript
url: 'https://your-site.vercel.app',
```

Commit and push → Auto-redeploys.

#### 3. Update Chat Widget

Edit `ChatWidget.js`:
```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

Set `REACT_APP_API_URL` in Vercel/Netlify.

---

## ✅ Testing Checklist

After deployment:

### Backend Tests
```bash
# Health check
curl https://your-backend.railway.app/api/health

# Should return:
{
  "status": "healthy",
  "checks": {
    "api_running": true,
    "agent_loaded": true,
    "embeddings_loaded": true
  }
}

# Stats check
curl https://your-backend.railway.app/api/stats

# Should return:
{
  "total_chunks": 93,
  "modules": 4,
  "chapters": 16,
  "topics": 35
}
```

### Frontend Tests
1. Visit: `https://your-site.vercel.app`
2. Click chat button (💬)
3. Type: "What is Physical AI?"
4. Verify: Response appears with citations
5. Test: Dark mode toggle works
6. Test: Responsive design (resize browser)

---

## 🐛 Troubleshooting

### Issue: CORS Error in Browser Console

**Error**: `Access to fetch at ... from origin ... has been blocked by CORS`

**Solution**: Update `CORS_ORIGINS` in backend environment:
```
CORS_ORIGINS=https://your-exact-frontend-url.vercel.app
```

### Issue: Chat Returns Errors

**Check**:
1. Backend health: `https://your-backend.railway.app/api/health`
2. Environment variable `GOOGLE_API_KEY` is set
3. Frontend has correct `REACT_APP_API_URL`

### Issue: 404 Not Found

**Solution**: Check root directory settings:
- Backend: Must point to `backend/`
- Frontend: Must point to `Future Ai And Robotics/`

---

## 📊 Summary Table

| What | Where to Paste | When |
|------|---------------|------|
| Frontend URL | `docusaurus.config.js` line 7 | After frontend deployed |
| Backend API URL | Environment var `REACT_APP_API_URL` | Before frontend deploy |
| Backend API URL | `ChatWidget.js` line 46 (code change) | Before frontend deploy |
| CORS Origins | Backend env var `CORS_ORIGINS` | After frontend deployed |
| Google API Key | Backend env var `GOOGLE_API_KEY` | Before backend deploy |

---

## 🔒 Security Reminders

- ✅ **Never commit** `.env` file
- ✅ **Never hardcode** API keys in source code
- ✅ **Always use** environment variables on hosting platform
- ✅ **Rotate keys** if accidentally exposed
- ✅ **Set CORS** to specific domain (not `*`)

---

## 📞 Need Help?

Common issues and solutions:
1. **Backend won't start**: Check Python version (3.10+)
2. **Frontend build fails**: Check Node version (18+)
3. **Chat doesn't work**: Check browser console for errors
4. **Slow responses**: Normal (5-10s for first request)

---

**Deployment Status**: Ready for production 🚀  
**Estimated Time**: 30-45 minutes total
