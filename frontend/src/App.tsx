import React, { useState, useEffect, createContext } from 'react';
import axios from 'axios';
import { Routes, Route, Link, useNavigate } from 'react-router-dom';
import Sidebar from './Sidebar';
import TaskDashboard from './TaskDashboard';
import PricingPage from './PricingPage';
import TaskHistory from './TaskHistory';
import AgentCommandCenter from './AgentCommandCenter';
import AgentLandingPage from './AgentLandingPage';
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
import UserDashboard from './UserDashboard';
import SchedulerStatusPanel from './SchedulerStatusPanel'; 
import AnalyticsDashboard from './AnalyticsDashboard'; // New import for AnalyticsDashboard

// For browsers that support webkitSpeechRecognition
declare global {
  interface Window {
    webkitSpeechRecognition: any;
  }
}

// Define AuthContext at the top level
interface AuthContextType {
  isAuthenticated: boolean;
  user: any;
  setIsAuthenticated: (isAuthenticated: boolean) => void;
  setUser: (user: any) => void;
  handleLogout: () => void;
}
export const AuthContext = createContext<AuthContextType | null>(null);

function App() {
  const [goal, setGoal] = useState('');
  const [response, setResponse] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const [tasks, setTasks] = useState<any[]>([]);
  const [scheduledJobs, setScheduledJobs] = useState<ScheduledJob[]>([]);
  const [landingPageHtml, setLandingPageHtml] = useState('');

  // Authentication state
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<any>(null); // Store user data
  const navigate = useNavigate(); // Hook for navigation

  // Fetch user data on app load if token exists
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      axios.get('http://127.0.0.1:8000/users/me/', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(res => {
        setUser(res.data);
        setIsAuthenticated(true);
      })
      .catch(() => {
        localStorage.removeItem('access_token');
        setIsAuthenticated(false);
        setUser(null);
      });
    }
    fetchLandingPageHtml(); // Fetch landing page content once
  }, []);

  // Fetch tasks and scheduled jobs only if authenticated
  useEffect(() => {
    if (isAuthenticated) {
      const token = localStorage.getItem('access_token');
      const fetchAuthenticatedData = async () => {
        try {
          const [tasksRes, scheduledJobsRes] = await Promise.all([
            axios.get('http://127.0.0.1:8000/tasks', { headers: { Authorization: `Bearer ${token}` } }),
            axios.get('http://127.0.0.1:8000/scheduler/jobs', { headers: { Authorization: `Bearer ${token}` } })
          ]);
          setTasks(Object.values(tasksRes.data));
          setScheduledJobs(scheduledJobsRes.data);
        } catch (error) {
          console.error("Failed to fetch authenticated data:", error);
          // If token is invalid, log out
          if (axios.isAxiosError(error) && error.response?.status === 401) {
            handleLogout();
          }
        }
      };

      fetchAuthenticatedData();

      const taskInterval = setInterval(fetchAuthenticatedData, 5000);
      const schedulerInterval = setInterval(fetchAuthenticatedData, 10000);

      return () => {
        clearInterval(taskInterval);
        clearInterval(schedulerInterval);
      };
    }
  }, [isAuthenticated, user]); // Re-run if isAuthenticated or user changes

  // Logout function
  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setIsAuthenticated(false);
    setUser(null);
    navigate('/login'); // Redirect to login page after logout
  };


  const fetchLandingPageHtml = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/v1/landing_page_html');
      setLandingPageHtml(res.data);
    } catch (error) {
      console.error("Failed to fetch landing page HTML:", error);
      setLandingPageHtml('<p>Error loading landing page content.</p>');
    }
  };

  const playAudio = async (text: string) => {
    try {
      const audioRes = await axios.post('http://127.0.0.1:8000/speak', 
        { text },
        { responseType: 'blob' }
      );
      const audioBlob = new Blob([audioRes.data], { type: 'audio/mpeg' });
      const audioUrl = URL.createObjectURL(audioBlob);
      new Audio(audioUrl).play();
    } catch (error) {
      console.error("Failed to play audio:", error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const isApproved = window.confirm(`Are you sure you want to submit the following goal?\n\n"${goal}"`);

    if (!isApproved) {
      const msg = 'Goal submission cancelled by user.';
      setResponse(msg);
      playAudio(msg);
      return;
    }

    try {
      const submittingMsg = 'Submitting goal to TitanForge CEO...';
      setResponse(submittingMsg);
      playAudio(submittingMsg);

      const token = localStorage.getItem('access_token');
      const res = await axios.post('http://127.0.0.1:8000/goals', { description: goal }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      const responseMessage = res.data.ceo_response || res.data.message;
      setResponse(responseMessage);
      playAudio(responseMessage);
      // fetchTasks(); // Will be triggered by useEffect
    } catch (error: any) {
      const errorMsg = `Error: ${error.response?.data?.detail || error.message}`;
      setResponse(errorMsg);
      playAudio(errorMsg);
    }
  };

  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Speech recognition not supported in this browser. Please use Chrome.');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
      setIsRecording(true);
      setGoal('Listening...');
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setGoal(transcript);
    };

    recognition.onerror = (event: any) => {
      console.error('Speech recognition error:', event.error);
      setGoal('');
    };

    recognition.onend = () => {
      setIsRecording(false);
    };

    recognition.start();
  };


  return (
    <AuthContext.Provider value={{ isAuthenticated, user, setIsAuthenticated, setUser, handleLogout }}>
        <div style={{ display: 'flex', fontFamily: 'sans-serif', minHeight: '100vh' }}>
          <Sidebar /> {/* Sidebar no longer needs currentView/onViewChange */}
          <div style={{ flexGrow: 1, padding: '20px', maxWidth: '800px', margin: 'auto' }}>
            <header style={{ textAlign: 'center', marginBottom: '40px' }}>
              <h1><Link to="/">TitanForge</Link></h1>
              <p>The Interface for Autonomous Software Engineering</p>
            </header>

            <main>
              <Routes>
                <Route path="/" element={<AgentLandingPage htmlContent={landingPageHtml} />} />
                <Route path="/pricing" element={<PricingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                
                {isAuthenticated ? (
                  <>
                    <Route path="/dashboard" element={
                      <UserDashboard
                        goal={goal}
                        setGoal={setGoal}
                        response={response}
                        setResponse={setResponse}
                        isRecording={isRecording}
                        setIsRecording={setIsRecording}
                        tasks={tasks}
                        scheduledJobs={scheduledJobs}
                        handleSubmit={handleSubmit}
                        handleVoiceInput={handleVoiceInput}
                      />
                    } />
                    <Route path="/tasks" element={<TaskHistory />} />
                    <Route path="/agents" element={<AgentCommandCenter />} />
                    {user?.is_superuser && (
                      <Route path="/analytics" element={<AnalyticsDashboard />} />
                    )}
                  </>
                ) : (
                  <Route path="/dashboard" element={<LoginPage />} /> // Redirect to login if not authenticated
                )}
                <Route path="*" element={<h1>404: Not Found</h1>} />
              </Routes>
            </main>
          </div>
        </div>
      </AuthContext.Provider>
  );
}

export default App;

