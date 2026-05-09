/**
 * SYNAPSE-X Frontend
 */

import React, { useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import PredictionInterface from './components/PredictionInterface';
import HowItWorks from './components/HowItWorks';
import Features from './components/Features';
import Footer from './components/Footer';

function App() {
  useEffect(() => {
    console.log('App component mounted successfully');
  }, []);

  return (
    <div>
      <Navbar />
      <Hero />
      <PredictionInterface />
      <HowItWorks />
      <Features />
      <Footer />
    </div>
  );
}

export default App;
