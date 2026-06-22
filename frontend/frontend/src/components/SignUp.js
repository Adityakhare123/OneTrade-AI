import React, { useState } from 'react';
import { Container, Form, Button, Alert } from 'react-bootstrap';
import axios from 'axios';
import AppNavbar from './AppNavbar';
import './style.css';

const Signup = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [termsAccepted, setTermsAccepted] = useState(false);

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSignup = async (event) => {
    event.preventDefault();
    setError('');

    if (!email || !password || !confirmPassword) {
      setError('Please fill all fields.');
      return;
    }

    if (password !== confirmPassword) {
      setError('Password and confirm password do not match.');
      return;
    }

    if (!termsAccepted) {
      setError('Please accept the terms and conditions.');
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post('http://127.0.0.1:5000/sign_up', {
        email,
        password,
        confirm_password: confirmPassword,
      });

      const sessionData = response.data;

      if (sessionData) {
        localStorage.setItem('sessionData', JSON.stringify(sessionData));
        window.location.href = '/dashboard';
      } else {
        setError('Invalid signup input.');
      }
    } catch (error) {
      console.log(error);
      setError(
        error.response?.data?.message ||
          'Signup failed. Please check backend server.'
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
          <h2 className="auth-title">Create account</h2>
          <p className="auth-muted mb-4">
            Start tracking trades with AI-powered market insights.
          </p>

          {error && <Alert variant="danger">{error}</Alert>}

          <Form onSubmit={handleSignup}>
            <Form.Group className="mb-3">
              <Form.Label>Email address</Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Create password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Confirm password</Form.Label>
              <Form.Control
                type="password"
                placeholder="Confirm password"
                value={confirmPassword}
                onChange={(event) => setConfirmPassword(event.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-4">
              <Form.Check
                type="checkbox"
                label="I agree to the terms and conditions"
                checked={termsAccepted}
                onChange={(event) => setTermsAccepted(event.target.checked)}
              />
            </Form.Group>

            <Button className="btn-premium w-100" type="submit" disabled={loading}>
              {loading ? 'Creating account...' : 'Sign Up'}
            </Button>
          </Form>

          <p className="auth-muted text-center mt-4 mb-0">
            Already have an account? <a href="/login">Login</a>
          </p>
        </div>
      </Container>
    </div>
  );
};

export default Signup;