import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate, useLocation } from 'react-router-dom';

function Verify() {
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    const location = useLocation();

    useEffect(() => {
        if (location.state?.email) {
            setEmail(location.state.email);
        }
    }, [location.state]);

    const handleVerify = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/verify', {
                email,
                otp,
            });
            setMessage(response.data.message);
            setError('');
            setTimeout(() => navigate('/login'), 2000);
        } catch (err) {
            setError(err.response?.data?.detail || 'Verification failed');
            setMessage('');
        }
    };

    return (
        <div className="auth-container">
            <h2>Verify Account</h2>
            {message && <p className="success" style={{ color: '#4caf50' }}>{message}</p>}
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleVerify}>
                <div>
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div>
                    <label>OTP Code:</label>
                    <input
                        type="text"
                        value={otp}
                        onChange={(e) => setOtp(e.target.value)}
                        placeholder="Enter 6-digit code"
                        required
                    />
                </div>
                <button type="submit">Verify</button>
            </form>
        </div>
    );
}

export default Verify;
