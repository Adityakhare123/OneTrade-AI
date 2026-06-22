import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import AppNavbar from './AppNavbar';
import './style.css';

const Pricing = () => {
  return (
    <div className="app-page">
      <AppNavbar />

      <Container className="section-padding">
        <h1 className="section-title">Pricing</h1>
        <p className="section-subtitle mb-5">
          Demo pricing cards for presenting the project like a real SaaS trading product.
        </p>

        <Row>
          <Col md={4} className="mb-4">
            <div className="premium-card card-padding h-100">
              <h3>Starter</h3>
              <div className="price">₹0</div>
              <p className="auth-muted">For demo users and learners.</p>
              <hr />
              <p>✓ Trade tracking</p>
              <p>✓ Recent trades</p>
              <p>✓ Basic dashboard</p>
              <Button className="btn-ghost w-100" href="/signup">
                Start Free
              </Button>
            </div>
          </Col>

          <Col md={4} className="mb-4">
            <div className="premium-card card-padding h-100">
              <div className="status-pill status-active mb-3 d-inline-block">Popular</div>
              <h3>Pro</h3>
              <div className="price">₹499</div>
              <p className="auth-muted">For active trading learners.</p>
              <hr />
              <p>✓ AI prediction suggestions</p>
              <p>✓ Profit target tracking</p>
              <p>✓ Stop-loss tracking</p>
              <Button className="btn-premium w-100" href="/signup">
                Choose Pro
              </Button>
            </div>
          </Col>

          <Col md={4} className="mb-4">
            <div className="premium-card card-padding h-100">
              <h3>Enterprise</h3>
              <div className="price">Custom</div>
              <p className="auth-muted">For advanced trading teams.</p>
              <hr />
              <p>✓ Custom ML model</p>
              <p>✓ API integration</p>
              <p>✓ Advanced reporting</p>
              <Button className="btn-ghost w-100" href="/contact">
                Contact Us
              </Button>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Pricing;