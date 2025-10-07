# Render Deployment Steps

## 🚀 Deploy Web Service on Render

### **Step 1: Create Web Service**
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure service:
   - **Name**: `mechanic-api` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn flask_app:app`
   - **Instance Type**: Free (or paid for production)

### **Step 2: Set Environment Variables**
In the Render dashboard, add these environment variables:
- `DATABASE_URL`: `postgresql://admin:securepass@db-abcd1234.render.com:5432/mechanic_shop`
- `SECRET_KEY`: `your-super-secret-production-key-here`
- `FLASK_ENV`: `production`

### **Step 3: Deploy**
1. Click "Create Web Service"
2. Wait for deployment to complete
3. Note your service URL: `https://your-app-name.onrender.com`

## 📝 Update Swagger Configuration

After deployment, update the host in `app/swagger_config.py`:
```python
"host": "your-actual-app-name.onrender.com",  # Replace with your actual URL
"schemes": ["https"],
```

## 🔐 GitHub Secrets Setup

### **Step 1: Get Render Credentials**
1. Go to Render Dashboard → Account Settings → API Keys
2. Create new API key and copy it
3. Get your Service ID from the service URL or dashboard

### **Step 2: Add GitHub Secrets**
1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Add repository secrets:
   - `RENDER_SERVICE_ID`: Your service ID from Render
   - `RENDER_API_KEY`: Your API key from Render

## 🔄 CI/CD Pipeline

The workflow will trigger on:
- ✅ Push to main branch
- ✅ Pull requests to main branch

Pipeline stages:
1. **Build**: Install dependencies and lint code
2. **Test**: Run all unit tests
3. **Deploy**: Deploy to Render (only on main branch)

## 🧪 Testing Deployment

Once deployed, test your API:
- **Base URL**: `https://your-app-name.onrender.com`
- **Health Check**: `https://your-app-name.onrender.com/`
- **Swagger Docs**: `https://your-app-name.onrender.com/docs`

Update your Postman environment:
- `base_url`: `https://your-app-name.onrender.com`

## 🎉 You're Live!

Your Mechanic API is now:
- ✅ Deployed on Render with PostgreSQL
- ✅ Using HTTPS with proper SSL
- ✅ Automated CI/CD pipeline
- ✅ Environment variables secured
- ✅ Ready for production use!