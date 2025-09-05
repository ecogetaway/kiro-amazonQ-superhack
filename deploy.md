# 🚀 Deployment Guide

## Local Testing
```bash
cd /Users/sanjay/kiro-superhack
python3 -m streamlit run main.py
```
Access at: http://localhost:8501

## Deployment Options

### 1. Streamlit Cloud (Recommended)
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect GitHub repo
4. Deploy automatically

### 2. Vercel
```bash
npm i -g vercel
vercel --prod
```

### 3. Railway
```bash
railway login
railway new
railway up
```

### 4. Docker
```bash
docker build -t itsm-solution .
docker run -p 8501:8501 itsm-solution
```

### 5. Heroku
```bash
heroku create your-app-name
git push heroku main
```

## GitHub Setup
```bash
git init
git add .
git commit -m "AI-Powered ITSM Solution"
git branch -M main
git remote add origin https://github.com/yourusername/kiro-superhack.git
git push -u origin main
```