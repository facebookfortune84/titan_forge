// Comprehensive TypeScript type definitions for TitanForge

export interface User {
  id: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface AuthTokens {
  access_token: string;
  token_type: string;
}

export interface Task {
  id: string;
  goal: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  created_at: string;
  updated_at: string;
  user_id: string;
  result?: string;
  error?: string;
}

export interface ScheduledJob {
  id: string;
  name: string;
  description?: string;
  schedule: string;
  next_run_time: string;
  last_run_time?: string;
  is_active: boolean;
  status: 'scheduled' | 'running' | 'completed' | 'failed';
}

export interface Agent {
  agent_id: string;
  role: string;
  department: string;
  model_name?: string;
  is_active: boolean;
  status?: 'idle' | 'busy' | 'offline';
  description?: string;
}

export interface Message {
  sender_id: string;
  recipient_id: string;
  content: string;
  timestamp: string;
  message_type?: 'task' | 'update' | 'error' | 'info';
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

export interface GraphNode {
  id: string;
  name: string;
  type: 'agent' | 'task' | 'artifact' | 'department';
  status?: string;
  metadata?: Record<string, any>;
}

export interface GraphLink {
  source: string;
  target: string;
  relationship: string;
  weight?: number;
}

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  currency: string;
  stripe_product_id: string;
  stripe_price_id: string;
  features: string[];
  active: boolean;
}

export interface CheckoutSession {
  session_id: string;
  url: string;
  expires_at: string;
}

export interface Transaction {
  id: string;
  user_id: string;
  amount: number;
  currency: string;
  status: 'succeeded' | 'failed' | 'pending';
  product_id?: string;
  created_at: string;
  description?: string;
}

export interface IncomeReport {
  total_revenue: number;
  total_transactions: number;
  currency: string;
  period: {
    start_date: string;
    end_date: string;
  };
  breakdown?: Record<string, number>;
}

export interface AnalyticsSummary {
  total_users: number;
  new_signups_this_month: number;
  active_subscriptions: number;
  mrr_estimate: number;
  churn_rate: number;
  retention_rate: number;
  avg_revenue_per_user: number;
}

export interface FileContent {
  path: string;
  content: string;
  size?: number;
  type?: string;
}

export interface SwarmStatus {
  total_agents: number;
  active_agents: number;
  departments: DepartmentStatus[];
  system_health: 'healthy' | 'degraded' | 'offline';
  uptime_seconds: number;
}

export interface DepartmentStatus {
  name: string;
  agent_count: number;
  active_agents: number;
  status: 'operational' | 'degraded' | 'offline';
}

export interface ApiError {
  detail: string;
  status_code: number;
  error_type?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface Lead {
  id: string;
  email: string;
  full_name?: string;
  company?: string;
  source: string;
  status: 'new' | 'contacted' | 'converted' | 'lost';
  created_at?: string;
  updated_at?: string;
}
