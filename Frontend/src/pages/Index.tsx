import OrbBackground from "@/components/ui/OrbBackground"
import Navigation from "@/components/Navigation"
import HeroSection from "@/components/HeroSection"
import FloatingChatButton from "@/components/FloatingChatButton"
import { motion } from "framer-motion"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Link } from "react-router-dom"

const FeatureCard = ({ title, description, icon, delay }: {
  title: string;
  description: string;
  icon: string;
  delay: number
}) => (
  <motion.div
    initial={{ opacity: 0, y: 50 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, delay }}
    viewport={{ once: true }}
    whileHover={{
      scale: 1.05,
      rotateY: 5
    }}
  >
    <Card className="glass-effect p-6 h-full border-white/10">
      <div className="text-4xl mb-4">{icon}</div>
      <h3
        className="text-xl font-cred-heading font-bold text-white mb-3 tracking-wide uppercase"
        style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.8)' }}
      >
        {title}
      </h3>
      <p
        className="text-white/80 font-cred-body text-sm leading-relaxed"
        style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
      >
        {description}
      </p>
    </Card>
  </motion.div>
)

const Index = () => {
  return (
    <div className="relative min-h-screen">
      <OrbBackground />
      {/* Gradient overlay to blend with orb background */}
      <div className="fixed inset-0 bg-gradient-to-br from-black/20 via-transparent to-black/30 pointer-events-none -z-5"></div>
      <Navigation />
      <HeroSection />

      {/* Features Section */}
      <section className="relative py-20 px-6">
        {/* Section backdrop */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/5 via-black/10 to-black/5 pointer-events-none"></div>
        <div className="max-w-7xl mx-auto relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2
              className="text-4xl md:text-5xl font-cred-heading font-black text-white mb-6 tracking-tight uppercase"
              style={{ textShadow: '2px 2px 12px rgba(0, 0, 0, 0.8)' }}
            >
              Why Choose <span className="text-gradient-neon">CRED NOVA</span>?
            </h2>
            <p
              className="text-white/80 text-lg max-w-2xl mx-auto font-cred-body"
              style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.6)' }}
            >
              Experience the future of alternative credit scoring with transparent, fair solutions
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <FeatureCard
              title="Alternative Data"
              description="We use rent payments, utility bills, and other alternative data to build your credit profile fairly"
              icon="📊"
              delay={0.1}
            />
            <FeatureCard
              title="Transparent Scoring"
              description="Understand exactly how your score is calculated with clear explanations and actionable insights"
              icon="🔍"
              delay={0.2}
            />
            <FeatureCard
              title="Fair Access"
              description="No traditional credit history? No problem. We believe everyone deserves a fair chance at credit"
              icon="⚖️"
              delay={0.3}
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-20 px-6">
        {/* Section backdrop */}
        <div className="absolute inset-0 bg-gradient-to-b from-black/10 via-black/15 to-black/10 pointer-events-none"></div>
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto text-center relative z-10"
        >
          <Card className="glass-effect p-12 glow-effect border-white/10">
            <h2
              className="text-4xl md:text-5xl font-cred-heading font-black text-white mb-6 tracking-tight uppercase"
              style={{ textShadow: '2px 2px 12px rgba(0, 0, 0, 0.8)' }}
            >
              Ready to Check Your Score?
            </h2>
            <p
              className="text-white/80 text-lg mb-8 max-w-2xl mx-auto font-cred-body"
              style={{ textShadow: '1px 1px 6px rgba(0, 0, 0, 0.6)' }}
            >
              Join thousands already using CRED NOVA for fair and transparent credit scoring
            </p>
            <Link to="/check-score">
              <motion.div
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Button size="lg" className="bg-white text-black hover:bg-white/90 nike-button font-cred-heading font-bold px-8 py-4 text-lg tracking-wide uppercase">
                  CHECK MY SCORE
                </Button>
              </motion.div>
            </Link>
          </Card>
        </motion.div>
      </section>

      {/* Floating Chat Button */}
      <FloatingChatButton />
    </div>
  )
}

export default Index