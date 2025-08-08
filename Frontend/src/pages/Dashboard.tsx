import React, { useEffect } from "react";
import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
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
  Zap,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import CreditScoreCalculator from "@/components/CreditScoreCalculator";
import Navigation from "@/components/Navigation";
import OrbBackground from "@/components/ui/OrbBackground";
import { useApp } from "../context/AppContext";

const Dashboard = () => {
  const { dashboard, loading, error, loadDashboard, downloadPDF, clearError } = useApp();

  useEffect(() => {
    loadDashboard();
  }, []);

  const handleDownloadPDF = async (): Promise<void> => {
    try {
      await downloadPDF();
    } catch (error) {
      console.error("Failed to download PDF:", error);
    }
  };

  const getScoreClass = (score: number) => {
    if (score >= 750) return "excellent";
    if (score >= 700) return "good";
    if (score >= 650) return "fair";
    return "poor";
  };

  const formatDate = (dateString: string): string => {
    if (!dateString) return "Never";
    return new Date(dateString).toLocaleDateString();
  };

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen relative overflow-y-auto">
        <OrbBackground />
        <Navigation />
        <div className="pt-20 px-4 pb-8">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-center h-96">
              <div className="text-center">
                <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-emerald-500 mx-auto mb-4"></div>
                <p className="text-white/80 font-cred-body text-lg">Loading your dashboard...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="min-h-screen relative overflow-y-auto">
        <OrbBackground />
        <Navigation />
        <div className="pt-20 px-4 pb-8">
          <div className="max-w-7xl mx-auto">
            <Card className="glass-effect p-8 border-red-500/20 text-center">
              <AlertCircle className="w-16 h-16 text-red-400 mx-auto mb-4" />
              <h3 className="text-2xl font-cred-heading font-bold text-white mb-4">
                Error Loading Dashboard
              </h3>
              <p className="text-white/80 font-cred-body mb-6">{error}</p>
              <Button
                onClick={clearError}
                className="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600">
                Try Again
              </Button>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  // No data state
  if (!dashboard || !dashboard.hasData) {
    return (
      <div className="min-h-screen relative overflow-y-auto">
        <OrbBackground />
        <Navigation />
        <div className="pt-20 px-4 pb-8">
          <div className="max-w-7xl mx-auto">
            <Card className="glass-effect p-8 border-white/10 text-center">
              <Star className="w-16 h-16 text-emerald-400 mx-auto mb-4" />
              <h2 className="text-3xl font-cred-heading font-bold text-white mb-4">
                Welcome to CredNova!
              </h2>
              <p className="text-white/80 font-cred-body text-lg mb-6">
                Get started by submitting your financial information to calculate your credit score.
              </p>
              <Button
                onClick={() => (window.location.href = "/form")}
                className="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white font-cred-body font-semibold px-8 py-3">
                Calculate My Score
              </Button>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  // Use backend data
  const creditScore = dashboard.creditScore;
  const scoreDate = formatDate(dashboard.lastUpdatedDate);

  const scoreFactors = [
    { factor: "Payment History", impact: "positive", description: "Consistent payment patterns" },
    {
      factor: "Credit Utilization",
      impact: dashboard.loanApproved ? "positive" : "negative",
      description: "Current usage levels",
    },
    { factor: "Income Stability", impact: "neutral", description: "Steady income verification" },
    { factor: "Financial Behavior", impact: "positive", description: "Strong financial habits" },
  ];

  const scoreHistory = [
    { date: "2 months ago", score: Math.max(300, creditScore - 40) },
    { date: "1 month ago", score: Math.max(300, creditScore - 20) },
    { date: "Current", score: creditScore },
  ];

  const badges = [
    {
      name: "Credit Builder",
      description: "Successfully calculated credit score",
      earnedAt: scoreDate,
      icon: "�",
    },
    {
      name: "Data Complete",
      description: "Submitted comprehensive financial data",
      earnedAt: scoreDate,
      icon: "✅",
    },
    {
      name: dashboard.loanApproved ? "Loan Ready" : "Score Climber",
      description: dashboard.loanApproved
        ? "Qualified for loan approval"
        : "Growing credit profile",
      earnedAt: scoreDate,
      icon: dashboard.loanApproved ? "💳" : "📈",
    },
  ];

  const insights = [
    {
      type: dashboard.loanApproved ? "positive" : "neutral",
      title: "Loan Status",
      message: dashboard.loanApproved
        ? "Congratulations! You're approved for loans."
        : "Continue building to improve loan eligibility.",
    },
    {
      type: "tip",
      title: "Score Potential",
      message: `Your best achievable score is ${dashboard.bestAchievableScore}. Keep building!`,
    },
    {
      type: "info",
      title: "Score Range",
      message: `Your current score of ${creditScore} falls in the ${dashboard.scoreRange} range.`,
    },
  ];

  const recentActivity = [
    { type: "score", message: `Credit score calculated: ${creditScore}`, timestamp: "Recently" },
    { type: "badge", message: "Earned 'Credit Builder' badge", timestamp: scoreDate },
    { type: "data", message: "Financial data submitted", timestamp: scoreDate },
  ];

  const missingFields = dashboard.loanApproved
    ? []
    : ["Complete Profile", "Verify Income", "Additional Data Sources"];

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
            className="flex justify-between items-center mb-4">
            <div>
              <h1
                className="text-3xl font-cred-heading font-bold text-white mb-2"
                style={{ textShadow: "2px 2px 12px rgba(0, 0, 0, 0.8)" }}>
                Your Credit Dashboard
              </h1>
              <p
                className="text-white/80 font-cred-body text-base"
                style={{ textShadow: "1px 1px 6px rgba(0, 0, 0, 0.6)" }}>
                Track your alternative credit journey
              </p>
            </div>

            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                className="bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white font-cred-body font-semibold px-6 py-3 shadow-lg"
                onClick={handleDownloadPDF}>
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
                className="h-full">
                <Card className="glass-effect p-4 border-white/10 glow-effect h-full">
                  <div className="flex items-center justify-between mb-3">
                    <h2
                      className="text-xl font-cred-heading font-bold text-white"
                      style={{ textShadow: "1px 1px 8px rgba(0, 0, 0, 0.8)" }}>
                      Credit Dashboard Overview
                    </h2>
                    <span
                      className="text-white/60 font-cred-body text-sm"
                      style={{ textShadow: "1px 1px 4px rgba(0, 0, 0, 0.6)" }}>
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
                      className="mt-4 text-center">
                      <div className="flex items-center justify-center gap-2 mb-2">
                        <span
                          className="text-2xl font-cred-heading font-bold text-white"
                          style={{ textShadow: "2px 2px 8px rgba(0, 0, 0, 0.8)" }}>
                          {creditScore}
                        </span>
                        <Badge className="bg-emerald-500/20 text-emerald-400 border-emerald-400/30">
                          {dashboard.scoreRange}
                        </Badge>
                      </div>
                      <p
                        className="text-white/70 font-cred-body text-sm"
                        style={{ textShadow: "1px 1px 4px rgba(0, 0, 0, 0.6)" }}>
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
                          Best: {dashboard.bestAchievableScore}
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
                            domain={["dataMin - 20", "dataMax + 20"]}
                            width={40}
                          />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: "rgba(0, 0, 0, 0.8)",
                              border: "1px solid rgba(255, 255, 255, 0.2)",
                              borderRadius: "8px",
                              backdropFilter: "blur(15px)",
                              color: "white",
                              fontSize: "12px",
                            }}
                            labelStyle={{ color: "white", fontSize: "11px" }}
                          />
                          <Line
                            type="monotone"
                            dataKey="score"
                            stroke="url(#scoreGradient)"
                            strokeWidth={3}
                            dot={{
                              fill: "#10b981",
                              strokeWidth: 2,
                              r: 5,
                              stroke: "#065f46",
                            }}
                            activeDot={{
                              r: 8,
                              fill: "#06d6a0",
                              stroke: "#065f46",
                              strokeWidth: 3,
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
                transition={{ duration: 0.6, delay: 0.2 }}>
                <Card className="glass-effect p-4 border-white/10">
                  <h3
                    className="text-base font-cred-heading font-bold text-white mb-3"
                    style={{ textShadow: "1px 1px 8px rgba(0, 0, 0, 0.8)" }}>
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
                        className="flex items-center gap-3 p-3 rounded-lg bg-gradient-to-r from-purple-500/10 via-pink-500/5 to-purple-500/10 border border-purple-400/20 cursor-pointer">
                        <motion.div
                          animate={{ rotate: [0, 10, -10, 0] }}
                          transition={{ duration: 3, repeat: Infinity, repeatDelay: 2 }}
                          className="text-lg">
                          {badge.icon}
                        </motion.div>
                        <div className="flex-1 min-w-0">
                          <p
                            className="text-white font-cred-body font-medium text-xs truncate"
                            style={{ textShadow: "1px 1px 4px rgba(0, 0, 0, 0.6)" }}>
                            {badge.name}
                          </p>
                          <p
                            className="text-purple-300 font-cred-body text-xs"
                            style={{ textShadow: "1px 1px 3px rgba(0, 0, 0, 0.5)" }}>
                            {badge.description}
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
                transition={{ duration: 0.6, delay: 0.3 }}>
                <Card className="glass-effect p-4 border-white/10">
                  <h3
                    className="text-base font-cred-heading font-bold text-white mb-3"
                    style={{ textShadow: "1px 1px 8px rgba(0, 0, 0, 0.8)" }}>
                    🕒 Activity
                  </h3>
                  <div className="space-y-2">
                    {recentActivity.slice(0, 4).map((activity, index) => (
                      <motion.div
                        key={index}
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: 0.4 + index * 0.1 }}
                        className="flex items-start gap-2 p-2 rounded-lg bg-black/20 border border-white/5">
                        {activity.type === "score" ? (
                          <TrendingUp className="w-3 h-3 text-emerald-400 mt-0.5 flex-shrink-0" />
                        ) : activity.type === "badge" ? (
                          <Award className="w-3 h-3 text-purple-400 mt-0.5 flex-shrink-0" />
                        ) : (
                          <Info className="w-3 h-3 text-blue-400 mt-0.5 flex-shrink-0" />
                        )}
                        <div className="flex-1 min-w-0">
                          <p
                            className="text-white font-cred-body text-xs leading-tight"
                            style={{ textShadow: "1px 1px 4px rgba(0, 0, 0, 0.6)" }}>
                            {activity.message}
                          </p>
                          <p
                            className="text-white/60 font-cred-body text-xs mt-1"
                            style={{ textShadow: "1px 1px 3px rgba(0, 0, 0, 0.5)" }}>
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
                transition={{ duration: 0.6, delay: 0.35 }}>
                <Card className="glass-effect p-4 border-white/10">
                  <h3
                    className="text-base font-cred-heading font-bold text-white mb-3"
                    style={{ textShadow: "1px 1px 8px rgba(0, 0, 0, 0.8)" }}>
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
                          insight.type === "positive"
                            ? "bg-emerald-500/10 border-emerald-400/30 hover:border-emerald-400/50"
                            : insight.type === "warning"
                            ? "bg-orange-500/10 border-orange-400/30 hover:border-orange-400/50"
                            : "bg-blue-500/10 border-blue-400/30 hover:border-blue-400/50"
                        }`}>
                        <div className="flex items-start gap-2">
                          {insight.type === "positive" ? (
                            <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                          ) : insight.type === "warning" ? (
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

      {/* Floating Action Button */}
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ duration: 0.6, delay: 1.5 }}
        className="fixed bottom-8 right-8 z-50">
        <motion.div
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          animate={{
            boxShadow: [
              "0 0 20px rgba(16, 185, 129, 0.3)",
              "0 0 30px rgba(6, 214, 160, 0.4)",
              "0 0 20px rgba(16, 185, 129, 0.3)",
            ],
          }}
          transition={{
            boxShadow: { duration: 2, repeat: Infinity },
            scale: { duration: 0.2 },
          }}
          className="w-12 h-12 bg-gradient-to-r from-emerald-500 to-cyan-500 rounded-full flex items-center justify-center cursor-pointer shadow-lg">
          <motion.div
            animate={{ rotate: [0, 180, 360] }}
            transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            onClick={loadDashboard}>
            <Zap className="w-5 h-5 text-white" />
          </motion.div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default Dashboard;
