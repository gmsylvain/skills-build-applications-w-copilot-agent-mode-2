import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="home-page">
      {/* Hero Section */}
      <div className="bg-primary text-white py-5">
        <Container>
          <Row className="align-items-center">
            <Col lg={6}>
              <h1 className="display-4 fw-bold">
                Welcome to OctoFit Tracker
              </h1>
              <p className="lead mb-4">
                Track your fitness journey, compete with friends, and achieve your goals 
                with Mergington High School's premier fitness tracking platform.
              </p>
              {!isAuthenticated ? (
                <div>
                  <Button as={Link} to="/register" variant="light" size="lg" className="me-3">
                    Get Started
                  </Button>
                  <Button as={Link} to="/login" variant="outline-light" size="lg">
                    Login
                  </Button>
                </div>
              ) : (
                <div>
                  <h4>Welcome back, {user?.username}!</h4>
                  <Button as={Link} to="/dashboard" variant="light" size="lg">
                    Go to Dashboard
                  </Button>
                </div>
              )}
            </Col>
            <Col lg={6} className="text-center">
              <i className="fas fa-dumbbell display-1 opacity-50"></i>
            </Col>
          </Row>
        </Container>
      </div>

      {/* Features Section */}
      <Container className="py-5">
        <Row className="text-center mb-5">
          <Col>
            <h2 className="display-5 fw-bold">Why Choose OctoFit?</h2>
            <p className="lead text-muted">
              Built specifically for Mergington High School students by Paul Octo
            </p>
          </Col>
        </Row>
        
        <Row>
          <Col md={4} className="mb-4">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body className="text-center">
                <i className="fas fa-chart-line text-primary display-4 mb-3"></i>
                <Card.Title>Track Progress</Card.Title>
                <Card.Text>
                  Log your workouts, monitor calories burned, and watch your fitness 
                  journey unfold with detailed analytics and progress tracking.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4} className="mb-4">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body className="text-center">
                <i className="fas fa-users text-success display-4 mb-3"></i>
                <Card.Title>Team Challenges</Card.Title>
                <Card.Text>
                  Join teams, participate in group challenges, and motivate each other 
                  to reach new fitness heights together.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={4} className="mb-4">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body className="text-center">
                <i className="fas fa-trophy text-warning display-4 mb-3"></i>
                <Card.Title>Leaderboards</Card.Title>
                <Card.Text>
                  Compete on various leaderboards, earn achievements, and see how you 
                  stack up against your peers in friendly competition.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>

        <Row className="mt-5">
          <Col md={6} className="mb-4">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body>
                <Card.Title>
                  <i className="fas fa-running text-info me-2"></i>
                  Activity Tracking
                </Card.Title>
                <Card.Text>
                  From running and cycling to strength training and yoga, track any type 
                  of physical activity with our comprehensive activity logging system.
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
          
          <Col md={6} className="mb-4">
            <Card className="h-100 border-0 shadow-sm">
              <Card.Body>
                <Card.Title>
                  <i className="fas fa-medal text-danger me-2"></i>
                  Achievements & Rewards
                </Card.Title>
                <Card.Text>
                  Unlock achievements as you hit milestones, maintain streaks, and 
                  complete challenges. Earn points and show off your dedication!
                </Card.Text>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>

      {/* Call to Action */}
      <div className="bg-light py-5">
        <Container>
          <Row className="text-center">
            <Col>
              <h3 className="fw-bold mb-3">Ready to Start Your Fitness Journey?</h3>
              <p className="lead text-muted mb-4">
                Join your fellow Mergington High School students and make fitness fun again!
              </p>
              {!isAuthenticated && (
                <Button as={Link} to="/register" variant="primary" size="lg">
                  Create Your Account
                </Button>
              )}
            </Col>
          </Row>
        </Container>
      </div>
    </div>
  );
};

export default Home;