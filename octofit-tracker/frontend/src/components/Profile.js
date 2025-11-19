import React from 'react';
import { Container, Row, Col, Card, Form, Button } from 'react-bootstrap';
import { useAuth } from '../contexts/AuthContext';

const Profile = () => {
  const { user } = useAuth();

  return (
    <Container className="py-4">
      <Row className="mb-4">
        <Col>
          <h2>
            <i className="fas fa-user me-2 text-info"></i>
            Profile
          </h2>
          <p className="text-muted">Manage your account and fitness preferences</p>
        </Col>
      </Row>

      <Row>
        <Col lg={8}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white">
              <h5 className="mb-0">
                <i className="fas fa-user-edit me-2"></i>
                Account Information
              </h5>
            </Card.Header>
            <Card.Body>
              <Form>
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Username</Form.Label>
                      <Form.Control
                        type="text"
                        value={user?.username || ''}
                        disabled
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Email</Form.Label>
                      <Form.Control
                        type="email"
                        value={user?.email || ''}
                        disabled
                      />
                    </Form.Group>
                  </Col>
                </Row>
                
                <Row>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>First Name</Form.Label>
                      <Form.Control
                        type="text"
                        value={user?.first_name || ''}
                        placeholder="Enter your first name"
                        disabled
                      />
                    </Form.Group>
                  </Col>
                  <Col md={6}>
                    <Form.Group className="mb-3">
                      <Form.Label>Last Name</Form.Label>
                      <Form.Control
                        type="text"
                        value={user?.last_name || ''}
                        placeholder="Enter your last name"
                        disabled
                      />
                    </Form.Group>
                  </Col>
                </Row>

                <div className="text-center">
                  <Button variant="info" disabled>
                    <i className="fas fa-save me-2"></i>
                    Save Changes
                  </Button>
                </div>
              </Form>
            </Card.Body>
          </Card>
        </Col>

        <Col lg={4}>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white">
              <h5 className="mb-0">
                <i className="fas fa-cogs me-2"></i>
                Coming Soon
              </h5>
            </Card.Header>
            <Card.Body>
              <div className="text-center py-3">
                <i className="fas fa-tools text-muted display-4 mb-3"></i>
                <p className="text-muted mb-0">
                  Profile editing, fitness goals, and preferences will be available soon!
                </p>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Profile;