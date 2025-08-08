import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence, useDragControls } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  X,
  Send,
  Bot,
  User,
  Minimize2,
  Maximize2,
  MessageCircle,
  Sparkles,
  TrendingUp,
  DollarSign,
  PieChart,
  Move
} from 'lucide-react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  typing?: boolean;
}

interface ChatBotOverlayProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatBotOverlay: React.FC<ChatBotOverlayProps> = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: "👋 Welcome! I'm your AI Financial Advisor, and I'm here to help you take control of your financial future! Whether you want to boost your credit score, crush debt, build savings, or start investing - I've got proven strategies that work. What financial goal can we tackle together today? 🚀",
      sender: 'bot',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isMinimized, setIsMinimized] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const dragControls = useDragControls();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (isOpen && !isMinimized) {
      inputRef.current?.focus();
    }
  }, [isOpen, isMinimized]);

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputValue;
    setInputValue('');
    setIsTyping(true);

    try {
      // Try to call the backend API
      const response = await fetch('/api/chat/send', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: currentInput,
          context: {
            page: 'financial_advisor',
            user_type: 'guest'
          }
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botResponse: Message = {
          id: (Date.now() + 1).toString(),
          text: data.data.response,
          sender: 'bot',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, botResponse]);
      } else {
        throw new Error('API call failed');
      }
    } catch (error) {
      // Fallback to local responses if API fails
      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: generateBotResponse(currentInput),
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botResponse]);
    } finally {
      setIsTyping(false);
    }
  };

  const generateBotResponse = (userInput: string): string => {
    const input = userInput.toLowerCase();

    if (input.includes('credit score') || input.includes('score')) {
      return "Your credit score is influenced by five key factors: Payment History (35%) - the most important factor, Credit Utilization (30%) - keep below 30%, Length of Credit History (15%), Credit Mix (10%), and New Credit (10%). Based on your current profile, I can provide personalized recommendations. What's your current credit situation?";
    } else if (input.includes('improve') || input.includes('better') || input.includes('increase')) {
      return "Excellent! Here's my proven strategy for improving your financial health: 1) Set up automatic payments to never miss due dates, 2) Pay down credit card balances to below 30% utilization, 3) Keep old accounts open to maintain credit history length, 4) Check your credit report monthly for errors, 5) Consider becoming an authorized user on a family member's account. Which area needs the most attention right now?";
    } else if (input.includes('debt') || input.includes('payment') || input.includes('owe')) {
      return "Smart debt management is key to financial freedom! I recommend two proven strategies: Debt Avalanche (pay minimums on all debts, extra on highest interest rate) saves more money long-term, or Debt Snowball (pay minimums on all debts, extra on smallest balance) provides psychological wins. What's your total debt amount and highest interest rate?";
    } else if (input.includes('budget') || input.includes('money') || input.includes('spend')) {
      return "Let's build you a winning budget! I recommend the 50/30/20 rule as a starting point: 50% for needs (rent, utilities, groceries), 30% for wants (entertainment, dining out), and 20% for savings and debt repayment. But we can customize this based on your income and goals. What's your monthly take-home income?";
    } else if (input.includes('save') || input.includes('saving') || input.includes('emergency')) {
      return "Building savings is crucial for financial security! Start with a $1,000 emergency fund, then work toward 3-6 months of expenses. I recommend high-yield savings accounts (currently 4-5% APY) and automating transfers. Even $25/week adds up to $1,300/year! What's your current savings goal?";
    } else if (input.includes('invest') || input.includes('retirement') || input.includes('401k')) {
      return "Investing is how you build long-term wealth! Start with your employer's 401(k) match (free money!), then consider low-cost index funds. The key is time in the market, not timing the market. Even $100/month invested with 7% returns becomes $87,000 in 20 years! Are you currently contributing to retirement?";
    } else if (input.includes('utilization') || input.includes('credit card')) {
      return "Credit utilization is super important! Keep total utilization below 30%, but ideally under 10% for the best scores. Pay balances before statement dates, or make multiple payments per month. If you have a $1,000 limit, keep balances under $100. Need help calculating your current utilization ratio?";
    } else if (input.includes('hello') || input.includes('hi') || input.includes('hey')) {
      return "Hello! I'm your AI Financial Advisor, and I'm excited to help you achieve your financial goals! I specialize in credit improvement, debt management, budgeting, and building wealth. Whether you want to boost your credit score, pay off debt faster, or start investing, I'm here to guide you. What financial challenge can I help you tackle today?";
    } else {
      return "I'm here to help with all aspects of your financial journey! I can assist with: 📊 Credit score improvement, 💳 Debt payoff strategies, 💰 Budget planning, 🏦 Savings goals, 📈 Investment basics, 🏠 Home buying preparation, and much more. What specific financial topic would you like to explore together?";
    }
  };

  const quickSuggestions = [
    "How can I boost my credit score by 100 points?",
    "What's the fastest way to pay off debt?",
    "Help me build an emergency fund",
    "Should I invest or pay off debt first?",
    "How do I create a realistic budget?",
    "What credit cards should I get?"
  ];

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-[100] pointer-events-none"
      >
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 bg-black/20 backdrop-blur-sm pointer-events-auto"
          onClick={onClose}
        />

        {/* Chat Window */}
        <motion.div
          drag
          dragMomentum={false}
          dragElastic={0.1}
          dragListener={false}
          dragControls={dragControls}
          dragConstraints={{
            top: -50,
            left: -200,
            right: typeof window !== 'undefined' ? window.innerWidth - 200 : 800,
            bottom: typeof window !== 'undefined' ? window.innerHeight - 100 : 600
          }}
          initial={{
            scale: 0.8,
            opacity: 0,
            x: typeof window !== 'undefined' ? window.innerWidth - 460 : 350,
            y: typeof window !== 'undefined' ? window.innerHeight - 690 : 50
          }}
          animate={{
            scale: isDragging ? 1.02 : 1,
            opacity: 1,
            height: isMinimized ? 'auto' : '480px',
            boxShadow: isDragging
              ? "0 20px 60px rgba(0, 0, 0, 0.4), 0 0 40px rgba(59, 130, 246, 0.3)"
              : "0 10px 30px rgba(0, 0, 0, 0.2)"
          }}
          exit={{ scale: 0.8, opacity: 0, y: 100 }}
          transition={{ type: 'spring', damping: 25, stiffness: 300 }}
          className="absolute w-full max-w-md pointer-events-auto select-none"
          onDragStart={() => setIsDragging(true)}
          onDragEnd={() => setIsDragging(false)}
          style={{
            zIndex: isDragging ? 110 : 100
          }}
        >
          <Card className="glass-effect border-white/20 overflow-hidden shadow-2xl">
            {/* Header - Drag Handle */}
            <motion.div
              className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 text-white relative cursor-grab active:cursor-grabbing"
              whileHover={{ backgroundColor: isDragging ? undefined : "rgba(59, 130, 246, 0.9)" }}
              onPointerDown={(e) => dragControls.start(e)}
            >
              {/* Drag Handle Indicator */}
              <div className="absolute top-2 left-1/2 transform -translate-x-1/2">
                <motion.div
                  className="w-8 h-1 bg-white/30 rounded-full"
                  animate={{
                    width: isDragging ? "12px" : "32px",
                    opacity: isDragging ? 0.8 : 0.3
                  }}
                />
              </div>

              <div className="flex items-center justify-between mt-2">
                <div className="flex items-center space-x-3">
                  <motion.div
                    animate={{ rotate: [0, 360] }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                    className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center"
                  >
                    <Sparkles className="w-5 h-5" />
                  </motion.div>
                  <div>
                    <h3 className="font-bold text-lg">AI Financial Advisor</h3>
                    <p className="text-blue-100 text-sm flex items-center gap-1">
                      <Move className="w-3 h-3" />
                      {isDragging ? "Moving..." : "Drag to move • Always here to help"}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      setIsMinimized(!isMinimized);
                    }}
                    className="text-white hover:bg-white/20 p-1 pointer-events-auto"
                    onPointerDown={(e) => e.stopPropagation()}
                  >
                    {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      onClose();
                    }}
                    className="text-white hover:bg-white/20 p-1 pointer-events-auto"
                    onPointerDown={(e) => e.stopPropagation()}
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </motion.div>

            {!isMinimized && (
              <>
                {/* Messages */}
                <div className="h-72 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-slate-50/50 to-white/50">
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`flex items-start space-x-2 max-w-[80%] ${
                        message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                      }`}>
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                          message.sender === 'user' 
                            ? 'bg-blue-500' 
                            : 'bg-gradient-to-r from-purple-500 to-pink-500'
                        }`}>
                          {message.sender === 'user' ? (
                            <User className="w-4 h-4 text-white" />
                          ) : (
                            <Bot className="w-4 h-4 text-white" />
                          )}
                        </div>
                        <div className={`rounded-2xl px-4 py-2 ${
                          message.sender === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-white border border-gray-200 text-gray-800'
                        }`}>
                          <p className="text-sm">{message.text}</p>
                          <p className={`text-xs mt-1 ${
                            message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                          }`}>
                            {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                  
                  {isTyping && (
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex justify-start"
                    >
                      <div className="flex items-start space-x-2">
                        <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 flex items-center justify-center">
                          <Bot className="w-4 h-4 text-white" />
                        </div>
                        <div className="bg-white border border-gray-200 rounded-2xl px-4 py-2">
                          <div className="flex space-x-1">
                            <motion.div
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 1, repeat: Infinity, delay: 0 }}
                              className="w-2 h-2 bg-gray-400 rounded-full"
                            />
                            <motion.div
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 1, repeat: Infinity, delay: 0.2 }}
                              className="w-2 h-2 bg-gray-400 rounded-full"
                            />
                            <motion.div
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 1, repeat: Infinity, delay: 0.4 }}
                              className="w-2 h-2 bg-gray-400 rounded-full"
                            />
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  )}
                  <div ref={messagesEndRef} />
                </div>

                {/* Quick Suggestions */}
                {messages.length === 1 && (
                  <div className="px-4 py-2 border-t border-gray-200">
                    <p className="text-xs text-gray-500 mb-2">Quick suggestions:</p>
                    <div className="flex flex-wrap gap-2">
                      {quickSuggestions.map((suggestion, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => setInputValue(suggestion)}
                          className="text-xs h-7 px-2 border-blue-200 text-blue-600 hover:bg-blue-50"
                        >
                          {suggestion}
                        </Button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Input */}
                <div className="p-4 border-t border-gray-200 bg-white">
                  <div className="flex space-x-2">
                    <Input
                      ref={inputRef}
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                      placeholder="Ask me about your finances..."
                      className="flex-1 border-gray-300 focus:border-blue-500"
                      disabled={isTyping}
                    />
                    <Button
                      onClick={handleSendMessage}
                      disabled={!inputValue.trim() || isTyping}
                      className="bg-blue-500 hover:bg-blue-600 text-white px-3"
                    >
                      <Send className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </>
            )}
          </Card>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
};

export default ChatBotOverlay;
