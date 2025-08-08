import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { MessageCircle } from 'lucide-react';
import ChatBotOverlay from './ChatBotOverlay';

const FloatingChatButton: React.FC = () => {
  const [isChatBotOpen, setIsChatBotOpen] = useState(false);

  return (
    <>
      {/* Floating Action Button - AI Financial Advisor */}
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ duration: 0.6, delay: 1.5 }}
        className="fixed bottom-8 right-8 z-50"
      >
        <motion.div
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => setIsChatBotOpen(true)}
          animate={{
            boxShadow: [
              "0 0 20px rgba(59, 130, 246, 0.4)",
              "0 0 30px rgba(147, 51, 234, 0.5)",
              "0 0 20px rgba(59, 130, 246, 0.4)"
            ]
          }}
          transition={{
            boxShadow: { duration: 2, repeat: Infinity },
            scale: { duration: 0.2 }
          }}
          className="w-14 h-14 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 rounded-full flex items-center justify-center cursor-pointer shadow-lg relative overflow-hidden group"
        >
          {/* Animated background gradient */}
          <motion.div
            animate={{
              background: [
                "linear-gradient(45deg, #3b82f6, #8b5cf6, #ec4899)",
                "linear-gradient(45deg, #8b5cf6, #ec4899, #3b82f6)",
                "linear-gradient(45deg, #ec4899, #3b82f6, #8b5cf6)"
              ]
            }}
            transition={{ duration: 3, repeat: Infinity }}
            className="absolute inset-0 rounded-full"
          />
          
          {/* Icon container */}
          <motion.div
            animate={{ rotate: [0, 360] }}
            transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
            className="relative z-10"
          >
            <MessageCircle className="w-6 h-6 text-white" />
          </motion.div>
          
          {/* Pulse effect */}
          <motion.div
            animate={{
              scale: [1, 1.5, 1],
              opacity: [0.7, 0, 0.7]
            }}
            transition={{ duration: 2, repeat: Infinity }}
            className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full"
          />
        </motion.div>
        
        {/* Tooltip */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          whileHover={{ opacity: 1, x: 0 }}
          className="absolute right-16 top-1/2 transform -translate-y-1/2 bg-black/80 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap pointer-events-none"
        >
          AI Financial Advisor
          <div className="absolute right-0 top-1/2 transform translate-x-1 -translate-y-1/2 w-2 h-2 bg-black/80 rotate-45" />
        </motion.div>
      </motion.div>

      {/* ChatBot Overlay */}
      <ChatBotOverlay 
        isOpen={isChatBotOpen} 
        onClose={() => setIsChatBotOpen(false)} 
      />
    </>
  );
};

export default FloatingChatButton;
