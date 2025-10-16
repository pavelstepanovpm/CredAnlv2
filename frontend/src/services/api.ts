import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  CreditContract, 
  Drawdown, 
  Repayment, 
  CalculationVersion, 
  PortfolioCashflow, 
  PortfolioMetrics,
  ApiResponse,
  PaginatedResponse 
} from '../types';

// Конфигурация API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Интерцептор для обработки ошибок
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error);
        return Promise.reject(error);
      }
    );
  }

  // Методы для работы с портфелем
  async getPortfolioData(): Promise<AxiosResponse<{
    contracts: CreditContract[];
    drawdowns: Drawdown[];
    repayments: Repayment[];
  }>> {
    return this.client.get('/portfolio/data');
  }

  async getPortfolioMetrics(versionId: string): Promise<AxiosResponse<PortfolioMetrics>> {
    return this.client.get(`/portfolio/metrics/${versionId}`);
  }

  async getPortfolioCashflow(versionId: string): Promise<AxiosResponse<PortfolioCashflow>> {
    return this.client.get(`/portfolio/cashflow/${versionId}`);
  }

  async refreshPortfolioData(): Promise<AxiosResponse<{
    contracts: CreditContract[];
    drawdowns: Drawdown[];
    repayments: Repayment[];
  }>> {
    return this.client.post('/portfolio/refresh');
  }

  async getContractDetails(contractId: string): Promise<AxiosResponse<CreditContract>> {
    return this.client.get(`/portfolio/contracts/${contractId}`);
  }

  // Методы для работы с версиями
  async getVersions(): Promise<AxiosResponse<CalculationVersion[]>> {
    return this.client.get('/versions');
  }

  async createVersion(versionData: Partial<CalculationVersion>): Promise<AxiosResponse<CalculationVersion>> {
    return this.client.post('/versions', versionData);
  }

  async updateVersion(id: string, data: Partial<CalculationVersion>): Promise<AxiosResponse<CalculationVersion>> {
    return this.client.put(`/versions/${id}`, data);
  }

  async deleteVersion(id: string): Promise<AxiosResponse<void>> {
    return this.client.delete(`/versions/${id}`);
  }

  async setActiveVersion(id: string): Promise<AxiosResponse<CalculationVersion>> {
    return this.client.post(`/versions/${id}/activate`);
  }

  async compareVersions(version1Id: string, version2Id: string): Promise<AxiosResponse<any>> {
    return this.client.get(`/versions/compare/${version1Id}/${version2Id}`);
  }

  // Методы для работы со сценариями
  async createScenario(scenarioData: any): Promise<AxiosResponse<CalculationVersion>> {
    return this.client.post('/scenarios', scenarioData);
  }

  async getScenarioTemplates(): Promise<AxiosResponse<any[]>> {
    return this.client.get('/scenarios/templates');
  }

  // Методы для работы с отчетами
  async generateReport(reportType: string, parameters: any): Promise<AxiosResponse<any>> {
    return this.client.post(`/reports/${reportType}`, parameters);
  }

  async downloadReport(reportId: string, format: 'pdf' | 'excel'): Promise<AxiosResponse<Blob>> {
    return this.client.get(`/reports/${reportId}/download/${format}`, {
      responseType: 'blob',
    });
  }

  // Методы для работы с данными
  async exportData(format: 'json' | 'csv' | 'excel'): Promise<AxiosResponse<Blob>> {
    return this.client.get(`/data/export/${format}`, {
      responseType: 'blob',
    });
  }

  async importData(file: File): Promise<AxiosResponse<any>> {
    const formData = new FormData();
    formData.append('file', file);
    return this.client.post('/data/import', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  }
}

// Создание экземпляров API клиентов
export const portfolioApi = new ApiClient();
export const versionsApi = new ApiClient();
export const scenariosApi = new ApiClient();
export const reportsApi = new ApiClient();
export const dataApi = new ApiClient();

// Экспорт основного клиента
export default new ApiClient();

