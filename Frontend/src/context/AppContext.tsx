import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import APIService from '../services/api';
import { 
  User, 
  DashboardData, 
  ChatMessage, 
  Insight, 
  FinancialData 
} from '../types';

interface AppState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  dashboard: DashboardData | null;
  insights: Insight[] | null;
  chatHistory: ChatMessage[];
  error: string | null;
}

type AppAction = 
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'SET_DASHBOARD'; payload: DashboardData }
  | { type: 'SET_INSIGHTS'; payload: Insight[] }
  | { type: 'SET_CHAT_HISTORY'; payload: ChatMessage[] }
  | { type: 'ADD_CHAT_MESSAGE'; payload: ChatMessage }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'CLEAR_ERROR' }
  | { type: 'LOGOUT' };

interface AppContextType extends AppState {
  testLogin: () => Promise<void>;
  loadDashboard: () => Promise<void>;
  submitFinancialData: (financialData: FinancialData) => Promise<unknown>;
  loadInsights: () => Promise<Insight[]>;
  sendChatMessage: (message: string) => Promise<unknown>;
  loadChatHistory: () => Promise<void>;
  downloadPDF: () => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const initialState: AppState = {
  user: null,
  isAuthenticated: false,
  loading: false,
  dashboard: null,
  insights: null,
  chatHistory: [],
  error: null
};

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    
    case 'SET_USER':
      return { 
        ...state, 
        user: action.payload, 
        isAuthenticated: !!action.payload 
      };
    
    case 'SET_DASHBOARD':
      return { ...state, dashboard: action.payload };
    
    case 'SET_INSIGHTS':
      return { ...state, insights: action.payload };
    
    case 'SET_CHAT_HISTORY':
      return { ...state, chatHistory: action.payload };
    
    case 'ADD_CHAT_MESSAGE':
      return { 
        ...state, 
        chatHistory: [action.payload, ...state.chatHistory] 
      };
    
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    
    case 'CLEAR_ERROR':
      return { ...state, error: null };
    
    case 'LOGOUT':
      return { 
        ...initialState,
        isAuthenticated: false 
      };
    
    default:
      return state;
  }
}

interface AppProviderProps {
  children: ReactNode;
}

export const AppProvider: React.FC<AppProviderProps> = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Initialize app
  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async (): Promise<void> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      
      // Check if we have a token
      const token = localStorage.getItem('auth_token');
      if (token) {
        try {
          const response = await APIService.verifyToken();
          if (response.valid) {
            dispatch({ type: 'SET_USER', payload: response.user as User });
            await loadDashboard();
          }
        } catch (error) {
          // Token invalid, try test login for development
          await testLogin();
        }
      } else {
        // No token, try test login for development
        await testLogin();
      }
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const testLogin = async (): Promise<void> => {
    try {
      const response = await APIService.testLogin();
      dispatch({ type: 'SET_USER', payload: response.user });
      await loadDashboard();
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
    }
  };

  const loadDashboard = async (): Promise<void> => {
    try {
      const response = await APIService.getDashboard();
      dispatch({ type: 'SET_DASHBOARD', payload: response });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
    }
  };

  const submitFinancialData = async (financialData: FinancialData): Promise<unknown> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const response = await APIService.submitScore(financialData);
      
      // Reload dashboard after submission
      await loadDashboard();
      
      return response;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
      throw error;
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const loadInsights = async (): Promise<Insight[]> => {
    try {
      const response = await APIService.getInsights();
      dispatch({ type: 'SET_INSIGHTS', payload: response.insights });
      return response.insights;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
      throw error;
    }
  };

  const sendChatMessage = async (message: string): Promise<unknown> => {
    try {
      const response = await APIService.sendChatMessage(message);
      
      const chatMessage: ChatMessage = {
        message,
        response: response.response,
        timestamp: response.timestamp
      };
      
      dispatch({ type: 'ADD_CHAT_MESSAGE', payload: chatMessage });
      return response;
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
      throw error;
    }
  };

  const loadChatHistory = async (): Promise<void> => {
    try {
      const response = await APIService.getChatHistory();
      dispatch({ type: 'SET_CHAT_HISTORY', payload: response.history });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
    }
  };

  const downloadPDF = async (): Promise<void> => {
    try {
      const pdfBlob = await APIService.generatePDF();
      
      // Create download link
      const url = window.URL.createObjectURL(pdfBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `credit_report_${new Date().toISOString().split('T')[0]}.pdf`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: (error as Error).message });
      throw error;
    }
  };

  const logout = (): void => {
    APIService.clearToken();
    dispatch({ type: 'LOGOUT' });
  };

  const clearError = (): void => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value: AppContextType = {
    ...state,
    testLogin,
    loadDashboard,
    submitFinancialData,
    loadInsights,
    sendChatMessage,
    loadChatHistory,
    downloadPDF,
    logout,
    clearError
  };

  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
};

export const useApp = (): AppContextType => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};
