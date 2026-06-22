import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import AppNavbar from './AppNavbar';
import './style.css';

const Home = () => {
  return (
    <div className="app-page">
      <AppNavbar />

      <Container className="hero-section">
        <Row className="align-items-center">
          <Col lg={7}>
            <div className="hero-badge">AI Trading Assistant</div>

            <h1 className="hero-title">
              Smarter trade tracking with <span className="gradient-text">AI signals.</span>
            </h1>

            <p className="hero-subtitle">
              OneTradeAI helps users add trades, manage profit targets, track stop-loss limits,
              and review market prediction suggestions from a Flask-based machine learning backend.
            </p>

            <div className="d-flex gap-3 mt-4 flex-wrap">
              <Button className="btn-premium" href="/signup">
                Get Started
              </Button>
              <Button className="btn-ghost" href="/features">
                Explore Features
              </Button>
            </div>
          </Col>

          <Col lg={5} className="mt-5 mt-lg-0">
            <div className="premium-card card-padding">
              <div className="d-flex justify-content-between mb-4">
                <div>
                  <div className="stat-label">Portfolio Signal</div>
                  <div className="stat-value gradient-text">Bullish</div>
                </div>
                <div className="status-pill status-active">LIVE</div>
              </div>

              <div className="premium-card p-3 mb-3">
                <div className="d-flex justify-content-between">
                  <strong>BTC-USD</strong>
                  <span className="text-success">+10.4%</span>
                </div>
                <small className="auth-muted">AI confidence: 82%</small>
              </div>

              <div className="premium-card p-3 mb-3">
                <div className="d-flex justify-content-between">
                  <strong>ETH-USD</strong>
                  <span className="text-warning">Pending</span>
                </div>
                <small className="auth-muted">Waiting for confirmation</small>
              </div>

              <div className="premium-card p-3">
                <div className="d-flex justify-content-between">
                  <strong>AAPL</strong>
                  <span className="text-danger">Stop-loss watch</span>
                </div>
                <small className="auth-muted">Risk control enabled</small>
              </div>
            </div>
          </Col>
        </Row>
      </Container>

      <Container className="section-padding">
        <Row>
          <Col md={4} className="mb-4">
            <div className="premium-card card-padding h-100">
              <div className="feature-icon">📈</div>
              <h4>Trade Tracking</h4>
              <p className="auth-muted">
                Add symbols, amount, profit target, stop-loss limit, and status.
              </p>
            </div>
          </Col>

          <Col md={4} className="mb-4">
            <div className="premium-card card-padding h-100">
              <div className="feature-icon">🤖</div>
              <h4>AI Prediction</h4>
              <p className="auth-muted">
                Uses Python, market data, RSI, and ML logic to suggest trade direction.
              </p>
            </div>
          </Col>

          <Col md={4} className="mb-4">
            <div className="premium-card card-padding h-100">
              <div className="feature-icon">🛡️</div>
              <h4>Risk Limits</h4>
              <p className="auth-muted">
                Keep trades disciplined with profit and stop-loss percentage limits.
              </p>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Home;