'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

// Updated interfaces for The Bibliotherapist 2.0
interface Dosage {
  frequency: string;
  duration: string;
  method: string;
}

interface Quote {
  text: string;
  author: string;
  work: string;
  context: string;
  diagnosis: string;
  literary_analysis: string;
  modern_interpretation: string;
  punch_line: string;
  dosage: Dosage;
}

interface SubCategory {
  id: string;
  label: string;
  question: string;
  quotes: Quote[];
}

interface Emotion {
  id: string;
  label: string;
  description: string;
  sub_categories: SubCategory[];
}

interface QuotesData {
  meta: {
    version: string;
    physician: string;
    established: string;
    location: string;
  };
  emotions: Emotion[];
}

type Stage = 'intro' | 'subquestion' | 'loading' | 'prescription';

export default function BibliotherapistPage() {
  const [stage, setStage] = useState<Stage>('intro');
  const [selectedEmotion, setSelectedEmotion] = useState<Emotion | null>(null);
  const [selectedSubCategory, setSelectedSubCategory] = useState<SubCategory | null>(null);
  const [currentQuote, setCurrentQuote] = useState<Quote | null>(null);
  const [quotesData, setQuotesData] = useState<QuotesData | null>(null);
  const [patientNumber] = useState<number>(Math.floor(Math.random() * 9999) + 1000);

  // Load quotes data
  useEffect(() => {
    fetch('/quotes-complete.json')
      .then((res) => res.json())
      .then((data: QuotesData) => {
        console.log('Loaded quotes data:', data);
        setQuotesData(data);
      })
      .catch((err) => console.error('Failed to load quotes:', err));
  }, []);

  const handleEmotionSelect = (emotion: Emotion) => {
    setSelectedEmotion(emotion);
    setStage('subquestion');
  };

  const handleSubCategorySelect = (subCategory: SubCategory) => {
    setSelectedSubCategory(subCategory);
    setStage('loading');

    // Random quote from selected subcategory
    const randomQuote = subCategory.quotes[Math.floor(Math.random() * subCategory.quotes.length)];

    // Show loading for 2.5 seconds
    setTimeout(() => {
      setCurrentQuote(randomQuote);
      setStage('prescription');
    }, 2500);
  };

  const handleAnotherDose = () => {
    if (selectedSubCategory) {
      setStage('loading');
      const randomQuote = selectedSubCategory.quotes[Math.floor(Math.random() * selectedSubCategory.quotes.length)];
      setTimeout(() => {
        setCurrentQuote(randomQuote);
        setStage('prescription');
      }, 2500);
    }
  };

  const handleReset = () => {
    setStage('intro');
    setSelectedEmotion(null);
    setSelectedSubCategory(null);
    setCurrentQuote(null);
  };

  const getCurrentDate = () => {
    return new Date().toLocaleDateString('en-GB', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
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
            className="max-w-4xl w-full text-center space-y-8"
          >
            {/* Title */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
            >
              <div className="border-t border-b border-gold/30 py-4 mb-4">
                <h1 className="font-playfair text-5xl md:text-7xl font-bold text-gold mb-2">
                  THE BIBLIOTHERAPIST
                </h1>
                <p className="font-courier text-cream/70 text-xs tracking-widest uppercase">
                  Est. {quotesData.meta.established} — {quotesData.meta.location}
                </p>
              </div>
            </motion.div>

            {/* Dr. Pemberton Introduction */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="space-y-4 max-w-2xl mx-auto"
            >
              <p className="font-courier text-lg text-cream/90">
                {quotesData.meta.physician}, Literary Physician
              </p>
              <p className="font-courier text-sm text-cream/70 leading-relaxed">
                Curing souls with words since the Victorian era
              </p>
              <div className="border-l-2 border-gold/50 pl-6 text-left space-y-3">
                <p className="font-courier text-sm text-cream/80 leading-relaxed">
                  I've been practicing literary medicine for {new Date().getFullYear() - parseInt(quotesData.meta.established)} years.
                  In that time, I've learned three truths: suffering is universal, literature is eternal,
                  and modern humans are remarkably unoriginal in their misery.
                </p>
                <p className="font-courier text-sm text-cream/80 leading-relaxed">
                  No pills. No platitudes. No positive thinking.<br />
                  Just British literature and a healthy dose of cynicism.
                </p>
              </div>
            </motion.div>

            {/* Usage Guide */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.6 }}
              className="border-t border-b border-gold/20 py-6"
            >
              <p className="font-courier text-xs text-gold tracking-widest uppercase mb-4">How It Works</p>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-left max-w-3xl mx-auto">
                <div className="space-y-1">
                  <p className="font-courier text-xs text-gold">Step 1</p>
                  <p className="font-courier text-xs text-cream/70">Choose your affliction</p>
                </div>
                <div className="space-y-1">
                  <p className="font-courier text-xs text-gold">Step 2</p>
                  <p className="font-courier text-xs text-cream/70">Answer one question</p>
                </div>
                <div className="space-y-1">
                  <p className="font-courier text-xs text-gold">Step 3</p>
                  <p className="font-courier text-xs text-cream/70">Receive prescription</p>
                </div>
                <div className="space-y-1">
                  <p className="font-courier text-xs text-gold">Step 4</p>
                  <p className="font-courier text-xs text-cream/70">Take the medicine</p>
                </div>
              </div>
            </motion.div>

            {/* Main Question */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.8, duration: 0.6 }}
              className="space-y-2"
            >
              <p className="font-playfair text-2xl md:text-3xl italic text-cream/90">
                "What is haunting your soul today?"
              </p>
              <p className="font-courier text-xs text-cream/50">(Choose honestly. I've seen it all.)</p>
            </motion.div>

            {/* Emotion Tags */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 1, duration: 0.6 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-3 max-w-2xl mx-auto pt-4"
            >
              {quotesData.emotions.map((emotion, index) => (
                <motion.button
                  key={emotion.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 1.1 + index * 0.1 }}
                  whileHover={{ scale: 1.05, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleEmotionSelect(emotion)}
                  className="px-5 py-3 border border-gold/30 hover:border-gold bg-charcoal/50 hover:bg-gold/10 transition-all duration-300 font-courier text-xs tracking-wider uppercase relative overflow-hidden group"
                >
                  <span className="relative z-10 text-cream">{emotion.label}</span>
                </motion.button>
              ))}
            </motion.div>

            {/* Footer quote */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.5, duration: 0.6 }}
              className="pt-8 border-t border-gold/10"
            >
              <p className="font-courier text-xs text-cream/40 italic">
                "The good ended happily, and the bad unhappily. That is what Fiction means."
                <br />— Oscar Wilde
              </p>
            </motion.div>
          </motion.div>
        )}

        {/* STAGE 2: SUB-QUESTION */}
        {stage === 'subquestion' && selectedEmotion && (
          <motion.div
            key="subquestion"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl w-full space-y-8"
          >
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-center border-b border-gold/20 pb-6"
            >
              <p className="font-courier text-xs text-gold tracking-widest uppercase mb-2">Diagnostic Clarification</p>
              <h2 className="font-playfair text-3xl md:text-4xl text-cream mb-4">
                You've selected: {selectedEmotion.label}
              </h2>
              <p className="font-courier text-sm text-cream/70 max-w-xl mx-auto leading-relaxed">
                {selectedEmotion.description}
              </p>
            </motion.div>

            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="space-y-6"
            >
              <p className="font-playfair text-xl md:text-2xl text-cream/90 text-center italic">
                Let's narrow this down...
              </p>

              <div className="space-y-3">
                {selectedEmotion.sub_categories.map((subCat, index) => (
                  <motion.button
                    key={subCat.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.6 + index * 0.1 }}
                    whileHover={{ scale: 1.02, x: 4 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={() => handleSubCategorySelect(subCat)}
                    className="w-full text-left px-6 py-4 border border-gold/30 hover:border-gold bg-charcoal/50 hover:bg-gold/10 transition-all duration-300"
                  >
                    <p className="font-courier text-sm text-cream leading-relaxed">
                      {subCat.label}
                    </p>
                  </motion.button>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1, duration: 0.6 }}
              className="text-center pt-4"
            >
              <button
                onClick={handleReset}
                className="font-courier text-xs text-cream/50 hover:text-cream transition-colors"
              >
                ← Back to afflictions
              </button>
            </motion.div>
          </motion.div>
        )}

        {/* STAGE 3: LOADING */}
        {stage === 'loading' && (
          <motion.div
            key="loading"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.6 }}
            className="text-center space-y-8"
          >
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

            <motion.div className="space-y-2">
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
                className="font-courier text-xl text-cream"
              >
                Consulting the archives of British literature...
              </motion.p>
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: '200px' }}
                transition={{ duration: 2, ease: 'easeInOut' }}
                className="h-0.5 bg-gold/50 mx-auto"
              />
            </motion.div>
          </motion.div>
        )}

        {/* STAGE 4: PRESCRIPTION */}
        {stage === 'prescription' && currentQuote && (
          <motion.div
            key="prescription"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.8 }}
            className="max-w-4xl w-full space-y-8"
          >
            {/* Prescription Header */}
            <motion.div
              initial={{ y: -20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-center border-t border-b border-gold/30 py-6"
            >
              <h2 className="font-playfair text-4xl md:text-5xl text-gold mb-4">
                ℞ Literary Prescription
              </h2>
              <div className="font-courier text-xs text-cream/60 space-y-1">
                <p>Date: {getCurrentDate()}</p>
                <p>Patient: Anonymous Soul №{patientNumber}</p>
                <p>Physician: {quotesData.meta.physician}</p>
              </div>
            </motion.div>

            {/* Diagnosis */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.4, duration: 0.6 }}
              className="border border-gold/30 p-4 text-center"
            >
              <p className="font-courier text-xs text-gold tracking-wider uppercase mb-2">Diagnosis</p>
              <p className="font-courier text-sm text-cream">{currentQuote.diagnosis}</p>
            </motion.div>

            {/* The Prescription (Quote) */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.8 }}
              className="border-t border-b border-gold/20 py-8"
            >
              <p className="font-courier text-xs text-gold tracking-wider uppercase text-center mb-6">
                The Prescription
              </p>
              <blockquote className="font-playfair text-2xl md:text-3xl italic text-cream leading-relaxed text-center mb-6 px-4">
                "{currentQuote.text}"
              </blockquote>
              <div className="text-center font-courier text-sm text-cream/80 space-y-1">
                <p className="font-bold">— {currentQuote.author}</p>
                <p className="italic text-cream/60">{currentQuote.work}</p>
              </div>
            </motion.div>

            {/* Dr. Pemberton's Notes */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 0.8, duration: 0.6 }}
              className="border-l-4 border-gold/50 pl-6 space-y-4"
            >
              <p className="font-courier text-xs text-gold tracking-wider uppercase">
                📖 Dr. Pemberton's Notes
              </p>

              <div className="space-y-3 font-courier text-sm text-cream/80 leading-relaxed">
                <p className="text-xs text-cream/60 italic">{currentQuote.context}</p>
                <p>{currentQuote.literary_analysis}</p>
                <p className="text-cream/90">{currentQuote.modern_interpretation}</p>
              </div>
            </motion.div>

            {/* Modern Translation (Punch Line) */}
            <motion.div
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 1, duration: 0.6 }}
              className="border border-gold/30 p-6 bg-deep-brown/20"
            >
              <p className="font-courier text-xs text-gold tracking-wider uppercase mb-3">
                ⚠ Modern Translation
              </p>
              <p className="font-courier text-base md:text-lg text-cream/90 leading-relaxed">
                {currentQuote.punch_line}
              </p>
            </motion.div>

            {/* Dosage & Instructions */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 1.2, duration: 0.6 }}
              className="border-t border-gold/20 pt-6"
            >
              <p className="font-courier text-xs text-gold tracking-wider uppercase mb-4">
                💊 Dosage & Instructions
              </p>
              <div className="font-courier text-sm text-cream/80 space-y-2 leading-relaxed">
                <p><span className="text-gold">Frequency:</span> {currentQuote.dosage.frequency}</p>
                <p><span className="text-gold">Duration:</span> {currentQuote.dosage.duration}</p>
                <p><span className="text-gold">Method:</span> {currentQuote.dosage.method}</p>
              </div>
            </motion.div>

            {/* Action Buttons */}
            <motion.div
              initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              transition={{ delay: 1.4, duration: 0.6 }}
              className="flex flex-col sm:flex-row gap-3 justify-center pt-6 border-t border-gold/10"
            >
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleAnotherDose}
                className="px-8 py-3 border border-gold/50 hover:border-gold bg-charcoal hover:bg-gold/10 transition-all duration-300 font-courier text-xs tracking-wider uppercase"
              >
                Another Dose
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleReset}
                className="px-8 py-3 bg-gold hover:bg-faded-gold text-charcoal transition-all duration-300 font-courier text-xs tracking-wider uppercase font-bold"
              >
                New Diagnosis
              </motion.button>
            </motion.div>

            {/* Footer */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.6, duration: 0.6 }}
              className="text-center pt-6 border-t border-gold/10"
            >
              <p className="font-courier text-xs text-cream/40 italic">
                "There is no greater agony than bearing an untold story inside you."
                <br />— Maya Angelou
              </p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
