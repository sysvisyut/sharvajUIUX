import requests
import json
from flask import current_app

class ChatService:
    """Service for handling chat with OpenRouter API"""
    
    @staticmethod
    def send_message(message, user_context=None, conversation_history=None):
        """Send message to OpenRouter API using configured model with conversation context"""
        try:
            api_key = current_app.config.get('OPENROUTER_API_KEY')
            model = current_app.config.get('OPEN_ROUTER_MODEL')
            base_url = current_app.config.get('OPENROUTER_BASE_URL')

            current_app.logger.info(f"Chat request - Model: {model}, API Key present: {bool(api_key)}")

            if not api_key:
                current_app.logger.warning("No OpenRouter API key configured, using fallback response")
                return ChatService._fallback_response(message)
            
            # Prepare the prompt with context
            system_prompt = ChatService._build_system_prompt(user_context)

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://realzilla-financial-advisor.com',
                'X-Title': 'RealZilla AI Financial Advisor'
            }

            # Build conversation messages with history
            messages = [{'role': 'system', 'content': system_prompt}]

            # Add recent conversation history (last 6 messages for context)
            if conversation_history:
                recent_history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
                for hist_msg in recent_history:
                    messages.append({'role': 'user', 'content': hist_msg.get('user_message', '')})
                    messages.append({'role': 'assistant', 'content': hist_msg.get('bot_response', '')})

            # Add current message
            messages.append({'role': 'user', 'content': message})

            data = {
                'model': model,
                'messages': messages,
                'max_tokens': 800,  # Increased for more detailed responses
                'temperature': 0.8,  # Slightly more creative
                'top_p': 0.95,      # Better response quality
                'frequency_penalty': 0.1,  # Reduce repetition
                'presence_penalty': 0.1    # Encourage diverse topics
            }
            
            current_app.logger.info(f"Sending request to OpenRouter API: {base_url}/chat/completions")

            response = requests.post(
                f'{base_url}/chat/completions',
                headers=headers,
                json=data,
                timeout=30
            )

            current_app.logger.info(f"OpenRouter API response status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content'].strip()
                current_app.logger.info(f"OpenRouter API success - Response length: {len(ai_response)}")
                return ai_response
            else:
                current_app.logger.error(f"OpenRouter API error: {response.status_code} - {response.text}")
                return ChatService._fallback_response(message)
                
        except Exception as e:
            current_app.logger.error(f"Chat service error: {str(e)}")
            return ChatService._fallback_response(message)
    
    @staticmethod
    def _build_system_prompt(user_context):
        """Build system prompt with user context"""
        base_prompt = '''You are an expert AI Financial Advisor with deep knowledge in personal finance, credit management, and wealth building. You communicate like a knowledgeable, friendly financial consultant who genuinely cares about helping people achieve financial success.

CORE EXPERTISE:
• Credit Score Optimization: Detailed strategies for improving FICO/VantageScore ratings
• Debt Management: Avalanche vs. snowball methods, consolidation strategies, negotiation tactics
• Budgeting & Cash Flow: 50/30/20 rule, zero-based budgeting, envelope method
• Investment Planning: Index funds, 401(k) optimization, Roth vs. Traditional IRA
• Loan Strategies: Mortgage qualification, refinancing, personal loans, auto loans
• Credit Cards: Rewards optimization, balance transfers, utilization strategies
• Emergency Planning: Building emergency funds, insurance needs, financial safety nets

COMMUNICATION STYLE:
• Conversational and engaging, like talking to a trusted financial advisor
• Provide specific, actionable steps with clear timelines
• Use real examples and numbers to illustrate points
• Break down complex financial concepts into simple terms
• Ask follow-up questions to provide personalized advice
• Show empathy for financial struggles and celebrate progress
• Be encouraging but realistic about timeframes for improvement

RESPONSE FORMAT:
• Start with a brief acknowledgment of their question/situation
• Provide 2-3 specific, actionable recommendations
• Include relevant examples or calculations when helpful
• End with a follow-up question or next step suggestion
• Keep responses conversational but informative (3-5 paragraphs)

IMPORTANT GUIDELINES:
• Always provide practical, implementable advice
• Mention when to consult certified financial professionals for complex situations
• Never guarantee specific outcomes or provide investment recommendations
• Emphasize that financial improvement requires consistency and patience'''

        if user_context:
            context_info = f'''\n\nUser Context:
- Current Credit Score: {user_context.get('credit_score', 'Not calculated')}
- Last Updated: {user_context.get('last_updated', 'N/A')}
- Loan Approval Status: {user_context.get('loan_approved', 'Unknown')}'''
            
            base_prompt += context_info
        
        return base_prompt
    
    @staticmethod
    def _fallback_response(message):
        """Provide fallback response when API is unavailable"""
        
        message_lower = message.lower()
        
        # Simple keyword-based responses
        if any(word in message_lower for word in ['credit score', 'score', 'rating']):
            return '''A credit score is a numerical representation of your creditworthiness, typically ranging from 300 to 850. It's calculated based on factors like payment history (35%), credit utilization (30%), length of credit history (15%), credit mix (10%), and new credit (10%).

To improve your credit score:
1. Pay all bills on time
2. Keep credit utilization below 30%
3. Don't close old credit cards
4. Limit new credit applications
5. Monitor your credit report regularly'''

        elif any(word in message_lower for word in ['improve', 'increase', 'better']):
            return '''Here are key ways to improve your credit score:

1. **Payment History** (35% impact): Never miss payments. Set up automatic payments for at least minimum amounts.

2. **Credit Utilization** (30% impact): Keep total credit card balances below 30% of limits, ideally under 10%.

3. **Credit Age** (15% impact): Keep old accounts open to maintain longer average account age.

4. **Credit Mix** (10% impact): Have a diverse mix of credit types (cards, auto loan, mortgage).

5. **New Credit** (10% impact): Limit hard inquiries by spacing out new credit applications.

Remember, improvements take time - typically 3-6 months to see significant changes.'''

        elif any(word in message_lower for word in ['loan', 'approval', 'qualify']):
            return '''Loan approval depends on several factors:

**Credit Score Requirements:**
- Excellent (750+): Best rates and terms
- Good (700-749): Competitive rates
- Fair (650-699): Standard rates, may need larger down payment
- Poor (below 650): Limited options, higher rates

**Other Factors:**
- Debt-to-income ratio (should be below 43% for most loans)
- Employment history and income stability
- Down payment amount
- Loan purpose and amount

**Tips to Improve Approval Chances:**
1. Improve your credit score before applying
2. Pay down existing debt
3. Save for a larger down payment
4. Get pre-qualified to understand your options
5. Consider a co-signer if needed'''

        else:
            return '''I'm here to help with credit score and financial questions! You can ask me about:

- Understanding your credit score
- Improving your credit rating
- Loan approval requirements
- Credit card management
- Debt reduction strategies
- Financial wellness tips

What specific aspect of credit or personal finance would you like to know more about?'''

    @staticmethod
    def get_suggested_questions():
        """Get list of suggested questions for the chat interface"""
        return [
            "How can I improve my credit score?",
            "What factors affect my credit score the most?",
            "How long does it take to improve credit?",
            "What credit score do I need for a mortgage?",
            "How does credit utilization affect my score?",
            "Should I close old credit cards?",
            "What's the difference between credit score ranges?",
            "How often should I check my credit report?",
            "What can I do about late payments?",
            "How do I build credit with no credit history?"
        ]
