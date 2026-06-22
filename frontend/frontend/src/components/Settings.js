import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';

const Settings = () => {
  const [botSettings, setBotSettings] = useState({
    tradeStrategy: 'RSI',
    maxTradeAmount: 10000,
    stopLossPercent: 5,
    takeProfitPercent: 10,
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setBotSettings((prevState) => ({ ...prevState, [name]: value }));
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    console.log('Settings form submitted:', botSettings);
    // Add logic to update bot settings here
  };

  return (
    <div>
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <a className="navbar-brand" href="#">
          &ensp; OneTradeAI
        </a>
        <button
          className="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav">
            <li className="nav-item">
              <a className="nav-link" href="/">
                Home
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/features">
                Features
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/pricing">
                Pricing
              </a>
            </li>
            <li className="nav-item">
              <a className="nav-link" href="/contact">
                Contact
              </a>
            </li>
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdownMenuLink"
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                Profile
              </a>
              <div
                className="dropdown-menu"
                aria-labelledby="navbarDropdownMenuLink"
              >
                <a className="dropdown-item" href="/profile">
                  My Profile
                </a>
                <a className="dropdown-item" href="/settings">
                  Settings
                </a>
                <a className="dropdown-item" href="/logout">
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
            <h2 className="text-center mb-4">Settings</h2>
            <Form onSubmit={handleFormSubmit}>
              <Form.Group controlId="tradeStrategy">
                <Form.Label>Trade Strategy</Form.Label>
                <Form.Control
                  as="select"
                  name="tradeStrategy"
                  value={botSettings.tradeStrategy}
                  onChange={handleInputChange}
                >
                  <option value="RSI">RSI</option>
                  <option value="MACD">MACD</option>
                  <option value="MovingAverage">Moving Average</option>
                </Form.Control>
              </Form.Group>

              <Form.Group controlId="maxTradeAmount">
                <Form.Label>Max Trade Amount (in INR)</Form.Label>
                <Form.Control
                  type="number"
                  name="maxTradeAmount"
                  value={botSettings.maxTradeAmount}
                  onChange={handleInputChange}
                />
              </Form.Group>

              <Form.Group controlId="stopLossPercent">
                <Form.Label>Stop Loss Percent</Form.Label>
                <Form.Control
                  type="number"
                  name="stopLossPercent"
                  value={botSettings.stopLossPercent}
                  onChange={handleInputChange}
                />
              </Form.Group>

              <Form.Group controlId="takeProfitPercent">
                <Form.Label>Take Profit Percent</Form.Label>
                <Form.Control
                  type="number"
                  name="takeProfitPercent"
                  value={botSettings.takeProfitPercent}
                  onChange={handleInputChange}
                />
              </Form.Group>

              <Button variant="primary" type="submit" className="btn-block mt-4">
                Save Settings
              </Button>
            </Form>
          </Card>
        </Col>
      </Row>
    </Container>
    </div>
  );
};

export default Settings;
