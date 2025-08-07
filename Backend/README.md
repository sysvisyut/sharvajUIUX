# Credit Score Analysis Backend

A scalable Flask + MongoDB backend for credit score analysis with ML integration, chat assistant, and PDF generation capabilities.

## 🚀 Features

- **🔐 Flexible Authentication**: Firebase Auth with testing bypass option
- **📊 Credit Score Calculation**: ML-powered scoring with fallback rules
- **💬 AI Chat Assistant**: OpenRouter API integration with context awareness  
- **📄 PDF Reports**: Professional credit reports with insights
- **📈 Dashboard Analytics**: User credit score tracking and insights
- **🗄️ MongoDB Integration**: Efficient data storage and retrieval
- **🧪 Testing Ready**: Auth bypass and development modes

## 🏗️ Architecture

```
credit_score_app/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── app.py                   # Application entry point
│   ├── auth/
│   │   ├── auth.py              # Authentication with Firebase/bypass
│   ├── api/
│   │   ├── routes.py            # Main API endpoints
│   ├── models/
│   │   ├── database.py          # MongoDB models and queries
│   ├── services/
│   │   ├── ml_service.py        # Credit scoring ML service
│   │   ├── chat_service.py      # OpenRouter chat integration
│   │   └── pdf_service.py       # PDF generation service
│   └── utils/
├── config/
│   └── config.py                # Configuration management
├── docs/
│   └── mongodb_schema.md        # Database schema documentation
├── ml_models/                   # ML model storage
├── tests/                       # Test files
├── requirements.txt             # Python dependencies
└── .env.example                 # Environment variables template
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- MongoDB (local or cloud)
- OpenRouter API key (optional)
- Firebase credentials (optional for production)

### Setup

1. **Clone and navigate to project**
   ```bash
   cd credit_score_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start MongoDB**
   ```bash
   # Local MongoDB
   mongod
   
   # Or use MongoDB Atlas cloud connection string in .env
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `FLASK_CONFIG` | Environment (development/production) | development | No |
| `SECRET_KEY` | Flask secret key | auto-generated | Yes |
| `MONGO_URI` | MongoDB connection string | mongodb://localhost:27017/credit_score_db | Yes |
| `OPENROUTER_API_KEY` | OpenRouter API key for chat | None | No |
| `FIREBASE_CREDENTIALS_PATH` | Firebase service account JSON | None | No |
| `BYPASS_AUTH` | Enable auth bypass for testing | true (dev) | No |
| `ML_MODEL_LOCAL` | Use local ML model | true | No |

### Testing vs Production

**Development/Testing Mode:**
- Set `BYPASS_AUTH=true` in .env
- Use `/auth/test-login` endpoint
- No Firebase setup required

**Production Mode:**
- Set `BYPASS_AUTH=false`
- Configure Firebase credentials
- Use proper authentication flow

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Firebase authentication | No |
| POST | `/auth/test-login` | Test authentication (dev only) | No |
| POST | `/auth/verify` | Verify authentication token | Yes |

### Core Features

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/dashboard` | Get user dashboard data | Yes |
| POST | `/api/submit-score` | Submit financial data & calculate score | Yes |
| GET | `/api/insights` | Get detailed credit insights | Yes |
| POST | `/api/chat` | Chat with AI assistant | Yes |
| GET | `/api/chat/suggestions` | Get suggested chat questions | No |
| GET | `/api/chat/history` | Get chat history | Yes |
| POST | `/api/generate-pdf` | Generate PDF report | Yes |

### Health Check

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/health` | API health status | No |
| GET | `/` | API information | No |

## 💾 Database Schema

### Collections

**users** - User account information
**financial_data** - User financial submissions
**credit_scores** - Calculated credit scores and results
**chat_history** - Chat conversation history

See `docs/mongodb_schema.md` for detailed schema documentation.

## 🧠 ML Model Integration

### Local Model
Place your trained model in `ml_models/` directory and update the loading logic in `MLService`.

### API Model
Set `ML_MODEL_LOCAL=false` and `ML_MODEL_URL` to your model API endpoint.

### Fallback System
Rule-based scoring system provides fallback when ML models fail.

## 💬 Chat Integration

The chat system uses OpenRouter API with the Horizon Beta model for intelligent financial advice.

**Features:**
- Context-aware responses using user's credit data
- Fallback responses when API unavailable
- Conversation history tracking
- Suggested questions

## 📄 PDF Generation

Professional PDF reports include:
- Credit score summary with color coding
- Score factor breakdown
- Personal and financial information
- Personalized insights and recommendations
- Professional formatting and styling

## 🧪 Testing

### Quick Test (No Auth)
```bash
# Test health endpoint
curl http://localhost:5000/health

# Test login bypass (development)
curl -X POST http://localhost:5000/auth/test-login

# Test dashboard with bypass
curl -H "Authorization: Bearer test-token" http://localhost:5000/api/dashboard
```

### Example Financial Data Submission
```json
{
  "personal_info": {
    "age": 28,
    "state": "CA", 
    "education_level": "Bachelor's"
  },
  "employment_income": {
    "employment_type": "Full-time",
    "annual_income": 65000,
    "job_duration": "2 years"
  },
  "housing": {
    "monthly_cost": 2000,
    "mortgage": 0,
    "savings": 15000,
    "balance": 5000
  },
  "family": {
    "dependents": 0
  },
  "credit_loans": {
    "existing_loans": 1,
    "loan_payments": 300,
    "credit_cards": 2
  },
  "credit_behavior": {
    "inquiries": 1,
    "late_payments": 0,
    "bankruptcy": false,
    "credit_history_length": 3
  }
}
```

## 🚀 Deployment

### Heroku
```bash
# Create Heroku app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_CONFIG=production
heroku config:set BYPASS_AUTH=false
heroku config:set MONGO_URI=your-mongodb-atlas-uri

# Deploy
git push heroku main
```

### Docker
```bash
# Build image
docker build -t credit-score-api .

# Run container
docker run -p 5000:5000 --env-file .env credit-score-api
```

## 🔒 Security

- JWT token authentication
- Firebase integration for production
- Input validation and sanitization
- Error handling without data leakage
- Secure PDF generation
- CORS protection

## 📈 Scalability Features

- MongoDB for efficient data storage
- Stateless API design
- Service-oriented architecture
- Caching-ready structure
- Horizontal scaling support
- Environment-based configuration

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in `/docs`
- Review the API endpoint examples above
