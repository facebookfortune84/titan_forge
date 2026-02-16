import React, { useState, useEffect, createContext } from "react";
import axios from "axios";
import { Routes, Route, Link, useNavigate } from "react-router-dom";

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

import type { ScheduledJob, User } from "@/types/index";
import { SwarmProvider } from "@/contexts/SwarmContext";
import { authAPI, taskAPI, schedulerAPI, messageAPI } from "@/services/api";

// For browsers that support webkitSpeechRecognition
declare global {
  interface Window {
    webkitSpeechRecognition: any;
  }
}

// ---------------- AUTH CONTEXT ----------------

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  setIsAuthenticated: (isAuthenticated: boolean) => void;
  setUser: (user: User | null) => void;
  handleLogout: () => void;
}

export const AuthContext = createContext<AuthContextType | null>(null);

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

  // ---------------- FETCH AUTH DATA ----------------

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
        console.error("Failed to fetch authenticated data:", error);

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
  }, [isAuthenticated, user]);

  // ---------------- LOGOUT ----------------

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
    setUser(null);
    navigate("/login");
  };

  // ---------------- AUDIO ----------------

  const playAudio = async (text: string) => {
    try {
      const audioBlob = await messageAPI.textToSpeech(text);
      const audioUrl = URL.createObjectURL(audioBlob);
      new Audio(audioUrl).play();
    } catch (error) {
      console.error("Failed to play audio:", error);
    }
  };

  // ---------------- GOAL SUBMISSION ----------------

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const isApproved = window.confirm(
      `Are you sure you want to submit the following goal?\n\n"${goal}"`
    );

    if (!isApproved) {
      const msg = "Goal submission cancelled by user.";
      setResponse(msg);
      playAudio(msg);
      return;
    }

    try {
      const submittingMsg = "Submitting goal to TitanForge CEO...";
      setResponse(submittingMsg);
      playAudio(submittingMsg);

      const task = await taskAPI.submitGoal(goal);
      const responseMessage = `Goal submitted successfully with ID: ${task.id}`;
      setResponse(responseMessage);
      playAudio(responseMessage);
      setGoal("");
    } catch (error: any) {
      const errorMsg = `Error: ${error.detail || error.message}`;
      setResponse(errorMsg);
      playAudio(errorMsg);
    }
  };

  // ---------------- VOICE INPUT ----------------

  const handleVoiceInput = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported in this browser. Please use Chrome.");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onstart = () => {
      setIsRecording(true);
      setGoal("Listening...");
    };

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setGoal(transcript);
    };

    recognition.onerror = () => {
      setGoal("");
    };

    recognition.onend = () => {
      setIsRecording(false);
    };

    recognition.start();
  };

  // ---------------- RENDER ----------------

  return (
    <SwarmProvider autoRefreshInterval={30000}>
      <AuthContext.Provider
        value={{ isAuthenticated, user, setIsAuthenticated, setUser, handleLogout }}
      >
        <div style={{ display: "flex", fontFamily: "sans-serif", minHeight: "100vh" }}>
          {isAuthenticated && (
            <Sidebar
              isAuthenticated={isAuthenticated}
              handleLogout={handleLogout}
            />
          )}

          <div style={{ flexGrow: 1, padding: "20px", maxWidth: "800px", margin: "auto" }}>
            <header style={{ textAlign: "center", marginBottom: "40px" }}>
              <h1>
                <Link to="/">TitanForge</Link>
              </h1>
              <p>The Interface for Autonomous Software Engineering</p>
            </header>

            <main>
              <Routes>
                <Route path="/" element={<LandingPageProPro />} />
                <Route path="/legacy-landing" element={<LandingPagePro />} />
                <Route path="/pricing" element={<PricingPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />

                {isAuthenticated ? (
                  <>
                    <Route path="/cockpit" element={<AgentCockpitPro />} />
                    <Route
                      path="/dashboard"
                      element={
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
                      }
                    />

                    <Route path="/tasks" element={<TaskHistory />} />
                    <Route path="/chambers/*" element={<ChambersContainer />} />

                    {user?.is_superuser && (
                      <Route path="/analytics" element={<AnalyticsDashboard />} />
                    )}
                  </>
                ) : (
                  <Route path="/dashboard" element={<LoginPage />} />
                )}

                <Route path="*" element={<h1>404: Not Found</h1>} />
              </Routes>
            </main>
          </div>
        </div>
      </AuthContext.Provider>
    </SwarmProvider>
  );
}

export default App;