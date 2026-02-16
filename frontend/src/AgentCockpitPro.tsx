// @ts-nocheck
import React, { useState, useEffect, useRef, useContext } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Mic, Send, Settings, Users, Radio, PlayCircle, Pause,
  Volume2, VolumeX, Sparkles, Zap, CheckCircle, AlertCircle,
  Terminal, Eye, Grid, List, MessageSquare, Clock
} from "lucide-react";
import { AuthContext } from "./App";
import { taskAPI, messageAPI, agentAPI } from "@/services/api";

// Import chamber components
import WarRoom from "./components/chambers/WarRoom";
import NeuralLattice from "./components/chambers/NeuralLattice";
import ArtifactStudio from "./components/chambers/ArtifactStudio";
import ArsenalManager from "./components/chambers/ArsenalManager";

export default function AgentCockpit() {
  const { isAuthenticated } = useContext(AuthContext)!;
  
  // --- STATE ---
  const [commandInput, setCommandInput] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [responses, setResponses] = useState<any[]>([]);
  const [activeAgents, setActiveAgents] = useState<any[]>([]);
  const [activeTasks, setActiveTasks] = useState<any[]>([]);
  const [viewMode, setViewMode] = useState<"terminal" | "graph" | "studio" | "arsenal">("terminal");
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [taskLogs, setTaskLogs] = useState<any[]>([]);
  
  const recognitionRef = useRef<any>(null);
  const synthesisRef = useRef<any>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  // --- SCROLL TO BOTTOM OF LOGS ---
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [responses, taskLogs]);

  // --- INITIALIZE VOICE ---
  useEffect(() => {
    if (!("webkitSpeechRecognition" in window)) {
      console.warn("Speech recognition not available");
      return;
    }

    recognitionRef.current = new window.webkitSpeechRecognition();
    recognitionRef.current.continuous = false;
    recognitionRef.current.interimResults = true;
    recognitionRef.current.lang = "en-US";

    recognitionRef.current.onstart = () => setIsListening(true);
    recognitionRef.current.onend = () => setIsListening(false);
    recognitionRef.current.onerror = () => setIsListening(false);

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, []);

  // --- FETCH AGENTS & TASKS ---
  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchData = async () => {
      try {
        const agents = await agentAPI.getAgents();
        setActiveAgents(agents || []);
      } catch (error) {
        console.error("Failed to fetch agents:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, [isAuthenticated]);

  // --- VOICE INPUT ---
  const startListening = () => {
    if (!recognitionRef.current) return;

    recognitionRef.current.onresult = (event: any) => {
      let transcript = "";
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      setCommandInput(transcript);
    };

    recognitionRef.current.start();
  };

  // --- TEXT-TO-SPEECH ---
  const speakResponse = (text: string) => {
    if (!voiceEnabled || !text) return;
    
    setIsSpeaking(true);
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9;
    utterance.onend = () => setIsSpeaking(false);
    
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  };

  // --- SUBMIT COMMAND ---
  const handleSubmitCommand = async () => {
    if (!commandInput.trim() || !isAuthenticated) return;

    const userInput = commandInput;
    setCommandInput("");

    // Add to log
    setResponses((prev) => [
      ...prev,
      {
        id: Date.now(),
        type: "user",
        content: userInput,
        timestamp: new Date(),
      },
    ]);

    // Add loading state
    const loadingId = Date.now() + 1;
    setResponses((prev) => [
      ...prev,
      {
        id: loadingId,
        type: "system",
        content: "Processing command...",
        loading: true,
        timestamp: new Date(),
      },
    ]);

    try {
      // Parse command and route to appropriate handler
      const command = userInput.toLowerCase();
      let response = "";

      if (command.includes("agents") || command.includes("roster")) {
        response = `Active Agents: ${activeAgents.length}\n\n${activeAgents.map((a: any) => `• ${a.name} (${a.role})`).join("\n")}`;
      } else if (command.includes("task") || command.includes("build")) {
        // Submit task to backend
        const task = await taskAPI.submitGoal(userInput);
        response = `Task created: ${task.id}\n\nTask: ${task.goal}\nStatus: In Progress`;
        
        // Add to active tasks
        setActiveTasks((prev) => [...prev, task]);
        
        // Log
        setTaskLogs((prev) => [
          ...prev,
          {
            id: task.id,
            type: "task_created",
            content: userInput,
            timestamp: new Date(),
            status: "in_progress",
          },
        ]);
      } else if (command.includes("status")) {
        response = `Current Status:\n\nActive Agents: ${activeAgents.length}\nActive Tasks: ${activeTasks.length}\nLast Update: ${new Date().toLocaleTimeString()}`;
      } else {
        // Default: submit as goal
        const task = await taskAPI.submitGoal(userInput);
        response = `Command acknowledged. Task ID: ${task.id}\n\n${task.goal}`;
      }

      // Remove loading state and add response
      setResponses((prev) => prev.filter((r) => r.id !== loadingId));
      setResponses((prev) => [
        ...prev,
        {
          id: Date.now() + 2,
          type: "agent",
          content: response,
          timestamp: new Date(),
        },
      ]);

      // Speak response
      if (voiceEnabled) {
        speakResponse(response.substring(0, 200)); // Speak first 200 chars
      }
    } catch (error: any) {
      setResponses((prev) => prev.filter((r) => r.id !== loadingId));
      setResponses((prev) => [
        ...prev,
        {
          id: Date.now() + 2,
          type: "error",
          content: `Error: ${error.message || "Failed to process command"}`,
          timestamp: new Date(),
        },
      ]);
    }
  };

  return (
    <div className="h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-900 text-white flex overflow-hidden">
      {/* --- LEFT PANEL: COMMAND CENTER --- */}
      <div className="w-full lg:w-1/3 border-r border-purple-500/20 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="p-4 border-b border-purple-500/20 bg-slate-900/50 backdrop-blur">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
              <Zap size={24} className="text-white" />
            </div>
            <div>
              <h1 className="font-bold text-lg">Agent Cockpit</h1>
              <p className="text-xs text-slate-400">Command your swarm</p>
            </div>
          </div>

          {/* Status Indicators */}
          <div className="grid grid-cols-3 gap-2 text-xs">
            <div className="bg-slate-800/50 rounded p-2 border border-green-500/30">
              <div className="text-green-400 font-bold">{activeAgents.length}</div>
              <div className="text-slate-500">Agents Active</div>
            </div>
            <div className="bg-slate-800/50 rounded p-2 border border-blue-500/30">
              <div className="text-blue-400 font-bold">{activeTasks.length}</div>
              <div className="text-slate-500">Tasks Running</div>
            </div>
            <div className="bg-slate-800/50 rounded p-2 border border-purple-500/30">
              <div className="text-purple-400 font-bold">
                {new Date().toLocaleTimeString()}
              </div>
              <div className="text-slate-500">Time</div>
            </div>
          </div>
        </div>

        {/* Terminal / Response Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 font-mono text-sm">
          {responses.length === 0 && (
            <div className="text-center text-slate-500 py-12">
              <Terminal size={48} className="mx-auto mb-4 opacity-50" />
              <p>Ready for commands. Speak or type below.</p>
            </div>
          )}

          {responses.map((response) => (
            <motion.div
              key={response.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className={`p-3 rounded-lg backdrop-blur ${
                response.type === "user"
                  ? "bg-purple-500/20 border border-purple-500/30 text-purple-100"
                  : response.type === "agent"
                  ? "bg-green-500/20 border border-green-500/30 text-green-100"
                  : response.type === "error"
                  ? "bg-red-500/20 border border-red-500/30 text-red-100"
                  : "bg-slate-700/50 border border-slate-600/30 text-slate-300"
              }`}
            >
              <div className="flex items-start gap-2">
                {response.type === "user" && <MessageSquare size={16} className="mt-1 flex-shrink-0" />}
                {response.type === "agent" && <CheckCircle size={16} className="mt-1 flex-shrink-0" />}
                {response.type === "error" && <AlertCircle size={16} className="mt-1 flex-shrink-0" />}
                {response.loading && (
                  <div className="w-4 h-4 border-2 border-slate-500/30 border-t-slate-200 rounded-full animate-spin mt-1 flex-shrink-0" />
                )}
                <div className="flex-1 min-w-0">
                  <p className="whitespace-pre-wrap break-words text-xs">{response.content}</p>
                  <p className="text-xs opacity-50 mt-1">
                    {response.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}

          <div ref={logsEndRef} />
        </div>

        {/* Command Input Area */}
        <div className="p-4 border-t border-purple-500/20 bg-slate-900/50 backdrop-blur space-y-4">
          {/* Voice Indicator */}
          {isListening && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="flex items-center gap-2 p-3 bg-red-500/20 border border-red-500/30 rounded-lg"
            >
              <Mic size={16} className="text-red-400 animate-pulse" />
              <span className="text-sm text-red-300">Listening...</span>
            </motion.div>
          )}

          {/* Input Field */}
          <div className="flex gap-2">
            <input
              type="text"
              value={commandInput}
              onChange={(e) => setCommandInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSubmitCommand()}
              placeholder="Speak or type command... 'Build me a React login page'"
              className="flex-1 px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-lg focus:outline-none focus:border-purple-500/50 transition text-sm"
              disabled={isListening}
            />
          </div>

          {/* Control Buttons */}
          <div className="grid grid-cols-4 gap-2">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={startListening}
              disabled={isListening}
              className="flex items-center justify-center gap-2 px-3 py-2 bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 disabled:opacity-50 rounded-lg transition"
              title="Voice Input"
            >
              <Mic size={18} />
              <span className="text-xs hidden sm:inline">Speak</span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleSubmitCommand}
              disabled={!commandInput.trim()}
              className="flex items-center justify-center gap-2 px-3 py-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 disabled:opacity-50 rounded-lg transition"
              title="Send Command"
            >
              <Send size={18} />
              <span className="text-xs hidden sm:inline">Send</span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setVoiceEnabled(!voiceEnabled)}
              className={`flex items-center justify-center gap-2 px-3 py-2 rounded-lg transition ${
                voiceEnabled
                  ? "bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700"
                  : "bg-slate-700 hover:bg-slate-600"
              }`}
              title="Toggle Voice Output"
            >
              {voiceEnabled ? <Volume2 size={18} /> : <VolumeX size={18} />}
              <span className="text-xs hidden sm:inline">Voice</span>
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setResponses([])}
              className="flex items-center justify-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition"
              title="Clear Logs"
            >
              <Settings size={18} />
              <span className="text-xs hidden sm:inline">Clear</span>
            </motion.button>
          </div>
        </div>
      </div>

      {/* --- RIGHT PANEL: CHAMBERS VIEW --- */}
      <div className="hidden lg:flex w-2/3 flex-col border-l border-purple-500/20">
        {/* View Mode Selector */}
        <div className="p-4 border-b border-purple-500/20 bg-slate-900/50 backdrop-blur flex items-center gap-2 flex-wrap">
          <span className="text-sm text-slate-400">View:</span>
          {[
            { id: "terminal", label: "Terminal", icon: Terminal },
            { id: "graph", label: "Neural Lattice", icon: Sparkles },
            { id: "studio", label: "Artifact Studio", icon: Eye },
            { id: "arsenal", label: "Arsenal", icon: Zap },
          ].map((mode) => {
            const Icon = mode.icon;
            return (
              <motion.button
                key={mode.id}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setViewMode(mode.id as any)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg transition ${
                  viewMode === mode.id
                    ? "bg-purple-600/50 border border-purple-500/50"
                    : "bg-slate-800/50 border border-slate-700/50 hover:border-slate-600/50"
                }`}
              >
                <Icon size={16} />
                <span className="text-xs">{mode.label}</span>
              </motion.button>
            );
          })}
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-auto">
          <AnimatePresence mode="wait">
            {viewMode === "terminal" && (
              <motion.div
                key="terminal"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full p-4 overflow-auto"
              >
                <div className="space-y-4">
                  <h3 className="text-lg font-bold">Active Tasks & Logs</h3>
                  {taskLogs.length === 0 ? (
                    <p className="text-slate-500">No tasks yet. Send a command to get started.</p>
                  ) : (
                    taskLogs.map((log) => (
                      <div key={log.id} className="p-3 bg-slate-800/50 border border-slate-700/50 rounded-lg">
                        <div className="flex items-center gap-2 mb-2">
                          <Clock size={14} />
                          <span className="text-xs text-slate-500">{log.timestamp.toLocaleTimeString()}</span>
                          <span
                            className={`text-xs font-bold px-2 py-1 rounded ${
                              log.status === "in_progress"
                                ? "bg-yellow-500/20 text-yellow-300"
                                : "bg-green-500/20 text-green-300"
                            }`}
                          >
                            {log.status}
                          </span>
                        </div>
                        <p className="text-sm text-slate-300">{log.content}</p>
                      </div>
                    ))
                  )}
                </div>
              </motion.div>
            )}

            {viewMode === "graph" && (
              <motion.div
                key="graph"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full"
              >
                {isAuthenticated && <NeuralLattice />}
              </motion.div>
            )}

            {viewMode === "studio" && (
              <motion.div
                key="studio"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full"
              >
                {isAuthenticated && <ArtifactStudio />}
              </motion.div>
            )}

            {viewMode === "arsenal" && (
              <motion.div
                key="arsenal"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="h-full"
              >
                {isAuthenticated && <ArsenalManager />}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
