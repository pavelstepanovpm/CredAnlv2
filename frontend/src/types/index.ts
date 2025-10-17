// Основные типы данных системы

export interface CreditContract {
  id: string;
  credit_type: 'credit_line' | 'one_time_loan' | 'overdraft' | 'revolving';
  currency: 'RUB' | 'USD' | 'EUR';
  total_limit: number;
  available_limit: number;
  start_date: string;
  end_date: string;
  payment_schedule_type: 'annuity' | 'differentiated' | 'bullet' | 'custom';
  interest_payment_frequency: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'semi_annually' | 'annually';
  principal_payment_frequency: 'daily' | 'weekly' | 'monthly' | 'quarterly' | 'semi_annually' | 'annually';
  interest_rate_base?: number;
  margin?: number;
  created_at: string;
  updated_at: string;
}

export interface Drawdown {
  id: string;
  contract_id: string;
  drawdown_date: string;
  amount: number;
  interest_rate_type: 'fixed' | 'floating';
  interest_rate: number;
  base_rate?: number;
  margin?: number;
  status: 'planned' | 'actual';
  created_at: string;
  updated_at: string;
}

export interface Repayment {
  id: string;
  contract_id: string;
  repayment_date: string;
  principal_amount: number;
  interest_amount: number;
  status: 'planned' | 'actual';
  repayment_type: 'principal' | 'interest' | 'full';
  created_at: string;
  updated_at: string;
}

export interface CalculationVersion {
  id: string;
  name: string;
  description?: string;
  version_type: 'base' | 'scenario';
  status: 'draft' | 'active' | 'archived';
  base_version_id?: string;
  scenario_parameters: Record<string, any>;
  created_at: string;
  created_by: string;
  updated_at: string;
}

export interface PaymentScheduleItem {
  payment_date: string;
  debt_balance_start: number;
  debt_balance_end: number;
  drawdown_amount: number;
  principal_payment: number;
  interest_payment: number;
  effective_rate: number;
  days_in_period: number;
}

export interface PaymentSchedule {
  contract_id: string;
  version_id: string;
  schedule_items: PaymentScheduleItem[];
  calculation_date: string;
  total_drawdowns: number;
  total_principal_payments: number;
  total_interest_payments: number;
}

export interface PortfolioCashflowItem {
  cashflow_date: string;
  total_drawdowns: number;
  total_principal_payments: number;
  total_interest_payments: number;
  total_debt_balance: number;
  total_available_limit: number;
}

export interface PortfolioCashflow {
  version_id: string;
  cashflow_items: PortfolioCashflowItem[];
  report_start_date?: string;
  report_end_date?: string;
  total_drawdowns: number;
  total_principal_payments: number;
  total_interest_payments: number;
  debt_balance_start_period: number;
  debt_balance_end_period: number;
  limit_balance_start_period: number;
  limit_balance_end_period: number;
}

// Типы для UI компонентов

export interface MetricCard {
  title: string;
  value: number | string;
  format: 'currency' | 'percentage' | 'number';
  trend?: 'increasing' | 'decreasing' | 'stable';
  color?: 'primary' | 'success' | 'warning' | 'error' | 'info';
}

export interface ChartData {
  name: string;
  data: Array<{
    x: string | number;
    y: number;
    [key: string]: any;
  }>;
  color?: string;
}

export interface TableColumn {
  id: string;
  label: string;
  minWidth?: number;
  align?: 'left' | 'right' | 'center';
  format?: (value: any) => string;
}

export interface Alert {
  id: string;
  type: 'info' | 'warning' | 'error' | 'success';
  title: string;
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: string;
  dismissed?: boolean;
}

export interface ScenarioTemplate {
  id: string;
  name: string;
  description: string;
  parameters: Record<string, any>;
}

// Типы для API

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  timestamp: string;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, any>;
}

// Типы для состояния приложения

export interface AppState {
  portfolio: PortfolioState;
  versions: VersionsState;
  ui: UIState;
}

export interface PortfolioState {
  contracts: CreditContract[];
  drawdowns: Drawdown[];
  repayments: Repayment[];
  cashflow: PortfolioCashflow | null;
  metrics: PortfolioMetrics | null;
  loading: boolean;
  error: string | null;
}

export interface VersionsState {
  versions: CalculationVersion[];
  activeVersion: string | null;
  loading: boolean;
  error: string | null;
}

export interface UIState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  notifications: Alert[];
  loading: boolean;
}

export interface PortfolioMetrics {
  total_contracts: number;
  total_limit: number;
  total_utilized: number;
  total_available: number;
  utilization_ratio: number;
  weighted_average_rate: number;
  concentration_metrics: {
    hhi: number;
    max_share: number;
    large_contracts_count: number;
    concentration_risk: 'low' | 'medium' | 'high';
  };
  debt_balance_start: number;
  debt_balance_end: number;
  limit_balance_start: number;
  limit_balance_end: number;
}

// Типы для форм

export interface ScenarioFormData {
  name: string;
  description: string;
  type: 'rate_change' | 'additional_drawdowns' | 'early_repayments' | 'stress_test';
  base_version_id: string;
  parameters: Record<string, any>;
}

export interface ContractFormData {
  credit_type: string;
  currency: string;
  total_limit: number;
  start_date: string;
  end_date: string;
  payment_schedule_type: string;
  interest_payment_frequency: string;
  principal_payment_frequency: string;
}

// Типы для фильтров и поиска

export interface FilterOptions {
  credit_type?: string[];
  currency?: string[];
  status?: string[];
  date_range?: {
    start: string;
    end: string;
  };
}

export interface SortOptions {
  field: string;
  direction: 'asc' | 'desc';
}

export interface SearchOptions {
  query: string;
  filters: FilterOptions;
  sort: SortOptions;
  page: number;
  pageSize: number;
}

// Демо интерфейс для показа Git workflow
export interface DemoData {
  id: string;
  name: string;
  value: number;
  timestamp: string;
}

