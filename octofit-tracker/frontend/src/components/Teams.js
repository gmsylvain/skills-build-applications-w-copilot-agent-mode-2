import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const Teams = () => {
  return (
    <Container className="py-4">
      <Row className="mb-4">
        <Col>
          <h2>
            <i className="fas fa-users me-2 text-success"></i>
            Teams
          </h2>
          <p className="text-muted">Join teams and participate in group challenges</p>
        </Col>
      </Row>

      <Row>
        <Col>
          <Card className="border-0 shadow-sm">
            <Card.Body className="text-center py-5">
              <i className="fas fa-users text-success display-1 mb-4"></i>
              <h4>Team Features</h4>
              <p className="text-muted mb-4">
                Team functionality is coming soon! You'll be able to create teams, 
                join challenges, and compete with your classmates.
              </p>
              <Button variant="success" disabled>
                <i className="fas fa-plus me-2"></i>
                Create Team
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Teams;