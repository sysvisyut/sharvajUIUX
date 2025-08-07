import React, { useEffect, useState, useRef, useCallback } from 'react';
import { motion, useScroll, useTransform, useSpring } from 'framer-motion';

interface CreditScoreCalculatorProps {
  targetScore?: number;
  className?: string;
}

const CreditScoreCalculator: React.FC<CreditScoreCalculatorProps> = ({
  targetScore = 756,
  className = ""
}) => {
  const [currentScore, setCurrentScore] = useState(300);
  const elementRef = useRef<HTMLDivElement>(null);

  // Scroll-based animation
  const { scrollYProgress } = useScroll({
    target: elementRef,
    offset: ["start end", "end start"]
  });

  // Transform scroll progress to score range (300-850)
  const scoreRange = useTransform(scrollYProgress, [0, 0.5, 1], [300, targetScore, targetScore]);
  const smoothScore = useSpring(scoreRange, {
    stiffness: 100,
    damping: 30,
    restDelta: 1
  });

  useEffect(() => {
    const unsubscribe = smoothScore.onChange((latest) => {
      setCurrentScore(Math.round(latest));
    });
    return unsubscribe;
  }, [smoothScore]);

  const getScoreColor = (score: number) => {
    if (score >= 750) return { primary: '#00D4AA', secondary: '#00F5C4', glow: '#00D4AA' }; // Cred green
    if (score >= 650) return { primary: '#FF6B35', secondary: '#FF8E53', glow: '#FF6B35' }; // Cred orange
    return { primary: '#FF4757', secondary: '#FF6B7A', glow: '#FF4757' }; // Cred red
  };

  const getGradientStops = (score: number) => {
    const percentage = Math.min((score - 300) / (850 - 300) * 270, 270); // 270 degrees for 3/4 circle
    const colors = getScoreColor(score);

    return {
      background: `conic-gradient(from -135deg, ${colors.primary} 0deg, ${colors.secondary} ${percentage}deg, #1a1a1a ${percentage}deg, #1a1a1a 270deg, transparent 270deg)`,
      glow: colors.glow
    };
  };

  const getScoreLabel = (score: number) => {
    if (score >= 750) return { text: 'Excellent', desc: 'You qualify for the best rates' };
    if (score >= 700) return { text: 'Very Good', desc: 'Great credit opportunities' };
    if (score >= 650) return { text: 'Good', desc: 'Most credit products available' };
    if (score >= 600) return { text: 'Fair', desc: 'Some credit options available' };
    return { text: 'Building', desc: 'Focus on building credit history' };
  };

  const gradientData = getGradientStops(currentScore);
  const scoreLabel = getScoreLabel(currentScore);
  const colors = getScoreColor(currentScore);

  return (
    <motion.div
      ref={elementRef}
      className={`flex flex-col items-center ${className}`}
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, delay: 0.2 }}
    >
      <div className="relative w-80 h-80">
        {/* Outer glow effect */}
        <motion.div
          className="absolute inset-0 rounded-full opacity-30 blur-2xl"
          style={{
            backgroundColor: gradientData.glow,
            scale: 1.2
          }}
          animate={{
            opacity: [0.2, 0.4, 0.2],
            scale: [1.1, 1.3, 1.1]
          }}
          transition={{
            duration: 3,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />

        {/* Main circle container */}
        <div className="relative w-full h-full">
          {/* Background circle */}
          <div className="absolute inset-4 rounded-full bg-gradient-to-br from-gray-900 to-black border border-gray-800 shadow-2xl" />

          {/* Progress ring */}
          <svg className="absolute inset-0 w-full h-full -rotate-[135deg]" viewBox="0 0 100 100">
            {/* Background track */}
            <circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke="#1a1a1a"
              strokeWidth="3"
              strokeDasharray="212 212"
              strokeDashoffset="0"
            />
            {/* Progress track */}
            <motion.circle
              cx="50"
              cy="50"
              r="45"
              fill="none"
              stroke={`url(#gradient-${currentScore})`}
              strokeWidth="3"
              strokeLinecap="round"
              strokeDasharray="212 212"
              initial={{ strokeDashoffset: 212 }}
              animate={{
                strokeDashoffset: 212 - (212 * Math.min((currentScore - 300) / (850 - 300), 1))
              }}
              transition={{ duration: 1, ease: "easeOut" }}
            />
            {/* Gradient definition */}
            <defs>
              <linearGradient id={`gradient-${currentScore}`} x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor={colors.primary} />
                <stop offset="100%" stopColor={colors.secondary} />
              </linearGradient>
            </defs>
          </svg>

          {/* Center content */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <motion.div
              className="text-center"
              animate={{ scale: [1, 1.02, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              <div className="text-gray-400 text-sm font-cred-body font-medium mb-2 tracking-wider uppercase">
                Credit Score
              </div>
              <motion.div
                className="text-6xl font-cred-heading font-bold mb-2 transition-colors duration-500"
                style={{ color: colors.primary }}
                animate={{
                  textShadow: [
                    `0 0 20px ${colors.glow}40`,
                    `0 0 30px ${colors.glow}60`,
                    `0 0 20px ${colors.glow}40`
                  ]
                }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                {currentScore}
              </motion.div>
              <div className="text-white text-lg font-cred-body font-semibold">
                {scoreLabel.text}
              </div>
            </motion.div>
          </div>
        </div>

        {/* Score range indicators */}
        <div className="absolute -bottom-6 left-0 right-0 flex justify-between text-xs text-gray-500 font-cred-body">
          <span>300</span>
          <span>850</span>
        </div>
      </div>

      {/* Score description */}
      <motion.div
        className="mt-12 text-center max-w-sm"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.8 }}
      >
        <div className="text-white text-sm font-cred-body leading-relaxed mb-4">
          {scoreLabel.desc}
        </div>

        {/* Credit factors */}
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-800">
            <div className="text-emerald-400 font-semibold mb-1">Payment History</div>
            <div className="text-gray-400">35% of score</div>
          </div>
          <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-800">
            <div className="text-blue-400 font-semibold mb-1">Credit Utilization</div>
            <div className="text-gray-400">30% of score</div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default CreditScoreCalculator;
