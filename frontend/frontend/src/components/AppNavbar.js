import React from 'react';
import { Container, Nav, Navbar, Button } from 'react-bootstrap';
import './style.css';

const AppNavbar = () => {
  const sessionData = localStorage.getItem('sessionData');

  const handleLogout = () => {
    localStorage.removeItem('sessionData');
    window.location.href = '/login';
  };

  return (
    <Navbar expand="lg" className="premium-navbar" variant="dark">
      <Container>
        <Navbar.Brand href="/" className="brand-text">
          OneTrade<span className="brand-dot">AI</span>
        </Navbar.Brand>

        <Navbar.Toggle aria-controls="main-navbar" />

        <Navbar.Collapse id="main-navbar">
          <Nav className="ms-auto align-items-lg-center gap-lg-2">
            <Nav.Link href="/">Home</Nav.Link>
            <Nav.Link href="/features">Features</Nav.Link>
            <Nav.Link href="/pricing">Pricing</Nav.Link>
            <Nav.Link href="/contact">Contact</Nav.Link>

            {sessionData ? (
              <>
                <Nav.Link href="/dashboard">Dashboard</Nav.Link>
                <Nav.Link href="/profile">Profile</Nav.Link>
                <Button size="sm" className="btn-ghost" onClick={handleLogout}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Nav.Link href="/login">Login</Nav.Link>
                <Button size="sm" className="btn-premium" href="/signup">
                  Sign Up
                </Button>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default AppNavbar;