import React, { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Alert } from 'react-bootstrap';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password1: '',
    password2: '',
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const { register, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  // Redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/dashboard');
    }
  }, [isAuthenticated, navigate]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    // Clear field error when user starts typing
    if (errors[e.target.name]) {
      setErrors({
        ...errors,
        [e.target.name]: '',
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});

    // Basic validation
    if (formData.password1 !== formData.password2) {
      setErrors({ password2: 'Passwords do not match' });
      setLoading(false);
      return;
    }

    const result = await register(
      formData.username,
      formData.email,
      formData.password1,
      formData.password2
    );
    
    if (result.success) {
      navigate('/dashboard');
    } else {
      setErrors(result.error || { detail: 'Registration failed. Please try again.' });
    }
    
    setLoading(false);
  };

  return (
    <Container className="py-5">
      <Row className="justify-content-center">
        <Col md={6} lg={5}>
          <Card className="shadow">
            <Card.Body className="p-5">
              <div className="text-center mb-4">
                <i className="fas fa-user-plus text-success" style={{ fontSize: '3rem' }}></i>
                <h2 className="mt-3 fw-bold">Join OctoFit!</h2>
                <p className="text-muted">Create your fitness tracking account</p>
              </div>

              {errors.detail && (
                <Alert variant="danger" dismissible onClose={() => setErrors({})}>
                  {errors.detail}
                </Alert>
              )}

              <Form onSubmit={handleSubmit}>
                <Form.Group className="mb-3">
                  <Form.Label>
                    <i className="fas fa-user me-2"></i>
                    Username
                  </Form.Label>
                  <Form.Control
                    type="text"
                    name="username"
                    value={formData.username}
                    onChange={handleChange}
                    required
                    placeholder="Choose a username"
                    isInvalid={!!errors.username}
                  />
                  <Form.Control.Feedback type="invalid">
                    {Array.isArray(errors.username) ? errors.username.join(' ') : errors.username}
                  </Form.Control.Feedback>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>
                    <i className="fas fa-envelope me-2"></i>
                    Email Address
                  </Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    placeholder="Enter your email"
                    isInvalid={!!errors.email}
                  />
                  <Form.Control.Feedback type="invalid">
                    {Array.isArray(errors.email) ? errors.email.join(' ') : errors.email}
                  </Form.Control.Feedback>
                </Form.Group>

                <Form.Group className="mb-3">
                  <Form.Label>
                    <i className="fas fa-lock me-2"></i>
                    Password
                  </Form.Label>
                  <Form.Control
                    type="password"
                    name="password1"
                    value={formData.password1}
                    onChange={handleChange}
                    required
                    placeholder="Create a password"
                    isInvalid={!!errors.password1}
                  />
                  <Form.Control.Feedback type="invalid">
                    {Array.isArray(errors.password1) ? errors.password1.join(' ') : errors.password1}
                  </Form.Control.Feedback>
                </Form.Group>

                <Form.Group className="mb-4">
                  <Form.Label>
                    <i className="fas fa-lock me-2"></i>
                    Confirm Password
                  </Form.Label>
                  <Form.Control
                    type="password"
                    name="password2"
                    value={formData.password2}
                    onChange={handleChange}
                    required
                    placeholder="Confirm your password"
                    isInvalid={!!errors.password2}
                  />
                  <Form.Control.Feedback type="invalid">
                    {Array.isArray(errors.password2) ? errors.password2.join(' ') : errors.password2}
                  </Form.Control.Feedback>
                </Form.Group>

                <Button
                  type="submit"
                  variant="success"
                  size="lg"
                  className="w-100 mb-3"
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2" role="status"></span>
                      Creating Account...
                    </>
                  ) : (
                    <>
                      <i className="fas fa-user-plus me-2"></i>
                      Create Account
                    </>
                  )}
                </Button>
              </Form>

              <div className="text-center">
                <p className="mb-0 text-muted">
                  Already have an account?{' '}
                  <Link to="/login" className="text-primary text-decoration-none">
                    Sign in here
                  </Link>
                </p>
              </div>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Register;