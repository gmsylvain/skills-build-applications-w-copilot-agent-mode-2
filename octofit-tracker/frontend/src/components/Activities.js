import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const Activities = () => {
  return (
    <Container className="py-4">
      <Row className="mb-4">
        <Col>
          <h2>
            <i className="fas fa-running me-2 text-primary"></i>
            Activities
          </h2>
          <p className="text-muted">Track and manage your fitness activities</p>
        </Col>
      </Row>

      <Row>
        <Col>
          <Card className="border-0 shadow-sm">
            <Card.Body className="text-center py-5">
              <i className="fas fa-running text-primary display-1 mb-4"></i>
              <h4>Activity Management</h4>
              <p className="text-muted mb-4">
                This feature is coming soon! You'll be able to log workouts, 
                track your progress, and view detailed activity history.
              </p>
              <Button variant="primary" disabled>
                <i className="fas fa-plus me-2"></i>
                Log New Activity
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Activities;