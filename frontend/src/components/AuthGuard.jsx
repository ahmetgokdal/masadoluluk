import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthGuard = ({ children }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const sessionToken = localStorage.getItem('session_token');
    if (!sessionToken) {
      navigate('/login');
    }
  }, [navigate]);

  const sessionToken = localStorage.getItem('session_token');
  if (!sessionToken) {
    return null;
  }

  return children;
};

export default AuthGuard;
