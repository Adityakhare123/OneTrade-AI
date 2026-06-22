import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import AppNavbar from './AppNavbar';
import './style.css';

const Features = () => {
  const features = [
    {
      icon: '📊',
      title: 'Recent Trade History',
      desc: 'View all recent trades with symbol, amount, profit target, status, and time.',
    },
    {
      icon: '🤖',
      title: 'AI Market Prediction',
      desc: 'Backend prediction logic uses Python, TensorFlow, yfinance, RSI, and market data.',
    },
    {
      icon: '🔐',
      title: 'Login & Signup',
      desc: 'Users can create an account, login, and access their own trading dashboard.',
    },
    {
      icon: '🎯',
      title: 'Profit Target',
      desc: 'Add profit percentage limits to track expected trade outcomes.',
    },
    {
      icon: '🛡️',
      title: 'Stop Loss Control',
      desc: 'Protect trades by defining stop-loss percentage levels.',
    },
    {
      icon: '⚡',
      title: 'Flask API Backend',
      desc: 'React frontend connects with Flask REST APIs and SQLite database.',
    },
  ];

  return (
    <div className="app-page">
      <AppNavbar />

      <Container className="section-padding">
        <h1 className="section-title">Features</h1>
        <p className="section-subtitle mb-5">
          OneTradeAI combines a React dashboard, Flask APIs, SQLite storage,
          and ML-based prediction logic into one trading demo application.
        </p>

        <Row>
          {features.map((feature, index) => (
            <Col md={4} className="mb-4" key={index}>
              <div className="premium-card card-padding h-100">
                <div className="feature-icon">{feature.icon}</div>
                <h4>{feature.title}</h4>
                <p className="auth-muted">{feature.desc}</p>
              </div>
            </Col>
          ))}
        </Row>
      </Container>
    </div>
  );
};

export default Features;