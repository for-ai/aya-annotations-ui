import React from "react";

import About from "../components/About.jsx";
import Footer from "../components/Footer.jsx";
import Header from "../components/Header.jsx";
import Hero from "../components/Hero";
import HowItWorks from "../components/HowItWorks.jsx";

const Home = () => {
  return (
    <div className="overflow-x-hidden">
      <Header />
      <Hero />
      <HowItWorks />
      <About />
      <Footer />
    </div>
  );
};

export default Home;
