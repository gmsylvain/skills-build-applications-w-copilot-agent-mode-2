import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Badge, Spinner } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user, apiCall } = useAuth();
  const [stats, setStats] = useState(null);
  const [recentActivities, setRecentActivities] = useState([]);
  const [achievements, setAchievements] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch user stats
      const statsResponse = await apiCall('/activities/stats/?days=30');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }

      // Fetch recent activities
      const activitiesResponse = await apiCall('/activities/recent/?days=7');
      if (activitiesResponse.ok) {
        const activitiesData = await activitiesResponse.json();
        setRecentActivities(activitiesData.slice(0, 5)); // Show only last 5
      }

      // Fetch user achievements
      const achievementsResponse = await apiCall('/achievements/my_achievements/');
      if (achievementsResponse.ok) {
        const achievementsData = await achievementsResponse.json();
        setAchievements(achievementsData.slice(0, 3)); // Show only latest 3
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Container className="py-5 text-center">
        <Spinner animation="border" variant="primary" />
        <p className="mt-3">Loading your dashboard...</p>
      </Container>
    );
  }

  return (
    <Container className="py-4">
      {/* Welcome Section */}
      <Row className="mb-4">
        <Col>
          <div className="bg-gradient-primary text-white rounded p-4">
            <Row className="align-items-center">
              <Col>
                <h2 className="mb-1">Welcome back, {user?.username}! 👋</h2>
                <p className="mb-0 opacity-75">
                  Ready to crush your fitness goals today?
                </p>
              </Col>
              <Col xs="auto">
                <Button as={Link} to="/activities" variant="light" size="lg">
                  <i className="fas fa-plus me-2"></i>
                  Log Activity
                </Button>
              </Col>
            </Row>
          </div>
        </Col>
      </Row>

      {/* Stats Cards */}
      <Row className="mb-4">
        <Col md={3} className="mb-3">
          <Card className="h-100 border-0 shadow-sm">
            <Card.Body className="text-center">
              <i className="fas fa-fire text-danger display-4 mb-2"></i>
              <h4 className="fw-bold">{stats?.total_activities || 0}</h4>
              <p className="text-muted mb-0">Total Activities</p>
              <small className="text-success">
                {stats?.recent_activities || 0} this month
              </small>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3} className="mb-3">
          <Card className="h-100 border-0 shadow-sm">
            <Card.Body className="text-center">
              <i className="fas fa-clock text-primary display-4 mb-2"></i>
              <h4 className="fw-bold">{Math.round(stats?.total_duration || 0)}</h4>
              <p className="text-muted mb-0">Minutes Exercised</p>
              <small className="text-info">
                {Math.round(stats?.avg_duration || 0)} avg per session
              </small>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3} className="mb-3">
          <Card className="h-100 border-0 shadow-sm">
            <Card.Body className="text-center">
              <i className="fas fa-burn text-warning display-4 mb-2"></i>
              <h4 className="fw-bold">{stats?.total_calories || 0}</h4>
              <p className="text-muted mb-0">Calories Burned</p>
              <small className="text-warning">Keep burning! 🔥</small>
            </Card.Body>
          </Card>
        </Col>
        
        <Col md={3} className="mb-3">
          <Card className="h-100 border-0 shadow-sm">
            <Card.Body className="text-center">
              <i className="fas fa-route text-success display-4 mb-2"></i>
              <h4 className="fw-bold">{parseFloat(stats?.total_distance || 0).toFixed(1)}</h4>
              <p className="text-muted mb-0">Kilometers</p>
              <small className="text-success">Distance covered</small>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row>
        {/* Recent Activities */}
        <Col lg={6} className="mb-4">
          <Card className="h-100 shadow-sm">
            <Card.Header className="bg-white border-bottom-0 d-flex justify-content-between align-items-center">
              <h5 className="mb-0">
                <i className="fas fa-history text-primary me-2"></i>
                Recent Activities
              </h5>
              <Button as={Link} to="/activities" variant="outline-primary" size="sm">
                View All
              </Button>
            </Card.Header>
            <Card.Body>
              {recentActivities.length > 0 ? (
                recentActivities.map((activity) => (
                  <div key={activity.id} className="d-flex align-items-center mb-3 p-3 bg-light rounded">
                    <div className="flex-shrink-0 me-3">
                      <div className="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center" style={{ width: '40px', height: '40px' }}>
                        <i className="fas fa-running"></i>
                      </div>
                    </div>
                    <div className="flex-grow-1">
                      <h6 className="mb-1">{activity.name}</h6>
                      <small className="text-muted">
                        {activity.duration_minutes} min • {activity.calories_burned} cal
                        {activity.distance_km && ` • ${activity.distance_km}km`}
                      </small>
                    </div>
                    <Badge bg="success">{activity.points_earned} pts</Badge>
                  </div>
                ))
              ) : (
                <div className="text-center py-4">
                  <i className="fas fa-running text-muted display-3 mb-3"></i>
                  <p className="text-muted">No activities logged yet.</p>
                  <Button as={Link} to="/activities" variant="primary">
                    Log Your First Activity
                  </Button>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>

        {/* Recent Achievements */}
        <Col lg={6} className="mb-4">
          <Card className="h-100 shadow-sm">
            <Card.Header className="bg-white border-bottom-0 d-flex justify-content-between align-items-center">
              <h5 className="mb-0">
                <i className="fas fa-trophy text-warning me-2"></i>
                Recent Achievements
              </h5>
              <Button as={Link} to="/leaderboard" variant="outline-warning" size="sm">
                View All
              </Button>
            </Card.Header>
            <Card.Body>
              {achievements.length > 0 ? (
                achievements.map((userAchievement) => (
                  <div key={userAchievement.id} className="d-flex align-items-center mb-3 p-3 bg-light rounded">
                    <div className="flex-shrink-0 me-3">
                      <div className="bg-warning text-white rounded-circle d-flex align-items-center justify-content-center" style={{ width: '40px', height: '40px' }}>
                        <i className={userAchievement.achievement.badge_icon || 'fas fa-medal'}></i>
                      </div>
                    </div>
                    <div className="flex-grow-1">
                      <h6 className="mb-1">{userAchievement.achievement.name}</h6>
                      <small className="text-muted">
                        {userAchievement.achievement.description}
                      </small>
                    </div>
                    <Badge bg="warning">{userAchievement.achievement.points_reward} pts</Badge>
                  </div>
                ))
              ) : (
                <div className="text-center py-4">
                  <i className="fas fa-medal text-muted display-3 mb-3"></i>
                  <p className="text-muted">No achievements unlocked yet.</p>
                  <p className="small text-muted">
                    Complete activities to start earning achievements!
                  </p>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>

      {/* Quick Actions */}
      <Row>
        <Col>
          <Card className="border-0 shadow-sm">
            <Card.Header className="bg-white">
              <h5 className="mb-0">
                <i className="fas fa-bolt text-primary me-2"></i>
                Quick Actions
              </h5>
            </Card.Header>
            <Card.Body>
              <Row>
                <Col sm={6} md={3} className="mb-2">
                  <Button as={Link} to="/activities" variant="outline-primary" className="w-100">
                    <i className="fas fa-plus me-2"></i>
                    Log Activity
                  </Button>
                </Col>
                <Col sm={6} md={3} className="mb-2">
                  <Button as={Link} to="/teams" variant="outline-success" className="w-100">
                    <i className="fas fa-users me-2"></i>
                    Join Team
                  </Button>
                </Col>
                <Col sm={6} md={3} className="mb-2">
                  <Button as={Link} to="/leaderboard" variant="outline-warning" className="w-100">
                    <i className="fas fa-trophy me-2"></i>
                    View Rankings
                  </Button>
                </Col>
                <Col sm={6} md={3} className="mb-2">
                  <Button as={Link} to="/profile" variant="outline-info" className="w-100">
                    <i className="fas fa-user me-2"></i>
                    Edit Profile
                  </Button>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default Dashboard;