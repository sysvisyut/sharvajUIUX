# OpenRouter Integration Setup Guide

This guide explains how to set up the OpenRouter API integration for the AI Financial Advisor chatbot.

## 🔑 Environment Variables Required

Add these environment variables to your `.env` file or system environment:

```bash
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPEN_ROUTER_MODEL=meta-llama/llama-3.3-70b-instruct:free
```

## 📝 Getting Your OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for an account or log in
3. Go to your API Keys section
4. Generate a new API key
5. Copy the API key to your `.env` file

## 🤖 Available Models

You can use any model available on OpenRouter. Some popular options:

### Free Models
- `meta-llama/llama-3.3-70b-instruct:free` (Default)
- `microsoft/phi-3-mini-128k-instruct:free`
- `google/gemma-2-9b-it:free`

### Paid Models (Better Performance)
- `anthropic/claude-3.5-sonnet`
- `openai/gpt-4o`
- `meta-llama/llama-3.1-405b-instruct`

## 🧪 Testing the Integration

Run the test script to verify everything is working:

```bash
cd sharvajUIUX/Backend
python test_openrouter.py
```

This will test:
1. Direct OpenRouter API connection
2. Flask app chat endpoint integration

## 🚀 Starting the Application

1. Make sure your environment variables are set
2. Start the Flask backend:
   ```bash
   cd sharvajUIUX/Backend
   python run.py
   ```
3. Start the React frontend:
   ```bash
   cd sharvajUIUX/Frontend
   npm run dev
   ```

## 🔧 Configuration Details

The integration uses these configuration settings:

- **API Base URL**: `https://openrouter.ai/api/v1`
- **Endpoint**: `/chat/completions`
- **Max Tokens**: 500
- **Temperature**: 0.7
- **Top P**: 0.9

## 🛠️ Troubleshooting

### Common Issues

1. **"No OpenRouter API key configured"**
   - Check that `OPENROUTER_API_KEY` is set in your environment
   - Verify the API key is valid and active

2. **"API call failed"**
   - Check your internet connection
   - Verify the model name is correct
   - Check OpenRouter service status

3. **"Insufficient credits"**
   - Add credits to your OpenRouter account
   - Switch to a free model for testing

### Fallback Behavior

If the OpenRouter API is unavailable, the system will automatically fall back to local responses with pre-programmed financial advice. This ensures the chatbot always works, even without API access.

## 📊 Monitoring

The application logs all OpenRouter API interactions:
- Request details (model, API key presence)
- Response status codes
- Error messages
- Response lengths

Check the Flask application logs for debugging information.

## 💰 Cost Management

- Free models have usage limits but no cost
- Paid models charge per token (input + output)
- Monitor your usage on the OpenRouter dashboard
- Set up billing alerts to avoid unexpected charges

## 🔒 Security Notes

- Never commit your API key to version control
- Use environment variables or secure secret management
- Rotate your API keys regularly
- Monitor API usage for unusual activity
