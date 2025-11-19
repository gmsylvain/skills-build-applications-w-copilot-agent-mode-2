import React from 'react';
import { Navbar, Nav, Container, Button } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Navigation = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <Navbar bg="primary" variant="dark" expand="lg">
      <Container>
        <Navbar.Brand as={Link} to="/">
          <i className="fas fa-dumbbell me-2"></i>
          OctoFit Tracker
        </Navbar.Brand>
        
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
          {isAuthenticated ? (
            <>
              <Nav className="me-auto">
                <Nav.Link as={Link} to="/dashboard">
                  <i className="fas fa-tachometer-alt me-1"></i>
                  Dashboard
                </Nav.Link>
                <Nav.Link as={Link} to="/activities">
                  <i className="fas fa-running me-1"></i>
                  Activities
                </Nav.Link>
                <Nav.Link as={Link} to="/teams">
                  <i className="fas fa-users me-1"></i>
                  Teams
                </Nav.Link>
                <Nav.Link as={Link} to="/leaderboard">
                  <i className="fas fa-trophy me-1"></i>
                  Leaderboard
                </Nav.Link>
              </Nav>
              <Nav>
                <Nav.Link as={Link} to="/profile">
                  <i className="fas fa-user me-1"></i>
                  {user?.username || 'Profile'}
                </Nav.Link>
                <Button variant="outline-light" size="sm" onClick={handleLogout}>
                  <i className="fas fa-sign-out-alt me-1"></i>
                  Logout
                </Button>
              </Nav>
            </>
          ) : (
            <Nav className="ms-auto">
              <Nav.Link as={Link} to="/login">
                <i className="fas fa-sign-in-alt me-1"></i>
                Login
              </Nav.Link>
              <Nav.Link as={Link} to="/register">
                <i className="fas fa-user-plus me-1"></i>
                Register
              </Nav.Link>
            </Nav>
          )}
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
};

export default Navigation;