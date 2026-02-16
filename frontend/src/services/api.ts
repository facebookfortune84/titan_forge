import axios, { AxiosError } from 'axios';
import {
  User,
  AuthTokens,
  Task,
  ScheduledJob,
  Agent,
  GraphData,
  Product,
  CheckoutSession,
  Transaction,
  IncomeReport,
  AnalyticsSummary,
  FileContent,
  SwarmStatus,
  ApiError,
  Lead,
} from '@/types/index';

// API Base URL from environment or default
const API_BASE_URL = (import.meta as any).env.VITE_API_URL || 'http://127.0.0.1:8000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Error handler
const handleError = (error: AxiosError<ApiError>): ApiError => {
  if (error.response?.data) {
    return error.response.data;
  }
  return {
    detail: error.message || 'An error occurred',
    status_code: error.response?.status || 500,
  };
};

// ============ AUTH ENDPOINTS ============
export const authAPI = {
  async register(email: string, password: string, full_name?: string): Promise<User> {
    try {
      const response = await apiClient.post<User>('/api/v1/auth/register', {
        email,
        password,
        full_name,
      });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async login(email: string, password: string): Promise<AuthTokens> {
    try {
      const response = await apiClient.post<AuthTokens>('/api/v1/auth/login', {
        email,
        password,
      });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async getCurrentUser(): Promise<User> {
    try {
      const response = await apiClient.get<User>('/api/v1/auth/me');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async refreshToken(): Promise<AuthTokens> {
    try {
      const response = await apiClient.post<AuthTokens>('/api/v1/auth/refresh');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post('/api/v1/auth/logout');
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ TASK ENDPOINTS ============
export const taskAPI = {
  async getTasks(): Promise<Task[]> {
    try {
      const response = await apiClient.get<Record<string, Task>>('/tasks');
      return Object.values(response.data);
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async submitGoal(goal: string): Promise<Task> {
    try {
      const response = await apiClient.post<Task>('/goals', { goal });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async updateTask(taskId: string, status: string): Promise<Task> {
    try {
      const response = await apiClient.put<Task>(`/tasks/${taskId}`, { status });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ SCHEDULER ENDPOINTS ============
export const schedulerAPI = {
  async getJobs(): Promise<ScheduledJob[]> {
    try {
      const response = await apiClient.get<ScheduledJob[]>('/scheduler/jobs');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ AGENT ENDPOINTS ============
export const agentAPI = {
  async getAgents(): Promise<Agent[]> {
    try {
      const response = await apiClient.get<Agent[]>('/api/v1/agents');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async getSwarmStatus(): Promise<SwarmStatus> {
    try {
      const agents = await this.getAgents();
      const departments: Record<string, { count: number; active: number }> = {};

      agents.forEach((agent) => {
        if (!departments[agent.department]) {
          departments[agent.department] = { count: 0, active: 0 };
        }
        departments[agent.department].count += 1;
        if (agent.status === 'idle' || agent.status === 'busy') {
          departments[agent.department].active += 1;
        }
      });

      return {
        total_agents: agents.length,
        active_agents: agents.filter((a) => a.status !== 'offline').length,
        departments: Object.entries(departments).map(([name, data]) => ({
          name,
          agent_count: data.count,
          active_agents: data.active,
          status: data.active > 0 ? 'operational' : 'offline',
        })),
        system_health: agents.filter((a) => a.status === 'offline').length > agents.length * 0.1 ? 'degraded' : 'healthy',
        uptime_seconds: 0,
      };
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ MESSAGING ENDPOINTS ============
export const messageAPI = {
  async sendMessage(recipientId: string, content: string): Promise<void> {
    try {
      await apiClient.post('/messages/send', {
        recipient_id: recipientId,
        content,
      });
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async getMessages(agentId: string): Promise<any[]> {
    try {
      const response = await apiClient.get(`/messages/receive/${agentId}`);
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async textToSpeech(text: string): Promise<Blob> {
    try {
      const response = await apiClient.post<Blob>('/speak', { text }, { responseType: 'blob' });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ GRAPH ENDPOINTS ============
export const graphAPI = {
  async getGraph(): Promise<GraphData> {
    try {
      const response = await apiClient.get<GraphData>('/api/v1/graph');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ FILE I/O ENDPOINTS ============
export const fileAPI = {
  async readFile(path: string): Promise<FileContent> {
    try {
      const response = await apiClient.post<FileContent>('/api/v1/io/read', { path });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async writeFile(path: string, content: string): Promise<FileContent> {
    try {
      const response = await apiClient.post<FileContent>('/api/v1/io/write', { path, content });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ PRODUCT ENDPOINTS ============
export const productAPI = {
  async getProducts(): Promise<Product[]> {
    try {
      const response = await apiClient.get<Product[]>('/api/v1/products');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async createCheckoutSession(productId: string): Promise<CheckoutSession> {
    try {
      const response = await apiClient.post<CheckoutSession>('/api/v1/create-checkout-session', {
        product_id: productId,
      });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ LEAD ENDPOINTS ============
export const leadsAPI = {
  async submitLead(email: string, full_name?: string, company?: string, source: string = 'landing_page'): Promise<Lead> {
    try {
      const response = await apiClient.post<Lead>('/api/v1/leads', {
        email,
        full_name,
        company,
        source,
      });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async getLeads(): Promise<Lead[]> {
    try {
      const response = await apiClient.get<Lead[]>('/api/v1/leads');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async getLead(leadId: string): Promise<Lead> {
    try {
      const response = await apiClient.get<Lead>(`/api/v1/leads/${leadId}`);
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ PAYMENT/INCOME ENDPOINTS ============
export const paymentAPI = {
  async getTransactions(page: number = 1, pageSize: number = 50): Promise<Transaction[]> {
    try {
      const response = await apiClient.get<Transaction[]>('/api/v1/income/transactions', {
        params: { page, page_size: pageSize },
      });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async getIncomeSummary(startDate?: string, endDate?: string): Promise<IncomeReport> {
    try {
      const response = await apiClient.get<IncomeReport>('/api/v1/income/summary', {
        params: { start_date: startDate, end_date: endDate },
      });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async getTransaction(transactionId: string): Promise<Transaction> {
    try {
      const response = await apiClient.get<Transaction>(`/api/v1/income/transaction/${transactionId}`);
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

// ============ ADMIN ENDPOINTS ============
export const adminAPI = {
  async getAnalytics(): Promise<AnalyticsSummary> {
    try {
      const response = await apiClient.get<AnalyticsSummary>('/api/v1/analytics/summary');
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async makeSuperuser(userId: string): Promise<User> {
    try {
      const response = await apiClient.post<User>(`/api/v1/admin/make-superuser/${userId}`);
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async createProduct(name: string, description: string, price: number, features: string[]): Promise<Product> {
    try {
      const response = await apiClient.post<Product>('/api/v1/admin/products', {
        name,
        description,
        price,
        features,
      });
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async updateProduct(productId: string, data: Partial<Product>): Promise<Product> {
    try {
      const response = await apiClient.put<Product>(`/api/v1/admin/products/${productId}`, data);
      return response.data;
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },

  async deleteProduct(productId: string): Promise<void> {
    try {
      await apiClient.delete(`/api/v1/admin/products/${productId}`);
    } catch (error) {
      throw handleError(error as AxiosError<ApiError>);
    }
  },
};

export default apiClient;
