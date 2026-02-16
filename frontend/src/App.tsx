import React, { useState, useEffect, createContext } from "react";
import axios from "axios";
import { Routes, Route, Link, useNavigate, Navigate, useLocation } from "react-router-dom";

import Sidebar from "./Sidebar";
import TaskDashboard from "./TaskDashboard";
import PricingPage from "./PricingPage";
import TaskHistory from "./TaskHistory";
import AgentCommandCenter from "./AgentCommandCenter";
import AgentCockpitPro from "./AgentCockpitPro";
import RealmForgeLandingPage from "./RealmForgeLandingPage";
import LandingPagePro from "./LandingPagePro";
import LandingPageProPro from "./LandingPageProPro";
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import UserDashboard from "./UserDashboard";
import SchedulerStatusPanel from "./SchedulerStatusPanel";
import ChambersContainer from "./ChambersContainer";
import AnalyticsDashboard from "./AnalyticsDashboard";
import PrivacyPage from "./PrivacyPage";
import TermsPage from "./TermsPage";
import DataSalePage from "./DataSalePage";
import CheckoutPage from "./CheckoutPage";

import type { ScheduledJob, User } from "@/types/index";
import { SwarmProvider } from "@/contexts/SwarmContext";
import { authAPI, taskAPI, schedulerAPI, messageAPI } from "@/services/api";

// ---------------- TYPES & INTERFACES ----------------

declare global {
  interface Window {
    webkitSpeechRecognition: any;
  }
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  setIsAuthenticated: (isAuthenticated: boolean) => void;
  setUser: (user: User | null) => void;
  handleLogout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

// ---------------- PROTECTED ROUTE WRAPPER ----------------

const ProtectedRoute = ({
  children,
  isAuthenticated,
  adminOnly = false,
  user
}: {
  children: JSX.Element;
  isAuthenticated: boolean;
  adminOnly?: boolean;
  user?: User | null;
}) => {
  const location = useLocation();

  if (!isAuthenticated) {
    // If not logged in, redirect to login but save where they wanted to go
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (adminOnly && !user?.is_superuser) {
    // If logged in but not an admin, send them to dashboard
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// ---------------- MAIN APP ----------------

function App() {
  const [goal, setGoal] = useState("");
  const [response, setResponse] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const [tasks, setTasks] = useState<any[]>([]);
  const [scheduledJobs, setScheduledJobs] = useState<ScheduledJob[]>([]);

  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  const navigate = useNavigate();

  // ---------------- AUTH CHECK ----------------

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (token) {
      authAPI
        .getCurrentUser()
        .then((userData) => {
          setUser(userData);
          setIsAuthenticated(true);
        })
        .catch(() => {
          localStorage.removeItem("access_token");
          setIsAuthenticated(false);
          setUser(null);
        });
    }
  }, []);

  // ---------------- DATA POLLING ----------------

  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchAuthenticatedData = async () => {
      try {
        const [tasksList, jobsList] = await Promise.all([
          taskAPI.getTasks(),
          schedulerAPI.getJobs(),
        ]);
        setTasks(tasksList);
        setScheduledJobs(jobsList);
      } catch (error) {
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
  }, [isAuthenticated]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
    setUser(null);
    navigate("/login");
  };

  const playAudio = async (text: string) => {
    try {
      const audioBlob = await messageAPI.textToSpeech(text);
      const audioUrl = URL.createObjectURL(audioBlob);
      new Audio(audioUrl).play();
    } catch (error) { console.error(error); }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!window.confirm(`Submit goal: "${goal}"?`)) return;

    try {
      playAudio("Submitting goal...");
      const task = await taskAPI.submitGoal(goal);
      setResponse(`Goal submitted: ${task.id}`);
      setGoal("");
    } catch (error: any) {
      setResponse(`Error: ${error.detail || error.message}`);
    }
  };

  const handleVoiceInput = () => {
    if (!("webkitSpeechRecognition" in window)) return;
    const recognition = new window.webkitSpeechRecognition();
    recognition.onstart = () => { setIsRecording(true); setGoal("Listening..."); };
    recognition.onresult = (event: any) => setGoal(event.results[0][0].transcript);
    recognition.onend = () => setIsRecording(false);
    recognition.start();
  };

  return (
    <SwarmProvider autoRefreshInterval={30000}>
      <AuthContext.Provider value={{ isAuthenticated, user, setIsAuthenticated, setUser, handleLogout }}>
        <div style={{ display: "flex", fontFamily: "sans-serif", minHeight: "100vh" }}>
          
          {isAuthenticated && <Sidebar isAuthenticated={isAuthenticated} handleLogout={handleLogout} />}

          <div style={{ flexGrow: 1, padding: "20px", maxWidth: "1200px", margin: "auto" }}>
            <header style={{ textAlign: "center", marginBottom: "40px" }}>
              <h1><Link to="/">TitanForge</Link></h1>
              <p>The Interface for Autonomous Software Engineering</p>
            </header>

            <main>
              <Routes>
                {/* --- PUBLIC ROUTES --- */}
                <Route path="/" element={<LandingPageProPro />} />
                <Route path="/legacy-landing" element={<LandingPagePro />} />
                <Route path="/pricing" element={<PricingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/checkout" element={<CheckoutPage />} />
                <Route path="/privacy" element={<PrivacyPage />} />
                <Route path="/terms" element={<TermsPage />} />
                <Route path="/data-sale" element={<DataSalePage />} />

                {/* --- PROTECTED ROUTES (One-to-one mapping) --- */}
                <Route path="/cockpit" element={
                  <ProtectedRoute isAuthenticated={isAuthenticated}>
                    <AgentCockpitPro />
                  </ProtectedRoute>
                } />

                <Route path="/dashboard" element={
                  <ProtectedRoute isAuthenticated={isAuthenticated}>
                    <UserDashboard
                      goal={goal} setGoal={setGoal}
                      response={response} setResponse={setResponse}
                      isRecording={isRecording} setIsRecording={setIsRecording}
                      tasks={tasks} scheduledJobs={scheduledJobs}
                      handleSubmit={handleSubmit} handleVoiceInput={handleVoiceInput}
                    />
                  </ProtectedRoute>
                } />

                <Route path="/tasks" element={
                  <ProtectedRoute isAuthenticated={isAuthenticated}>
                    <TaskHistory />
                  </ProtectedRoute>
                } />

                <Route path="/chambers/*" element={
                  <ProtectedRoute isAuthenticated={isAuthenticated}>
                    <ChambersContainer />
                  </ProtectedRoute>
                } />

                {/* --- ADMIN ROUTES --- */}
                <Route path="/analytics" element={
                  <ProtectedRoute isAuthenticated={isAuthenticated} adminOnly={true} user={user}>
                    <AnalyticsDashboard />
                  </ProtectedRoute>
                } />

                {/* --- CATCH-ALL (True 404) --- */}
                <Route path="*" element={
                  <div style={{ textAlign: 'center', marginTop: '50px' }}>
                    <h1>404: Page Not Found</h1>
                    <p>The forge couldn't find this route.</p>
                    <Link to="/">Return Home</Link>
                  </div>
                } />
              </Routes>
            </main>
          </div>
        </div>
      </AuthContext.Provider>
    </SwarmProvider>
  );
}

export default App;