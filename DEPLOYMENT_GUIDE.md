# Deployment Guide - Render

## 🚀 Quick Deploy to Render

### **Option 1: Automatic Deploy (Recommended)**
1. Push your code to GitHub
2. Connect your GitHub repo to Render
3. Render will automatically use `render.yaml` configuration
4. Database and web service will be created automatically

### **Option 2: Manual Setup**

#### **Step 1: Create PostgreSQL Database**
1. Go to Render Dashboard
2. Click "New" → "PostgreSQL"
3. Name: `mechanic-api-db`
4. Database Name: `mechanic_api_db`
5. User: `mechanic_user`
6. Copy the connection string

#### **Step 2: Create Web Service**
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `mechanic-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn flask_app:app`

#### **Step 3: Set Environment Variables**
Add these environment variables in Render:
- `DATABASE_URL`: (from your PostgreSQL database)
- `SECRET_KEY`: (generate a secure random key)
- `FLASK_ENV`: `production`

## 🔧 Local Development Setup

### **Environment Variables**
Update your `.env` file with actual values:
```
DATABASE_URL=postgresql://username:password@hostname:port/database_name
SECRET_KEY=your-super-secret-production-key-here
FLASK_ENV=production
```

### **Run Locally with Production Config**
```bash
# Install dependencies
pip install -r requirements.txt

# Load environment variables and run
python flask_app.py
```

### **Run with Gunicorn (Production Server)**
```bash
gunicorn flask_app:app
```

## 📁 File Structure Changes

### **New Files:**
- `flask_app.py` (renamed from app.py)
- `.env` (environment variables)
- `.gitignore` (excludes sensitive files)
- `Procfile` (Render deployment)
- `render.yaml` (automatic deployment config)

### **Updated Files:**
- `config.py` (added ProductionConfig)
- `requirements.txt` (added gunicorn, psycopg2-binary)

## 🔒 Security Notes

- ✅ `.env` file is in `.gitignore`
- ✅ Sensitive data stored as environment variables
- ✅ Production config uses environment variables
- ✅ Debug mode disabled in production

## 🌐 Access Your Deployed API

Once deployed, your API will be available at:
- **Base URL**: `https://your-app-name.onrender.com`
- **Swagger Docs**: `https://your-app-name.onrender.com/docs`
- **Health Check**: `https://your-app-name.onrender.com/`

## 🧪 Testing Production Deployment

Update your Postman environment:
- `base_url`: `https://your-app-name.onrender.com`

All your existing Postman tests will work with the production URL!

## 🔄 CI/CD Pipeline

With `render.yaml`, every push to your main branch will:
1. Automatically trigger a new deployment
2. Install dependencies
3. Start the application with Gunicorn
4. Update environment variables as needed

Your Mechanic API is now production-ready! 🎉