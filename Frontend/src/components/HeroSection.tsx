import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-6">
      <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">
        {/* Left Content */}
        <div className="space-y-8">
          <div className="space-y-6">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-white leading-tight">
              Fueling Business Growth Through{" "}
              <span className="relative">
                <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-neon-blue/20 border border-neon-blue/30 text-neon-blue text-lg md:text-xl font-medium">
                  <span className="w-2 h-2 bg-neon-blue rounded-full"></span>
                  Innovative
                </span>
              </span>{" "}
              and{" "}
              <span className="text-gradient-neon">to Scale.</span>
            </h1>
            
            <div className="flex items-center gap-4">
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-secondary/50 border border-white/20 text-white text-sm font-medium">
                <span className="w-2 h-2 bg-white rounded-full"></span>
                Scalable Tools
              </span>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 gap-8 pt-8">
            <div>
              <div className="text-4xl md:text-5xl font-bold text-white mb-2">100k+</div>
              <div className="text-muted-foreground text-sm">Money Protected</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold text-white mb-2">30K+</div>
              <div className="text-muted-foreground text-sm">Active Users</div>
            </div>
          </div>
        </div>

        {/* Right Content - Placeholder Component */}
        <div className="relative">
          <Card className="glass-effect p-8 space-y-6 max-w-md ml-auto">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-gradient-to-r from-neon-blue to-neon-purple rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">P</span>
                </div>
                <span className="text-white font-semibold">Virtual</span>
              </div>
            </div>
            
            <div className="space-y-4">
              <div className="flex justify-center">
                <div className="w-16 h-10 bg-gradient-to-r from-neon-blue/20 to-neon-purple/20 rounded border border-white/20"></div>
              </div>
              
              <div className="text-center">
                <div className="text-2xl font-bold text-white">•••• •••• •••• 5491</div>
                <div className="text-sm text-muted-foreground mt-1">12/23/2030</div>
                <div className="text-sm text-muted-foreground">Alex Ryhan</div>
              </div>
            </div>
            
            <div className="pt-4 border-t border-white/10">
              <p className="text-sm text-muted-foreground leading-relaxed">
                Simplifying finance with smart, scalable tools—so your business grows faster and smarter.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </section>
  )
}

export default HeroSection