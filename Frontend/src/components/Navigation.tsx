import { Button } from "@/components/ui/button"
import { motion, useScroll, useTransform } from "framer-motion"
import { useEffect, useState } from "react"
import { Link, useLocation } from "react-router-dom"

const Navigation = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const location = useLocation()
  const { scrollY } = useScroll()
  const backgroundColor = useTransform(
    scrollY,
    [0, 100],
    ["rgba(0, 0, 0, 0)", "rgba(0, 0, 0, 0.3)"]
  )

  useEffect(() => {
    const unsubscribe = scrollY.onChange((latest) => {
      setIsScrolled(latest > 50)
    })
    return () => unsubscribe()
  }, [scrollY])

  return (
    <motion.nav
      style={{ backgroundColor }}
      className={`fixed top-0 left-0 right-0 z-50 p-6 transition-all duration-300 ${
        isScrolled ? 'backdrop-blur-md border-b border-white/10' : ''
      }`}
    >
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="flex items-center justify-between max-w-7xl mx-auto"
      >
        <Link to="/">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center space-x-2"
          >
            <motion.div
              animate={{ rotate: [0, 360] }}
              transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
              className="w-8 h-8 bg-gradient-to-r from-neon-blue to-neon-purple rounded-lg flex items-center justify-center"
            >
              <span className="text-white font-bold text-sm">S</span>
            </motion.div>
            <span
              className="text-white font-cred-heading font-bold text-lg tracking-wider"
              style={{ textShadow: '2px 2px 8px rgba(0, 0, 0, 0.8)' }}
            >
              CRED NOVA
            </span>
          </motion.div>
        </Link>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="hidden md:flex items-center space-x-8"
        >
          {[
            { name: "DASHBOARD", path: "/dashboard" },
            { name: "CHECK SCORE", path: "#check-score" },
            { name: "ABOUT US", path: "#about" },
            { name: "APP", path: "#app" }
          ].map((item, index) => (
            <motion.div key={item.name}>
              {item.path.startsWith('#') ? (
                <motion.a
                  href={item.path}
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4, delay: 0.1 * index }}
                  whileHover={{
                    scale: 1.1,
                    color: "#ffffff"
                  }}
                  className="text-white/70 hover:text-white transition-colors font-cred-body font-medium tracking-wide text-sm"
                  style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                >
                  {item.name}
                </motion.a>
              ) : (
                <Link to={item.path}>
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 * index }}
                    whileHover={{
                      scale: 1.1,
                      color: "#ffffff"
                    }}
                    className={`text-white/70 hover:text-white transition-colors font-cred-body font-medium tracking-wide text-sm ${
                      location.pathname === item.path ? 'text-white' : ''
                    }`}
                    style={{ textShadow: '1px 1px 4px rgba(0, 0, 0, 0.6)' }}
                  >
                    {item.name}
                  </motion.div>
                </Link>
              )}
            </motion.div>
          ))}
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Button variant="outline" className="glass-effect border-white/30 text-white hover:bg-white/10 hover:border-white/50 nike-button font-nike-helvetica font-bold tracking-wide text-sm px-6 py-2">
            GET STARTED
          </Button>
        </motion.div>
      </motion.div>
    </motion.nav>
  )
}

export default Navigation