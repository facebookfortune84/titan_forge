import React, { createContext, useContext, useState, useCallback, useEffect, ReactNode } from 'react';
import { Agent, SwarmStatus, ApiError } from '@/types/index';
import { agentAPI } from '@/services/api';

interface SwarmContextType {
  agents: Agent[];
  swarmStatus: SwarmStatus | null;
  loading: boolean;
  error: ApiError | null;
  refreshAgents: () => Promise<void>;
  refreshSwarmStatus: () => Promise<void>;
  getAgentsByDepartment: (department: string) => Agent[];
  getActiveAgents: () => Agent[];
  isAgentOnline: (agentId: string) => boolean;
}

const SwarmContext = createContext<SwarmContextType | null>(null);

export interface SwarmProviderProps {
  children: ReactNode;
  autoRefreshInterval?: number; // milliseconds, 0 to disable
}

export const SwarmProvider: React.FC<SwarmProviderProps> = ({ children, autoRefreshInterval = 30000 }) => {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [swarmStatus, setSwarmStatus] = useState<SwarmStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<ApiError | null>(null);

  const refreshAgents = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await agentAPI.getAgents();
      setAgents(data);
    } catch (err) {
      setError(err as ApiError);
    } finally {
      setLoading(false);
    }
  }, []);

  const refreshSwarmStatus = useCallback(async () => {
    try {
      const status = await agentAPI.getSwarmStatus();
      setSwarmStatus(status);
    } catch (err) {
      setError(err as ApiError);
    }
  }, []);

  const getAgentsByDepartment = useCallback(
    (department: string): Agent[] => {
      return agents.filter((agent) => agent.department === department);
    },
    [agents]
  );

  const getActiveAgents = useCallback((): Agent[] => {
    return agents.filter((agent) => agent.status !== 'offline');
  }, [agents]);

  const isAgentOnline = useCallback(
    (agentId: string): boolean => {
      const agent = agents.find((a) => a.agent_id === agentId);
      return agent?.status !== 'offline';
    },
    [agents]
  );

  // Auto-refresh on mount and interval
  useEffect(() => {
    refreshAgents();
    refreshSwarmStatus();
  }, [refreshAgents, refreshSwarmStatus]);

  useEffect(() => {
    if (autoRefreshInterval <= 0) return;

    const interval = setInterval(() => {
      refreshAgents();
      refreshSwarmStatus();
    }, autoRefreshInterval);

    return () => clearInterval(interval);
  }, [autoRefreshInterval, refreshAgents, refreshSwarmStatus]);

  const value: SwarmContextType = {
    agents,
    swarmStatus,
    loading,
    error,
    refreshAgents,
    refreshSwarmStatus,
    getAgentsByDepartment,
    getActiveAgents,
    isAgentOnline,
  };

  return <SwarmContext.Provider value={value}>{children}</SwarmContext.Provider>;
};

export const useSwarm = (): SwarmContextType => {
  const context = useContext(SwarmContext);
  if (!context) {
    throw new Error('useSwarm must be used within a SwarmProvider');
  }
  return context;
};
