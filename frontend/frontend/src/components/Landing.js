import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const Landing = () => {
  return (
    <div
      style={{
        backgroundImage: `url(${'https://source.unsplash.com/random/?trading'})`,
        backgroundSize: 'cover',
        minHeight: '100vh',
      }}
    >
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="#">
          &ensp; OneTradeAI
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/">
                Home
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/features">
                Features
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/pricing">
                Pricing
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/contact">
                Contact
              </a>
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdownMenuLink"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                Profile
              </a>
              <div
                class="dropdown-menu"
                aria-labelledby="navbarDropdownMenuLink"
              >
                <a class="dropdown-item" href="/profile">
                  My Profile
                </a>
                <a class="dropdown-item" href="/settings">
                  Settings
                </a>
                <a class="dropdown-item" href="/logout">
                  Logout
                </a>
              </div>
            </li>
          </ul>
        </div>
      </nav>
      <Container className="py-5">
        <Row className="justify-content-center">
          <Col lg={6}>
            <Card className="bg-white rounded p-4 shadow-sm">
              <h2 className="text-center mb-4">Welcome to OneTradeAI!</h2>
              <p>
                Congratulations! You have successfully logged in to our platform.
                OneTradeAI is the most advanced trading bot that uses machine learning algorithms
                to predict market trends and make profitable trades for you.
              </p>
              <p>
                To get started, navigate to the "Dashboard" section and configure your trading settings.
                Once you are done, sit back and relax as our bot does the rest for you.
              </p>
              <Button variant="primary" className="btn-block mt-4" href="/dashboard">
                Go to Dashboard
              </Button>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default Landing;
