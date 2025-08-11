import axios from 'axios';
import type {
  Source, SourceCreate, SourceUpdate,
  Topic, TopicSearchRequest, TopicSearchResponse,
  Article, ArticleList
} from '../types/api';

// Create axios instance
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
    },
    // Remove withCredentials for "*" origin
  });

// API service for sources
export const sourceApi = {
  getSources: async (params?: { skip?: number; limit?: number; source_type?: string }) => {
    const response = await api.get<Source[]>('/sources', { params });
    return response.data;
  },

  getSource: async (id: number) => {
    const response = await api.get<Source>(`/sources/${id}`);
    return response.data;
  },

  createSource: async (source: SourceCreate) => {
    const response = await api.post<Source>('/sources', source);
    return response.data;
  },

  updateSource: async (id: number, source: SourceUpdate) => {
    const response = await api.put<Source>(`/sources/${id}`, source);
    return response.data;
  },

  deleteSource: async (id: number): Promise<void> => {
    await api.delete(`/sources/${id}`);
  }
};

// API service for topics
export const topicApi = {
  getTopics: async (params?: { skip?: number; limit?: number; sort_by?: string }) => {
    const response = await api.get<Topic[]>('/topics', { params });
    return response.data;
  },

  getTopic: async (id: number) => {
    const response = await api.get<Topic>(`/topics/${id}`);
    return response.data;
  },

  searchTopic: async (request: TopicSearchRequest) => {
    const response = await api.post<TopicSearchResponse>('/topics/search', request);
    return response.data;
  },

  getTopicArticles: async (
    topicId: number,
    params?: { page?: number; size?: number; sort_by?: string }
  ) => {
    const response = await api.get<ArticleList>(`/topics/${topicId}/articles`, { params });
    return response.data;
  }
};

// API service for articles
export const articleApi = {
  getArticles: async (params?: {
    skip?: number;
    limit?: number;
    source_id?: number;
    source_name?: string;
  }) => {
    const response = await api.get<Article[]>('/articles', { params });
    return response.data;
  },

  getArticle: async (id: number) => {
    const response = await api.get<Article>(`/articles/${id}`);
    return response.data;
  }
};

// Health check API
export const healthApi = {
  check: async () => {
    const response = await axios.get<{ status: string }>('http://localhost:8000/health');
    return response.data;
  }
};

export default api;