import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useHistory } from '@docusaurus/router';

export default function SignUp() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [softwareBackground, setSoftwareBackground] = useState('');
  const [hardwareBackground, setHardwareBackground] = useState('');
  const [error, setError] = useState('');
  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:8000/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          email,
          password,
          software_background: softwareBackground,
          hardware_background: hardwareBackground,
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Failed to sign up');
      }

      history.push('/signin');
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <Layout title="Sign Up">
      <div className="auth-container">
        <div className="auth-form-container" style={{maxWidth: '550px'}}>
          <h1>Create Your Account</h1>
          <p>Tell us about your background to personalize your learning experience.</p>
          {error && <p className="auth-error">{error}</p>}
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Software Background</label>
              <textarea
                value={softwareBackground}
                onChange={(e) => setSoftwareBackground(e.target.value)}
                placeholder="e.g., Python, C++, JavaScript, ROS, etc."
                style={{minHeight: '100px'}}
              />
            </div>
            <div className="form-group">
              <label>Hardware Background</label>
              <textarea
                value={hardwareBackground}
                onChange={(e) => setHardwareBackground(e.target.value)}
                placeholder="e.g., Arduino, Raspberry Pi, Robotics platforms, etc."
                style={{minHeight: '100px'}}
              />
            </div>
            <button type="submit" className="auth-button">
              Sign Up
            </button>
          </form>
        </div>
      </div>
    </Layout>
  );
}