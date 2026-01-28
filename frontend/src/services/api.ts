// API Service for E-commerce Product Description Generator

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

export interface GenerateRequest {
  product_name: string;
  category: string;
  features?: string;
  target_audience?: string;
  tone: string;
  language: string;
  length: string;
  num_variants: number;
}

export interface ImproveRequest {
  original_description: string;
  improvement_focus: string[];
  tone: string;
  language: string;
}

export interface SEORequest {
  product_name: string;
  description?: string;
  category: string;
  language: string;
}

export interface TranslateRequest {
  description: string;
  source_language: string;
  target_language: string;
  adapt_culturally: boolean;
}

export interface APIResponse {
  success: boolean;
  data?: string;
  error?: string;
}

class APIService {
  private async request(endpoint: string, data: any): Promise<APIResponse> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Une erreur est survenue',
      };
    }
  }

  async generateDescription(data: GenerateRequest): Promise<APIResponse> {
    return this.request('/generate', data);
  }

  async improveDescription(data: ImproveRequest): Promise<APIResponse> {
    return this.request('/improve', data);
  }

  async generateSEO(data: SEORequest): Promise<APIResponse> {
    return this.request('/seo', data);
  }

  async translateDescription(data: TranslateRequest): Promise<APIResponse> {
    return this.request('/translate', data);
  }

  async checkHealth(): Promise<any> {
    try {
      const response = await fetch('/health');
      return await response.json();
    } catch (error) {
      return { status: 'error', error: 'Cannot connect to backend' };
    }
  }
}

export const api = new APIService();
