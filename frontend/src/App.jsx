import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './Login';
import Signup from './Signup';
import './App.css';

function Dashboard() {
  return (
    <div className="dashboard">
      <h1>Welcome to Dashboard</h1>
      <p>You are logged in!</p>
      <button onClick={() => window.location.href = '/login'}>Logout</button>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="app-container">
        <h1>Sandpyth Auth</h1>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
