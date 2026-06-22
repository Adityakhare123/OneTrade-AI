import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';
import AppNavbar from './AppNavbar';
import './style.css';

const MyProfile = () => {
  const sessionData = localStorage.getItem('sessionData');

  let user = {};

  try {
    user = sessionData ? JSON.parse(sessionData) : {};
  } catch (error) {
    user = {};
  }

  const email =
    user.email ||
    user?.data?.email ||
    user?.user?.email ||
    'demo@onetradeai.com';

  const id =
    user.id ||
    user.userId ||
    user.user_id ||
    user?.data?.id ||
    user?.user?.id ||
    'N/A';

  return (
    <div className="app-page">
      <AppNavbar />

      <Container className="section-padding">
        <h1 className="section-title">My Profile</h1>
        <p className="section-subtitle mb-5">
          Manage your OneTradeAI account details and trading profile.
        </p>

        <Row>
          <Col lg={4} className="mb-4">
            <div className="premium-card card-padding text-center">
              <div
                style={{
                  width: 96,
                  height: 96,
                  borderRadius: '50%',
                  margin: '0 auto 18px',
                  background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
                  display: 'grid',
                  placeItems: 'center',
                  fontSize: 36,
                  fontWeight: 900,
                }}
              >
                {email.charAt(0).toUpperCase()}
              </div>

              <h3>Trader Profile</h3>
              <p className="auth-muted mb-0">{email}</p>
            </div>
          </Col>

          <Col lg={8}>
            <div className="premium-card card-padding">
              <h4>Account Information</h4>

              <div className="mt-4">
                <p className="auth-muted mb-1">User ID</p>
                <h5>{id}</h5>
              </div>

              <div className="mt-4">
                <p className="auth-muted mb-1">Email</p>
                <h5>{email}</h5>
              </div>

              <div className="mt-4">
                <p className="auth-muted mb-1">Account Type</p>
                <span className="status-pill status-active">Demo Trader</span>
              </div>

              <div className="mt-4">
                <p className="auth-muted mb-1">Project Mode</p>
                <h5>Training / Demo Application</h5>
              </div>
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default MyProfile;