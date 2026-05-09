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
import { healthCheck } from './services/apiService';

function App() {
  useEffect(() => {
    console.log('App component mounted successfully');
    
    // Ping backend immediately on load to wake it up if it was sleeping
    healthCheck().catch(err => console.log('Warmup ping failed (expected if sleeping):', err.message));

    // Ping the backend every 10 minutes (600000 ms) to keep it awake
    // NOTE: This only works while a user has this website open in their browser!
    const pingInterval = setInterval(() => {
      console.log('Sending keep-alive ping to backend...');
      healthCheck().catch(console.error);
    }, 10 * 60 * 1000);

    return () => clearInterval(pingInterval);
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
