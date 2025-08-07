import { motion, useScroll, useTransform } from "framer-motion"
import { useRef } from "react"
import CreditScoreCalculator from "./CreditScoreCalculator"

const HeroSection = () => {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"]
  })

  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"])
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0])

  return (
    <section ref={ref} className="relative min-h-screen flex items-center justify-center px-6">
      {/* Content backdrop for better readability */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/10 via-transparent to-black/20 pointer-events-none"></div>

      <motion.div
        style={{ y, opacity }}
        className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center relative z-10"
      >
        {/* Left Content */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="space-y-8"
        >
          <div className="space-y-6">
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-4xl md:text-5xl lg:text-6xl font-cred-heading font-bold text-white leading-tight tracking-tight"
              style={{
                textShadow: '2px 2px 20px rgba(0, 0, 0, 0.8), 0 0 40px rgba(0, 0, 0, 0.6)'
              }}
            >
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.6 }}
                className="text-white font-cred-heading block mb-4"
              >
                Alternative credit
              </motion.span>
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8, delay: 0.8 }}
                className="text-white font-cred-heading block mb-4"
              >
                scoring made
              </motion.span>
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.8, delay: 1 }}
                className="text-gradient-neon font-cred-heading block"
              >
                fair and transparent
              </motion.span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.2 }}
              className="text-lg md:text-xl text-white font-cred-body leading-relaxed max-w-lg"
              style={{
                textShadow: '1px 1px 10px rgba(0, 0, 0, 0.8)'
              }}
            >
              No CIBIL? No problem. Let your rent and utility payments speak for you.
            </motion.p>
          </div>

          {/* Features */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1.4 }}
            className="space-y-6 pt-8"
          >
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 1.6 }}
              className="flex items-center gap-4"
            >
              <div className="w-3 h-3 bg-gradient-to-r from-emerald-400 to-cyan-400 rounded-full shadow-lg"></div>
              <span
                className="text-white font-cred-body text-lg"
                style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
              >
                <span className="text-emerald-400 font-bold">49 million Americans</span> excluded from traditional credit
              </span>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 1.8 }}
              className="flex items-center gap-4"
            >
              <div className="w-3 h-3 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full shadow-lg"></div>
              <span
                className="text-white font-cred-body text-lg"
                style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
              >
                <span className="text-purple-400 font-bold">Alternative data</span> creates fair opportunities
              </span>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 2 }}
              className="flex items-center gap-4"
            >
              <div className="w-3 h-3 bg-gradient-to-r from-orange-400 to-red-400 rounded-full shadow-lg"></div>
              <span
                className="text-white font-cred-body text-lg"
                style={{ textShadow: '1px 1px 8px rgba(0, 0, 0, 0.8)' }}
              >
                <span className="text-orange-400 font-bold">Transparent scoring</span> you can understand
              </span>
            </motion.div>
          </motion.div>
        </motion.div>

        {/* Right Content - Credit Score Calculator */}
        <motion.div
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="relative flex justify-center lg:justify-end"
        >
          <CreditScoreCalculator
            targetScore={756}
            className="max-w-md"
          />
        </motion.div>
      </motion.div>
    </section>
  )
}

export default HeroSection