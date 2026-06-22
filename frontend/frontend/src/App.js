import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route} from 'react-router-dom';
import { Routes } from 'react-router-dom';
import Home from './components/Home';
import Features from './components/Features';
import Pricing from './components/Pricing';
import Contact from './components/Contact';
import SignUp from './components/SignUp';
import Login from './components/Login';
import Landing from './components/Landing';
import Dashboard from './components/Dashboard';
import MyProfile from './components/MyProfile';
import Settings from './components/Settings';

function App() {
  return (
    <Router>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/features" element={<Features />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route path="/landing" element={<Landing />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<MyProfile />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
