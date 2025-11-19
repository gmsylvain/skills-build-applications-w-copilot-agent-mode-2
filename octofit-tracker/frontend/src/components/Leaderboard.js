import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';

const Leaderboard = () => {
  return (
    <Container className="py-4">
      <Row className="mb-4">
        <Col>
          <h2>
            <i className="fas fa-trophy me-2 text-warning"></i>
            Leaderboard
          </h2>
          <p className="text-muted">See how you rank against your peers</p>
        </Col>
      </Row>

      <Row>
        <Col>
          <Card className="border-0 shadow-sm">
            <Card.Body className="text-center py-5">
              <i className="fas fa-trophy text-warning display-1 mb-4"></i>
              <h4>Competitive Rankings</h4>
              <p className="text-muted mb-4">
                Leaderboards and achievements are coming soon! Track your progress 
                and see how you stack up against other students.
              </p>
              <Button variant="warning" disabled>
                <i className="fas fa-chart-line me-2"></i>
                View Rankings
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Leaderboard;