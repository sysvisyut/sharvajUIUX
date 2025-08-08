import {
  FinancialData,
  APIResponse,
  AuthResponse,
  DashboardData,
  ChatResponse,
  InsightsResponse,
  ChatMessage,
} from "../types";

const API_BASE_URL = "http://localhost:5001";

interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

class APIService {
  private baseURL: string;
  private token: string | null;

  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem("auth_token");
  }

  // Set auth token
  setToken(token: string): void {
    this.token = token;
    localStorage.setItem("auth_token", token);
  }

  // Clear auth token
  clearToken(): void {
    this.token = null;
    localStorage.removeItem("auth_token");
  }

  // Generic request method
  private async request<T = unknown>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<APIResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;

    const config: RequestInit = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    // Add auth token if available
    if (this.token) {
      config.headers = {
        ...config.headers,
        Authorization: `Bearer ${this.token}`,
      };
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error("API request failed:", error);
      throw error;
    }
  }

  // Authentication methods
  async testLogin(): Promise<AuthResponse> {
    const response = await this.request<AuthResponse>("/auth/test-login", {
      method: "POST",
    });

    if (response.data.token) {
      this.setToken(response.data.token);
    }

    return response.data;
  }

  async verifyToken(): Promise<{ valid: boolean; user?: unknown }> {
    const response = await this.request<{ valid: boolean; user?: unknown }>("/auth/verify", {
      method: "POST",
    });
    return response.data;
  }

  // Dashboard methods
  async getDashboard(): Promise<DashboardData> {
    const response = await this.request<DashboardData>("/api/dashboard");
    return response.data;
  }

  // Score submission
  async submitScore(financialData: FinancialData): Promise<unknown> {
    const response = await this.request("/api/submit-score", {
      method: "POST",
      body: JSON.stringify(financialData),
    });
    return response.data;
  }

  // Insights
  async getInsights(): Promise<InsightsResponse> {
    const response = await this.request<InsightsResponse>("/api/insights");
    return response.data;
  }

  // Chat methods
  async sendChatMessage(message: string): Promise<ChatResponse> {
    const response = await this.request<ChatResponse>("/api/chat/send", {
      method: "POST",
      body: JSON.stringify({ message }),
    });
    return response.data;
  }

  async getChatSuggestions(): Promise<{ suggestions: string[] }> {
    const response = await this.request<{ suggestions: string[] }>("/api/chat/suggestions");
    return response.data;
  }

  async getChatHistory(limit: number = 20): Promise<{ history: ChatMessage[] }> {
    const response = await this.request<{ history: ChatMessage[] }>(
      `/api/chat/history?limit=${limit}`
    );
    return response.data;
  }

  // PDF generation
  async generatePDF(): Promise<Blob> {
    const response = await fetch(`${this.baseURL}/api/generate-pdf`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${this.token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Failed to generate PDF");
    }

    return response.blob();
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await this.request<{ status: string }>("/health");
    return response.data;
  }
}

export default new APIService();
