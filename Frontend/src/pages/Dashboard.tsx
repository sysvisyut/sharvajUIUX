import React from 'react';
import { motion } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
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
  Shield,
  Zap
} from 'lucide-react';
import CreditScoreCalculator from '@/components/CreditScoreCalculator';
import Navigation from '@/components/Navigation';
import OrbBackground from '@/components/ui/OrbBackground';

const Dashboard = () => {
  // Mock data - in real app this would come from API
  const creditScore = 712;
  const scoreDate = "December 15, 2024";
  const dataCompleteness = 85;
  
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
    <div className="min-h-screen relative">
      <OrbBackground />
      <div className="fixed inset-0 bg-gradient-to-br from-black/20 via-transparent to-black/30 pointer-events-none -z-5"></div>
      
      <Navigation />
      
      <div className="pt-24 px-6 pb-12">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="flex justify-between items-center mb-8"
          >
            <div>
              <h1 
                className="text-4xl font-cred-heading font-bold text-white mb-2"
                style={{ textShadow: '2px 2px 12px rgba(0, 0, 0, 0.8)' }}
              >
                Your Credit Dashboard
              </h1>
              <p 
                className="text-white/80 font-cred-body text-lg"
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

          {/* Main Grid */}
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Left Column - Main Content */}
            <div className="lg:col-span-2 space-y-8">
              
              {/* Credit Score Summary */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.1 }}
              >
                <Card className="glass-effect p-8 border-white/10 glow-effect">
                  <div className="flex items-center justify-between mb-6">
                    <h2 
                      className="text-2xl font-cred-heading font-bold text-white"
                      style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                    >
                      Latest Credit Score
                    </h2>
                    <span 
                      className="text-white/60 font-cred-body text-sm"
                      style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                    >
                      Updated {scoreDate}
                    </span>
                  </div>
                  
                  <div className="grid md:grid-cols-2 gap-8 items-center">
                    <div className="flex flex-col items-center">
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

                    <div className="space-y-4">
                      <div className="flex items-center justify-between mb-4">
                        <h3
                          className="text-lg font-cred-heading font-semibold text-white"
                          style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.8)' }}
                        >
                          Score Factors
                        </h3>
                        <motion.div
                          animate={{ rotate: [0, 10, -10, 0] }}
                          transition={{ duration: 2, repeat: Infinity, repeatDelay: 3 }}
                        >
                          <Target className="w-5 h-5 text-cyan-400" />
                        </motion.div>
                      </div>
                      {scoreFactors.map((factor, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ duration: 0.4, delay: 0.2 + index * 0.1 }}
                          whileHover={{ scale: 1.02, x: 5 }}
                          className={`flex items-start gap-3 p-4 rounded-lg border transition-all duration-300 cursor-pointer ${
                            factor.impact === 'positive'
                              ? 'bg-emerald-500/10 border-emerald-400/30 hover:bg-emerald-500/20'
                              : factor.impact === 'negative'
                              ? 'bg-red-500/10 border-red-400/30 hover:bg-red-500/20'
                              : 'bg-blue-500/10 border-blue-400/30 hover:bg-blue-500/20'
                          }`}
                        >
                          {factor.impact === 'positive' ? (
                            <motion.div
                              animate={{ scale: [1, 1.2, 1] }}
                              transition={{ duration: 2, repeat: Infinity, repeatDelay: 2 }}
                            >
                              <CheckCircle className="w-5 h-5 text-emerald-400 mt-0.5 flex-shrink-0" />
                            </motion.div>
                          ) : factor.impact === 'negative' ? (
                            <AlertCircle className="w-5 h-5 text-red-400 mt-0.5 flex-shrink-0" />
                          ) : (
                            <Info className="w-5 h-5 text-blue-400 mt-0.5 flex-shrink-0" />
                          )}
                          <div className="flex-1">
                            <p
                              className="text-white font-cred-body font-medium text-sm"
                              style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                            >
                              {factor.factor}
                            </p>
                            <p
                              className="text-white/70 font-cred-body text-xs mt-1"
                              style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                            >
                              {factor.description}
                            </p>
                          </div>
                          {factor.impact === 'positive' && (
                            <motion.div
                              initial={{ opacity: 0 }}
                              animate={{ opacity: 1 }}
                              transition={{ delay: 0.5 + index * 0.1 }}
                            >
                              <span className="text-emerald-400 text-xs font-semibold">+15</span>
                            </motion.div>
                          )}
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </Card>
              </motion.div>

              {/* Score Trend Chart */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Card className="glass-effect p-6 border-white/10 glow-effect">
                  <div className="flex items-center justify-between mb-6">
                    <h3
                      className="text-xl font-cred-heading font-bold text-white"
                      style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                    >
                      📈 Score Trend
                    </h3>
                    <div className="flex items-center gap-2">
                      <TrendingUp className="w-4 h-4 text-emerald-400" />
                      <span
                        className="text-emerald-400 font-cred-body text-sm font-semibold"
                        style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                      >
                        +34 points
                      </span>
                    </div>
                  </div>
                  <div className="flex items-end justify-between h-40 gap-6 mb-4">
                    {scoreHistory.map((item, index) => (
                      <motion.div
                        key={index}
                        className="flex-1 flex flex-col items-center"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ duration: 0.6, delay: 0.3 + index * 0.2 }}
                      >
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: `${(item.score / 850) * 120}px` }}
                          transition={{ duration: 1, delay: 0.5 + index * 0.2, ease: "easeOut" }}
                          className="w-full bg-gradient-to-t from-emerald-500 via-emerald-400 to-cyan-400 rounded-t-lg relative min-h-[30px] flex items-end justify-center shadow-lg"
                          style={{
                            boxShadow: '0 0 20px rgba(16, 185, 129, 0.3)'
                          }}
                        >
                          <motion.span
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 0.4, delay: 1 + index * 0.2 }}
                            className="text-white font-cred-body font-bold text-sm mb-2 bg-black/30 px-2 py-1 rounded backdrop-blur-sm"
                            style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.8)' }}
                          >
                            {item.score}
                          </motion.span>
                        </motion.div>
                        <span
                          className="text-white/60 font-cred-body text-xs text-center mt-3"
                          style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                        >
                          {item.date}
                        </span>
                      </motion.div>
                    ))}
                  </div>

                  {/* Trend Line Visualization */}
                  <div className="relative h-2 bg-black/20 rounded-full overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: "100%" }}
                      transition={{ duration: 2, delay: 1.5 }}
                      className="h-full bg-gradient-to-r from-emerald-500 to-cyan-400 rounded-full"
                      style={{
                        boxShadow: '0 0 10px rgba(16, 185, 129, 0.5)'
                      }}
                    />
                  </div>

                  <div className="flex justify-between items-center mt-4 text-xs">
                    <span
                      className="text-white/60 font-cred-body"
                      style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                    >
                      3-month progress
                    </span>
                    <span
                      className="text-emerald-400 font-cred-body font-semibold"
                      style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                    >
                      Excellent improvement!
                    </span>
                  </div>
                </Card>
              </motion.div>

              {/* Personalized Insights */}
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <Card className="glass-effect p-6 border-white/10">
                  <h3 
                    className="text-xl font-cred-heading font-bold text-white mb-6"
                    style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                  >
                    💡 Personalized Insights
                  </h3>
                  <div className="space-y-4">
                    {insights.map((insight, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20, rotateX: -90 }}
                        animate={{ opacity: 1, x: 0, rotateX: 0 }}
                        transition={{
                          duration: 0.6,
                          delay: 0.4 + index * 0.15,
                          type: "spring",
                          stiffness: 100
                        }}
                        whileHover={{
                          scale: 1.02,
                          y: -2,
                          boxShadow: insight.type === 'positive'
                            ? "0 10px 30px rgba(16, 185, 129, 0.2)"
                            : insight.type === 'warning'
                            ? "0 10px 30px rgba(251, 146, 60, 0.2)"
                            : "0 10px 30px rgba(59, 130, 246, 0.2)"
                        }}
                        className={`p-5 rounded-xl border cursor-pointer transition-all duration-300 ${
                          insight.type === 'positive'
                            ? 'bg-emerald-500/15 border-emerald-400/40 hover:border-emerald-400/60'
                            : insight.type === 'warning'
                            ? 'bg-orange-500/15 border-orange-400/40 hover:border-orange-400/60'
                            : 'bg-blue-500/15 border-blue-400/40 hover:border-blue-400/60'
                        }`}
                        style={{
                          backdropFilter: 'blur(10px)'
                        }}
                      >
                        <div className="flex items-start gap-3">
                          <motion.div
                            animate={{
                              rotate: insight.type === 'positive' ? [0, 360] : [0, 10, -10, 0],
                              scale: [1, 1.1, 1]
                            }}
                            transition={{
                              duration: insight.type === 'positive' ? 3 : 2,
                              repeat: Infinity,
                              repeatDelay: 3 + index
                            }}
                          >
                            {insight.type === 'positive' ? (
                              <CheckCircle className="w-6 h-6 text-emerald-400 flex-shrink-0" />
                            ) : insight.type === 'warning' ? (
                              <AlertCircle className="w-6 h-6 text-orange-400 flex-shrink-0" />
                            ) : (
                              <Zap className="w-6 h-6 text-blue-400 flex-shrink-0" />
                            )}
                          </motion.div>
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h4
                                className="text-white font-cred-body font-bold text-sm"
                                style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                              >
                                {insight.title}
                              </h4>
                              {insight.type === 'positive' && (
                                <motion.div
                                  initial={{ scale: 0, rotate: -180 }}
                                  animate={{ scale: 1, rotate: 0 }}
                                  transition={{ delay: 0.8 + index * 0.2, type: "spring" }}
                                >
                                  <Badge className="bg-emerald-500/20 text-emerald-300 border-emerald-400/30 text-xs">
                                    +17 pts
                                  </Badge>
                                </motion.div>
                              )}
                            </div>
                            <p
                              className="text-white/85 font-cred-body text-sm leading-relaxed"
                              style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                            >
                              {insight.message}
                            </p>
                            {insight.type === 'tip' && (
                              <motion.div
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: 1 + index * 0.2 }}
                                className="mt-3"
                              >
                                <Button
                                  size="sm"
                                  className="bg-blue-500/20 hover:bg-blue-500/30 text-blue-300 border border-blue-400/30 text-xs"
                                >
                                  Take Action
                                </Button>
                              </motion.div>
                            )}
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </Card>
              </motion.div>
            </div>

            {/* Right Column - Sidebar */}
            <div className="space-y-6">
              
              {/* Data Completeness */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.2 }}
              >
                <Card className="glass-effect p-6 border-white/10">
                  <h3 
                    className="text-lg font-cred-heading font-bold text-white mb-4"
                    style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                  >
                    📊 Profile Completeness
                  </h3>
                  <div className="text-center mb-4">
                    <div className="relative w-24 h-24 mx-auto mb-4">
                      <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 100 100">
                        <circle
                          cx="50"
                          cy="50"
                          r="40"
                          fill="none"
                          stroke="#1a1a1a"
                          strokeWidth="8"
                        />
                        <motion.circle
                          cx="50"
                          cy="50"
                          r="40"
                          fill="none"
                          stroke="url(#completeness-gradient)"
                          strokeWidth="8"
                          strokeLinecap="round"
                          strokeDasharray={`${2 * Math.PI * 40}`}
                          initial={{ strokeDashoffset: 2 * Math.PI * 40 }}
                          animate={{ strokeDashoffset: 2 * Math.PI * 40 * (1 - dataCompleteness / 100) }}
                          transition={{ duration: 1, delay: 0.5 }}
                        />
                        <defs>
                          <linearGradient id="completeness-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#10B981" />
                            <stop offset="100%" stopColor="#06D6A0" />
                          </linearGradient>
                        </defs>
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span 
                          className="text-2xl font-cred-heading font-bold text-white"
                          style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.8)' }}
                        >
                          {dataCompleteness}%
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="space-y-2">
                    <p 
                      className="text-white/80 font-cred-body text-sm mb-3"
                      style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                    >
                      Missing fields:
                    </p>
                    {missingFields.map((field, index) => (
                      <div key={index} className="flex items-center gap-2 text-orange-400 font-cred-body text-xs">
                        <AlertCircle className="w-3 h-3" />
                        <span>{field}</span>
                      </div>
                    ))}
                  </div>
                </Card>
              </motion.div>

              {/* Gamification Badges */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.3 }}
              >
                <Card className="glass-effect p-6 border-white/10">
                  <h3 
                    className="text-lg font-cred-heading font-bold text-white mb-4"
                    style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                  >
                    🏅 Your Badges
                  </h3>
                  <div className="space-y-3">
                    {badges.map((badge, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, scale: 0.8, rotateY: -90 }}
                        animate={{ opacity: 1, scale: 1, rotateY: 0 }}
                        transition={{
                          duration: 0.6,
                          delay: 0.4 + index * 0.2,
                          type: "spring",
                          stiffness: 100
                        }}
                        whileHover={{
                          scale: 1.05,
                          rotateY: 5,
                          boxShadow: "0 10px 30px rgba(168, 85, 247, 0.3)"
                        }}
                        className="flex items-center gap-4 p-4 rounded-xl bg-gradient-to-r from-purple-500/15 via-pink-500/10 to-purple-500/15 border border-purple-400/30 cursor-pointer transition-all duration-300 hover:border-purple-400/50"
                        style={{
                          backdropFilter: 'blur(10px)',
                          boxShadow: '0 4px 20px rgba(168, 85, 247, 0.1)'
                        }}
                      >
                        <motion.div
                          animate={{
                            rotate: [0, 10, -10, 0],
                            scale: [1, 1.1, 1]
                          }}
                          transition={{
                            duration: 3,
                            repeat: Infinity,
                            repeatDelay: 2 + index
                          }}
                          className="text-3xl filter drop-shadow-lg"
                        >
                          {badge.icon}
                        </motion.div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <p
                              className="text-white font-cred-body font-bold text-sm"
                              style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                            >
                              {badge.name}
                            </p>
                            <motion.div
                              initial={{ scale: 0 }}
                              animate={{ scale: 1 }}
                              transition={{ delay: 0.8 + index * 0.2 }}
                            >
                              <Star className="w-3 h-3 text-yellow-400 fill-current" />
                            </motion.div>
                          </div>
                          <p
                            className="text-white/80 font-cred-body text-xs mb-1"
                            style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                          >
                            {badge.description}
                          </p>
                          <p
                            className="text-purple-300 font-cred-body text-xs font-medium"
                            style={{ textShadow: '1px 1px 3px rgba(0, 0, 0, 0.5)' }}
                          >
                            Earned {badge.earnedAt}
                          </p>
                        </div>
                        <motion.div
                          initial={{ opacity: 0, x: 10 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: 1 + index * 0.2 }}
                          className="flex flex-col items-center"
                        >
                          <Shield className="w-4 h-4 text-purple-400 mb-1" />
                          <span className="text-purple-300 text-xs font-semibold">
                            +{5 + index * 2}
                          </span>
                        </motion.div>
                      </motion.div>
                    ))}
                  </div>
                </Card>
              </motion.div>

              {/* Recent Activity */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <Card className="glass-effect p-6 border-white/10">
                  <h3 
                    className="text-lg font-cred-heading font-bold text-white mb-4"
                    style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
                  >
                    🕒 Recent Activity
                  </h3>
                  <div className="space-y-3">
                    {recentActivity.map((activity, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.4, delay: 0.5 + index * 0.1 }}
                        className="flex items-start gap-3 p-3 rounded-lg bg-black/20 border border-white/10"
                      >
                        {activity.type === 'score' ? (
                          <TrendingUp className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                        ) : (
                          <Award className="w-4 h-4 text-purple-400 mt-0.5 flex-shrink-0" />
                        )}
                        <div className="flex-1">
                          <p 
                            className="text-white font-cred-body text-sm"
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
            </div>
          </div>
        </div>
      </div>

      {/* Floating Action Button */}
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ duration: 0.6, delay: 2 }}
        className="fixed bottom-8 right-8 z-50"
      >
        <motion.div
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          animate={{
            boxShadow: [
              "0 0 20px rgba(16, 185, 129, 0.3)",
              "0 0 30px rgba(6, 214, 160, 0.4)",
              "0 0 20px rgba(16, 185, 129, 0.3)"
            ]
          }}
          transition={{
            boxShadow: { duration: 2, repeat: Infinity },
            scale: { duration: 0.2 }
          }}
          className="w-14 h-14 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full flex items-center justify-center cursor-pointer shadow-lg"
        >
          <motion.div
            animate={{ rotate: [0, 180, 360] }}
            transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
          >
            <Zap className="w-6 h-6 text-white" />
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Background Particles */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-white/20 rounded-full"
            initial={{
              x: Math.random() * window.innerWidth,
              y: Math.random() * window.innerHeight,
            }}
            animate={{
              y: [null, -100],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: Math.random() * 3 + 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
