import { Button } from "@/components/ui/button"

const Navigation = () => {
  return (
    <nav className="absolute top-0 left-0 right-0 z-50 p-6">
      <div className="flex items-center justify-between max-w-7xl mx-auto">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-gradient-to-r from-neon-blue to-neon-purple rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">P</span>
          </div>
          <span className="text-white font-semibold text-lg">PremiumTech</span>
        </div>
        
        <div className="hidden md:flex items-center space-x-8">
          <a href="#" className="text-white/80 hover:text-white transition-colors">Features</a>
          <a href="#" className="text-white/80 hover:text-white transition-colors">Products</a>
          <a href="#" className="text-white/80 hover:text-white transition-colors">Solutions</a>
          <a href="#" className="text-white/80 hover:text-white transition-colors">App</a>
        </div>
        
        <Button variant="outline" className="glass-effect border-white/20 text-white hover:bg-white/10">
          Get Started
        </Button>
      </div>
    </nav>
  )
}

export default Navigation