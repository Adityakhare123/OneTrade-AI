import React, { useState } from 'react';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';
import AppNavbar from './AppNavbar';
import './style.css';

const Contact = () => {
  const [sent, setSent] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setSent(true);
  };

  return (
    <div className="app-page">
      <AppNavbar />

      <Container className="section-padding">
        <Row className="align-items-center">
          <Col lg={5} className="mb-4">
            <h1 className="section-title">Contact Us</h1>
            <p className="section-subtitle">
              Have questions about OneTradeAI, API flow, prediction logic, or dashboard usage?
              Send a message using this demo contact form.
            </p>

            <div className="premium-card card-padding mt-4">
              <h5>Project Stack</h5>
              <p className="auth-muted mb-1">Frontend: React + Bootstrap</p>
              <p className="auth-muted mb-1">Backend: Flask + SQLAlchemy</p>
              <p className="auth-muted mb-0">ML: TensorFlow + yfinance + TA-Lib</p>
            </div>
          </Col>

          <Col lg={7}>
            <div className="premium-card card-padding">
              {sent && <Alert variant="success">Message submitted successfully.</Alert>}

              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>Your Name</Form.Label>
                  <Form.Control type="text" placeholder="Enter your name" />
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>Email</Form.Label>
                  <Form.Control type="email" placeholder="Enter your email" />
                </Form.Group>

                <Form.Group className="mb-4">
                  <Form.Label>Message</Form.Label>
                  <Form.Control as="textarea" rows={5} placeholder="Write your message" />
                </Form.Group>

                <Button className="btn-premium" type="submit">
                  Send Message
                </Button>
              </Form>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Contact;