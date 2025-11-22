'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Quote {
  text: string;
  author: string;
  work: string;
  comment: string;
}

interface Emotion {
  id: string;
  label: string;
  color: string;
  quotes: Quote[];
}

interface QuotesData {
  emotions: Emotion[];
}

type Stage = 'intro' | 'loading' | 'prescription';

export default function BibliotherapistPage() {
  const [stage, setStage] = useState<Stage>('intro');
  const [selectedEmotion, setSelectedEmotion] = useState<Emotion | null>(null);
  const [currentQuote, setCurrentQuote] = useState<Quote | null>(null);
  const [quotesData, setQuotesData] = useState<QuotesData | null>(null);

  // Load quotes data
  useEffect(() => {
    fetch('/quotes.json')
      .then((res) => res.json())
      .then((data: QuotesData) => setQuotesData(data))
      .catch((err) => console.error('Failed to load quotes:', err));
  }, []);

  const handleEmotionSelect = (emotion: Emotion) => {
    setSelectedEmotion(emotion);
    setStage('loading');

    // Random quote from selected emotion
    const randomQuote = emotion.quotes[Math.floor(Math.random() * emotion.quotes.length)];

    // Show loading for 2.5 seconds
    setTimeout(() => {
      setCurrentQuote(randomQuote);
      setStage('prescription');
    }, 2500);
  };

  const handleReset = () => {
    setStage('intro');
    setSelectedEmotion(null);
    setCurrentQuote(null);
  };

  if (!quotesData) {
    return (
      <div className="min-h-screen bg-charcoal flex items-center justify-center">
        <div className="text-cream font-courier text-lg">Loading the library...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-charcoal text-cream flex items-center justify-center p-4 overflow-hidden">
      {/* Subtle background texture */}
      <div className="absolute inset-0 opacity-5 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMzLjMxNCAwIDYgMi42ODYgNiA2cy0yLjY4NiA2LTYgNi02LTIuNjg2LTYtNiAyLjY4Ni02IDYtNiIgc3Ryb2tlPSIjRjVGNURDIiBzdHJva2Utd2lkdGg9IjEiLz48L2c+PC9zdmc+')]" />

      <AnimatePresence mode="wait">
        {/* STAGE 1: INTRO */}
        {stage === 'intro' && (
          <motion.div
            key="intro"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-3xl w-full text-center space-y-12"
          >
            {/* Title */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              <h1 className="font-playfair text-6xl md:text-7xl font-bold text-gold mb-4">
                The Bibliotherapist
              </h1>
              <p className="font-courier text-cream/70 text-sm tracking-wider uppercase">
                Est. 1818 — London
              </p>
            </motion.div>

            {/* Question */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="space-y-2"
            >
              <p className="font-playfair text-2xl md:text-3xl italic text-cream/90">
                "What is haunting your soul today?"
              </p>
            </motion.div>

            {/* Emotion Tags */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.6 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-2xl mx-auto"
            >
              {quotesData.emotions.map((emotion, index) => (
                <motion.button
                  key={emotion.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.7 + index * 0.1 }}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleEmotionSelect(emotion)}
                  className="px-6 py-4 border-2 border-gold/30 hover:border-gold bg-charcoal/50 hover:bg-gold/10 transition-all duration-300 font-courier text-sm tracking-wider uppercase relative overflow-hidden group"
                  style={{
                    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
                  }}
                >
                  <div className="absolute inset-0 bg-gold/5 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
                  <span className="relative z-10 text-cream">{emotion.label}</span>
                </motion.button>
              ))}
            </motion.div>

            {/* Footer quote */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.2, duration: 0.6 }}
              className="pt-8"
            >
              <p className="font-courier text-xs text-cream/40 italic">
                "The good ended happily, and the bad unhappily. That is what Fiction means."
                <br />— Oscar Wilde
              </p>
            </motion.div>
          </motion.div>
        )}

        {/* STAGE 2: LOADING */}
        {stage === 'loading' && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center space-y-8"
          >
            {/* Quill pen animation */}
            <motion.div
              animate={{
                rotate: [0, -10, 10, -10, 0],
                y: [0, -10, 0, -5, 0],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="text-6xl mb-8"
            >
              🖋️
            </motion.div>

            {/* Loading text with typewriter effect */}
            <motion.div className="space-y-2">
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="font-courier text-xl text-cream"
              >
                Consulting the ghosts of writers...
              </motion.p>
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: '200px' }}
                transition={{ duration: 2, ease: 'easeInOut' }}
                className="h-0.5 bg-gold/50 mx-auto"
              />
            </motion.div>

            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: [0, 1, 0.7, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="font-courier text-sm text-cream/60"
            >
              {selectedEmotion?.label}
            </motion.p>
          </motion.div>
        )}

        {/* STAGE 3: PRESCRIPTION */}
        {stage === 'prescription' && currentQuote && (
          <motion.div
            key="prescription"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl w-full space-y-12"
          >
            {/* Header */}
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-center border-b border-gold/20 pb-6"
            >
              <h2 className="font-playfair text-4xl md:text-5xl text-gold mb-2">
                ℞ Prescription
              </h2>
              <p className="font-courier text-xs text-cream/60 tracking-widest uppercase">
                For {selectedEmotion?.label}
              </p>
            </motion.div>

            {/* Quote */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.5, duration: 0.8 }}
              className="bg-charcoal/80 border-l-4 border-gold p-8 md:p-12 space-y-6"
              style={{
                boxShadow: '0 10px 40px rgba(0, 0, 0, 0.4)',
              }}
            >
              <motion.blockquote
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.8, duration: 1 }}
                className="font-playfair text-2xl md:text-3xl italic text-cream leading-relaxed"
              >
                "{currentQuote.text}"
              </motion.blockquote>

              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.2, duration: 0.6 }}
                className="flex items-center justify-between border-t border-cream/10 pt-6"
              >
                <div className="font-courier text-sm text-cream/80">
                  <p className="font-bold">— {currentQuote.author}</p>
                  <p className="italic text-cream/60">{currentQuote.work}</p>
                </div>
              </motion.div>
            </motion.div>

            {/* Modern Comment (The Roast) */}
            <motion.div
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 1.5, duration: 0.6 }}
              className="bg-deep-brown/40 border border-gold/30 p-6 md:p-8"
            >
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 1.8, duration: 0.8 }}
                className="font-courier text-base md:text-lg text-cream/90 leading-relaxed"
              >
                <span className="text-gold font-bold">⚠ Modern Translation: </span>
                {currentQuote.comment}
              </motion.p>
            </motion.div>

            {/* Action Buttons */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 2, duration: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center pt-6"
            >
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => handleEmotionSelect(selectedEmotion!)}
                className="px-8 py-3 border-2 border-gold/50 hover:border-gold bg-charcoal hover:bg-gold/10 transition-all duration-300 font-courier text-sm tracking-wider uppercase"
              >
                Another Dose
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleReset}
                className="px-8 py-3 bg-gold hover:bg-faded-gold text-charcoal transition-all duration-300 font-courier text-sm tracking-wider uppercase font-bold"
              >
                New Ailment
              </motion.button>
            </motion.div>

            {/* Footer */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 2.3, duration: 0.6 }}
              className="text-center pt-8 border-t border-gold/10"
            >
              <p className="font-courier text-xs text-cream/40 italic">
                "There is no greater agony than bearing an untold story inside you."
                <br />— Maya Angelou (Honorary Brit in Spirit)
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
