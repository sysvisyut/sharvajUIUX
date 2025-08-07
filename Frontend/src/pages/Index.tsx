import AnimatedBackground from "@/components/ui/AnimatedBackground"
import Navigation from "@/components/Navigation"
import HeroSection from "@/components/HeroSection"

const Index = () => {
  return (
    <div className="relative min-h-screen bg-background overflow-hidden">
      <AnimatedBackground />
      <Navigation />
      <HeroSection />
    </div>
  )
}

export default Index