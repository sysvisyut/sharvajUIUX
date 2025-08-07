import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ArrowRight, Sparkles, TrendingUp, Award, Target } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import OrbBackground from '@/components/ui/OrbBackground';

const ScoreResult = () => {
  const [isCalculating, setIsCalculating] = useState(true);
  const [showScore, setShowScore] = useState(false);
  const [animatedScore, setAnimatedScore] = useState(0);
  const navigate = useNavigate();
  
  // Simulated ML calculation result
  const finalScore = 756;
  const scoreCategory = "Excellent";
  const improvement = "+47";

  useEffect(() => {
    // Simulate ML model calculation time
    const calculationTimer = setTimeout(() => {
      setIsCalculating(false);
      setShowScore(true);
    }, 5000);

    return () => clearTimeout(calculationTimer);
  }, []);

  useEffect(() => {
    if (showScore) {
      // Animate score counting up
      const duration = 2000;
      const steps = 60;
      const increment = finalScore / steps;
      let currentStep = 0;

      const scoreTimer = setInterval(() => {
        currentStep++;
        setAnimatedScore(Math.min(Math.floor(increment * currentStep), finalScore));
        
        if (currentStep >= steps) {
          clearInterval(scoreTimer);
        }
      }, duration / steps);

      return () => clearInterval(scoreTimer);
    }
  }, [showScore, finalScore]);

  // Spark animation variants
  const sparkVariants = {
    animate: {
      scale: [1, 1.2, 1],
      rotate: [0, 180, 360],
      opacity: [0.7, 1, 0.7],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const floatingSparkVariants = {
    animate: {
      y: [-20, -40, -20],
      x: [-10, 10, -10],
      opacity: [0.3, 0.8, 0.3],
      scale: [0.8, 1.2, 0.8],
      transition: {
        duration: 3,
        repeat: Infinity,
        ease: "easeInOut",
        delay: Math.random() * 2
      }
    }
  };

  const LoadingScreen = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="flex flex-col items-center justify-center min-h-screen relative"
    >
      {/* Floating Sparks */}
      {[...Array(12)].map((_, i) => (
        <motion.div
          key={i}
          variants={floatingSparkVariants}
          animate="animate"
          className="absolute"
          style={{
            left: `${20 + (i * 6)}%`,
            top: `${30 + (i * 4)}%`,
          }}
        >
          <Sparkles className="w-6 h-6 text-neon-blue opacity-60" />
        </motion.div>
      ))}

      {/* Central Loading Animation */}
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.8 }}
        className="relative"
      >
        {/* Rotating Ring */}
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
          className="w-32 h-32 border-4 border-transparent border-t-neon-blue border-r-neon-purple rounded-full"
        />
        
        {/* Inner Pulsing Circle */}
        <motion.div
          variants={sparkVariants}
          animate="animate"
          className="absolute inset-4 bg-gradient-to-r from-neon-blue to-neon-purple rounded-full flex items-center justify-center"
        >
          <TrendingUp className="w-12 h-12 text-white" />
        </motion.div>
      </motion.div>

      {/* Loading Text */}
      <motion.div
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.5 }}
        className="mt-12 text-center"
      >
        <h2 
          className="text-3xl font-cred-heading font-bold text-white mb-4 tracking-tight uppercase"
          style={{ textShadow: '2px 2px 12px rgba(0, 0, 0, 0.8)' }}
        >
          Calculating Your Score
        </h2>
        
        <motion.p
          animate={{ opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity }}
          className="text-white/70 font-cred-body text-lg"
          style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.6)' }}
        >
          Analyzing your financial profile with AI...
        </motion.p>
      </motion.div>
    </motion.div>
  );

  const ScoreDisplay = () => (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
      className="min-h-screen flex flex-col items-center justify-center px-6"
    >
      {/* Hero Section */}
      <motion.div
        initial={{ y: -50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 1, delay: 0.3 }}
        className="text-center mb-12"
      >
        <motion.h1
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.8, delay: 0.5 }}
          className="text-5xl md:text-6xl font-cred-heading font-black text-white mb-6 tracking-tight uppercase"
          style={{ textShadow: '3px 3px 15px rgba(0, 0, 0, 0.8)' }}
        >
          Your Credit Score
        </motion.h1>
        
        <motion.p
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.7 }}
          className="text-white/80 font-cred-body text-xl max-w-2xl mx-auto"
          style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.6)' }}
        >
          Based on your alternative credit data and transparent scoring algorithm
        </motion.p>
      </motion.div>

      {/* Central Score Card */}
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ 
          type: "spring", 
          stiffness: 100, 
          damping: 15,
          delay: 1
        }}
        whileHover={{ 
          scale: 1.05,
          rotateY: 5,
          transition: { duration: 0.3 }
        }}
        className="relative mb-12"
      >
        <Card className="glass-effect border-white/20 p-12 glow-effect relative overflow-hidden">
          {/* Background Gradient Animation */}
          <motion.div
            animate={{
              background: [
                "linear-gradient(45deg, rgba(20, 78, 227, 0.1), rgba(176, 67, 255, 0.1))",
                "linear-gradient(45deg, rgba(176, 67, 255, 0.1), rgba(255, 95, 95, 0.1))",
                "linear-gradient(45deg, rgba(255, 95, 95, 0.1), rgba(20, 78, 227, 0.1))"
              ]
            }}
            transition={{ duration: 4, repeat: Infinity }}
            className="absolute inset-0 rounded-lg"
          />
          
          {/* Score Circle */}
          <div className="relative z-10 flex flex-col items-center">
            {/* Circular Progress */}
            <div className="relative w-64 h-64 mb-8">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                {/* Background Circle */}
                <circle
                  cx="50"
                  cy="50"
                  r="45"
                  stroke="rgba(255, 255, 255, 0.1)"
                  strokeWidth="8"
                  fill="none"
                />
                {/* Progress Circle */}
                <motion.circle
                  cx="50"
                  cy="50"
                  r="45"
                  stroke="url(#scoreGradient)"
                  strokeWidth="8"
                  fill="none"
                  strokeLinecap="round"
                  initial={{ pathLength: 0 }}
                  animate={{ pathLength: finalScore / 850 }}
                  transition={{ duration: 2, delay: 1.5, ease: "easeOut" }}
                  style={{
                    filter: "drop-shadow(0 0 10px rgba(20, 78, 227, 0.5))"
                  }}
                />
                <defs>
                  <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#144ee3" />
                    <stop offset="50%" stopColor="#b043ff" />
                    <stop offset="100%" stopColor="#ff5f5f" />
                  </linearGradient>
                </defs>
              </svg>
              
              {/* Score Number */}
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  transition={{ 
                    type: "spring", 
                    stiffness: 200, 
                    damping: 10,
                    delay: 2
                  }}
                  className="text-center"
                >
                  <div className="text-6xl font-cred-heading font-black text-white mb-2">
                    {animatedScore}
                  </div>
                  <div className="text-neon-blue font-cred-body font-medium text-lg">
                    {scoreCategory}
                  </div>
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 2.5 }}
                    className="text-emerald-400 font-cred-body text-sm mt-1"
                  >
                    {improvement} points improved
                  </motion.div>
                </motion.div>
              </div>
            </div>

            {/* Score Range */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 2.8 }}
              className="flex justify-between w-full max-w-xs text-white/60 font-cred-body text-sm"
            >
              <span>300</span>
              <span>850</span>
            </motion.div>
          </div>
        </Card>
      </motion.div>

      {/* Action Button */}
      <motion.div
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, delay: 3 }}
      >
        <Link to="/dashboard">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-neon-blue to-neon-purple hover:from-neon-purple hover:to-neon-pink text-white font-cred-heading font-bold px-12 py-4 text-xl tracking-wide uppercase nike-button glow-effect"
            >
              <Award className="mr-3 w-6 h-6" />
              Return to Dashboard
              <ArrowRight className="ml-3 w-6 h-6" />
            </Button>
          </motion.div>
        </Link>
      </motion.div>
    </motion.div>
  );

  return (
    <div className="relative min-h-screen">
      <OrbBackground />
      <div className="fixed inset-0 bg-gradient-to-br from-black/20 via-transparent to-black/30 pointer-events-none -z-5"></div>
      
      <AnimatePresence mode="wait">
        {isCalculating ? (
          <LoadingScreen key="loading" />
        ) : (
          <ScoreDisplay key="score" />
        )}
      </AnimatePresence>
    </div>
  );
};

export default ScoreResult;
