import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import FloatingChatButton from '@/components/FloatingChatButton';
import {
  Download,
  TrendingUp,
  TrendingDown,
  Calendar,
  Award,
  AlertCircle,
  CheckCircle,
  Info,
  Clock,
  Star,
  Target,
  Shield
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import CreditScoreCalculator from '@/components/CreditScoreCalculator';
import Navigation from '@/components/Navigation';
import OrbBackground from '@/components/ui/OrbBackground';

const Dashboard = () => {
  // Mock data - in real app this would come from API
  const creditScore = 712;
  const scoreDate = "December 15, 2024";
  
  const scoreFactors = [
    { factor: "Rent Payment Consistency", impact: "positive", description: "12 months of on-time payments" },
    { factor: "Utility Payment History", impact: "positive", description: "Consistent electricity & water payments" },
    { factor: "Income Stability", impact: "neutral", description: "Steady income for 8 months" },
    { factor: "Credit Utilization", impact: "negative", description: "High usage on existing accounts" }
  ];

  const scoreHistory = [
    { date: "Oct 2024", score: 678 },
    { date: "Nov 2024", score: 695 },
    { date: "Dec 2024", score: 712 }
  ];

  const badges = [
    { name: "Rent Rockstar", description: "12 consecutive on-time rent payments", earnedAt: "Dec 10, 2024", icon: "🏠" },
    { name: "Utility Champion", description: "Perfect utility payment record", earnedAt: "Dec 5, 2024", icon: "⚡" },
    { name: "Score Climber", description: "Improved score by 30+ points", earnedAt: "Nov 28, 2024", icon: "📈" }
  ];

  const insights = [
    { 
      type: "positive", 
      title: "Score Improvement", 
      message: "Your score increased by 17 points this month thanks to consistent rent payments!" 
    },
    { 
      type: "tip", 
      title: "Boost Your Score", 
      message: "Adding your streaming subscriptions could increase your score by 15-25 points." 
    },
    { 
      type: "warning", 
      title: "Missing Data", 
      message: "Complete your profile to unlock your full credit potential." 
    }
  ];

  const recentActivity = [
    { type: "score", message: "Credit score calculated: 712", timestamp: "2 hours ago" },
    { type: "badge", message: "Earned 'Rent Rockstar' badge", timestamp: "5 days ago" },
    { type: "score", message: "Credit score calculated: 695", timestamp: "1 month ago" }
  ];

  const missingFields = ["Bank Account Verification", "Employment History", "Streaming Subscriptions"];

  return (
    <div className="min-h-screen relative overflow-y-auto">
      <OrbBackground />
      
      <Navigation />
      
      <div className="pt-20 px-4 pb-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="flex justify-between items-center mb-4"
          >
            <div>
              <h1 
                className="text-3xl font-cred-heading font-bold text-white mb-2"
                style={{ textShadow: '2px 2px 12px rgba(0, 0, 0, 0.8)' }}
              >
                Your Credit Dashboard
              </h1>
              <p 
                className="text-white/80 font-cred-body text-base"
                style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.6)' }}
              >
                Track your alternative credit journey
              </p>
            </div>
            
            <motion.div
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Button 
                className="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white font-cred-body font-semibold px-6 py-3 shadow-lg"
              >
                <Download className="w-4 h-4 mr-2" />
                Download Report
              </Button>
            </motion.div>
          </motion.div>

          {/* Main Grid - No scroll, everything fits */}
          <div className="grid lg:grid-cols-4 gap-4 h-[calc(100vh-140px)]">
            {/* Left Column - Main Content */}
            <div className="lg:col-span-3 space-y-4">
              
              {/* Combined Credit Score, Line Graph & Insights */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 }}
                className="h-full"
              >
                <Card className="glass-effect p-4 border-white/10 glow-effect h-full">
                  <div className="flex items-center justify-between mb-3">
                    <h2 
                      className="text-xl font-cred-heading font-bold text-white"
                      style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                    >
                      Credit Dashboard Overview
                    </h2>
                    <span 
                      className="text-white/60 font-cred-body text-sm"
                      style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                    >
                      Updated {scoreDate}
                    </span>
                  </div>
                  
                  {/* Top Section - Credit Score centered */}
                  <div className="flex flex-col items-center justify-center mb-6">
                    <CreditScoreCalculator targetScore={creditScore} className="scale-75" />
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ duration: 0.6, delay: 0.8 }}
                      className="mt-4 text-center"
                    >
                      <div className="flex items-center justify-center gap-2 mb-2">
                        <span
                          className="text-2xl font-cred-heading font-bold text-white"
                          style={{ textShadow: '2px 2px 8px rgba(0, 0, 0, 0.8)' }}
                        >
                          {creditScore}
                        </span>
                        <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-400/30">
                          Good
                        </Badge>
                      </div>
                      <p
                        className="text-white/70 font-cred-body text-sm"
                        style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                      >
                        Alternative Credit Score
                      </p>
                    </motion.div>
                  </div>

                  {/* Score Trend Section - Full width under the score */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-cred-heading font-bold text-white">
                        📈 Score Trend
                      </h3>
                      <div className="flex items-center gap-2">
                        <TrendingUp className="w-4 h-4 text-emerald-400" />
                        <span className="text-emerald-400 font-cred-body text-sm font-semibold">
                          +34 points
                        </span>
                      </div>
                    </div>
                    <div className="bg-black/30 rounded-lg p-4 h-48">
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={scoreHistory}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.15)" />
                          <XAxis 
                            dataKey="date" 
                            stroke="rgba(255,255,255,0.7)"
                            fontSize={12}
                            fontFamily="var(--font-cred-body)"
                          />
                          <YAxis 
                            stroke="rgba(255,255,255,0.7)"
                            fontSize={12}
                            fontFamily="var(--font-cred-body)"
                            domain={['dataMin - 20', 'dataMax + 20']}
                            width={40}
                          />
                          <Tooltip 
                            contentStyle={{
                              backgroundColor: 'rgba(0, 0, 0, 0.8)',
                              border: '1px solid rgba(255, 255, 255, 0.2)',
                              borderRadius: '8px',
                              backdropFilter: 'blur(15px)',
                              color: 'white',
                              fontSize: '12px'
                            }}
                            labelStyle={{ color: 'white', fontSize: '11px' }}
                          />
                          <Line 
                            type="monotone" 
                            dataKey="score" 
                            stroke="url(#scoreGradient)" 
                            strokeWidth={3}
                            dot={{ 
                              fill: '#10b981', 
                              strokeWidth: 2, 
                              r: 5,
                              stroke: '#065f46'
                            }}
                            activeDot={{ 
                              r: 8, 
                              fill: '#06d6a0',
                              stroke: '#065f46',
                              strokeWidth: 3
                            }}
                          />
                          <defs>
                            <linearGradient id="scoreGradient" x1="0" y1="0" x2="1" y2="0">
                              <stop offset="0%" stopColor="#10b981" />
                              <stop offset="50%" stopColor="#06d6a0" />
                              <stop offset="100%" stopColor="#22d3ee" />
                            </linearGradient>
                          </defs>
                        </LineChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                </Card>
              </motion.div>
            </div>

            {/* Right Sidebar - Condensed */}
            <div className="lg:col-span-1 space-y-4">
              
              {/* Gamification Badges - Compact */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Card className="glass-effect p-4 border-white/10">
                  <h3 
                    className="text-base font-cred-heading font-bold text-white mb-3"
                    style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                  >
                    🏅 Badges
                  </h3>
                  <div className="space-y-2">
                    {badges.slice(0, 2).map((badge, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
                        whileHover={{ scale: 1.02 }}
                        className="flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-purple-500/10 via-pink-500/5 to-purple-500/10 border border-purple-400/20 cursor-pointer"
                      >
                        <motion.div
                          animate={{ rotate: [0, 10, -10, 0] }}
                          transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
                          className="text-lg"
                        >
                          {badge.icon}
                        </motion.div>
                        <div className="flex-1 min-w-0">
                          <p
                            className="text-white font-cred-body font-medium text-xs truncate"
                            style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                          >
                            {badge.name}
                          </p>
                          <p
                            className="text-purple-300 font-cred-body text-xs"
                            style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                          >
                            +{5 + index * 2} pts
                          </p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </Card>
              </motion.div>

              {/* Recent Activity - Compact */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <Card className="glass-effect p-4 border-white/10">
                  <h3 
                    className="text-base font-cred-heading font-bold text-white mb-3"
                    style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                  >
                    🕒 Activity
                  </h3>
                  <div className="space-y-2">
                    {recentActivity.slice(0, 4).map((activity, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: 0.4 + index * 0.1 }}
                        className="flex items-start gap-2 p-2 rounded-lg bg-black/20 border border-white/5"
                      >
                        {activity.type === 'score' ? (
                          <TrendingUp className="w-3 h-3 text-emerald-400 mt-0.5 flex-shrink-0" />
                        ) : (
                          <Award className="w-3 h-3 text-purple-400 mt-0.5 flex-shrink-0" />
                        )}
                        <div className="flex-1 min-w-0">
                          <p 
                            className="text-white font-cred-body text-xs leading-tight"
                            style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                          >
                            {activity.message}
                          </p>
                          <p 
                            className="text-white/60 font-cred-body text-xs mt-1"
                            style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                          >
                            {activity.timestamp}
                          </p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </Card>
              </motion.div>

              {/* Key Insights - Moved to Right Panel */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.35 }}
              >
                <Card className="glass-effect p-4 border-white/10">
                  <h3 
                    className="text-base font-cred-heading font-bold text-white mb-3"
                    style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                  >
                    💡 Key Insights
                  </h3>
                  <div className="space-y-3">
                    {insights.slice(0, 2).map((insight, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: 0.4 + index * 0.1 }}
                        whileHover={{ scale: 1.02 }}
                        className={`p-3 rounded-lg border cursor-pointer transition-all duration-300 ${
                          insight.type === 'positive'
                            ? 'bg-emerald-500/10 border-emerald-400/30 hover:border-emerald-400/50'
                            : insight.type === 'warning'
                            ? 'bg-orange-500/10 border-orange-400/30 hover:border-orange-400/50'
                            : 'bg-blue-500/10 border-blue-400/30 hover:border-blue-400/50'
                        }`}
                      >
                        <div className="flex items-start gap-2">
                          {insight.type === 'positive' ? (
                            <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                          ) : insight.type === 'warning' ? (
                            <AlertCircle className="w-4 h-4 text-orange-400 flex-shrink-0 mt-0.5" />
                          ) : (
                            <Info className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                          )}
                          <div className="flex-1">
                            <h4 className="text-white font-cred-body font-semibold text-xs mb-1">
                              {insight.title}
                            </h4>
                            <p className="text-white/80 font-cred-body text-xs leading-relaxed">
                              {insight.message}
                            </p>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </Card>
              </motion.div>
            </div>
          </div>
        </div>
      </div>

      {/* Floating Chat Button */}
      <FloatingChatButton />
    </div>
  );
};

export default Dashboard;
