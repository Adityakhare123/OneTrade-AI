import React, { useState } from 'react';
import { Container, Form, Button, Alert } from 'react-bootstrap';
import axios from 'axios';
import AppNavbar from './AppNavbar';
import './style.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (event) => {
    event.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please enter email and password.');
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post('http://127.0.0.1:5000/login', {
        email,
        password,
      });

      const sessionData = response.data;

      if (sessionData) {
        localStorage.setItem('sessionData', JSON.stringify(sessionData));
        window.location.href = '/dashboard';
      } else {
        setError('Invalid email or password.');
      }
    } catch (error) {
      console.log(error);
      setError(
        error.response?.data?.message ||
          'Login failed. Please check backend server.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-page">
      <AppNavbar />

      <Container className="auth-wrapper">
        <div className="premium-card card-padding auth-card">
          <h2 className="auth-title">Welcome back</h2>
          <p className="auth-muted mb-4">
            Login to access your AI trading dashboard.
          </p>

          {error && <Alert variant="danger">{error}</Alert>}

          <Form onSubmit={handleLogin}>
            <Form.Group className="mb-3">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-4">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </Form.Group>

            <Button className="btn-premium w-100" type="submit" disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </Button>
          </Form>

          <p className="auth-muted text-center mt-4 mb-0">
            New to OneTradeAI? <a href="/signup">Create account</a>
          </p>
        </div>
      </Container>
    </div>
  );
};

export default Login;