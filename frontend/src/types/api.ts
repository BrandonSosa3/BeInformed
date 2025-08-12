// API response and request types for Source

export interface Source {
    id: number;
    url: string;
    title: string;
    description: string | null;
    source_type: string;
    created_at: string;
    updated_at: string | null;
    credibility_score: number | null;
  }
  
  export interface SourceCreate {
    url: string;
    title: string;
    description?: string;
    source_type: string;
  }
  
  export interface SourceUpdate {
    url?: string;
    title?: string;
    description?: string;
    source_type?: string;
    credibility_score?: number;
  }
  
  // API error type
  export interface ApiError {
    detail: string;
  }
  
  // Pagination params
  export interface PaginationParams {
    skip?: number;
    limit?: number;
  }
  
  // Filter params for sources
  export interface SourceFilterParams extends PaginationParams {
    source_type?: string;
  }

  // API Types for BeInformed

// Source types
export interface Source {
    id: number;
    url: string;
    title: string;
    description: string | null;
    source_type: string;
    created_at: string;
    updated_at: string | null;
    credibility_score: number | null;
  }
  
  export interface SourceCreate {
    url: string;
    title: string;
    description?: string;
    source_type: string;
  }
  
  export interface SourceUpdate {
    url?: string;
    title?: string;
    description?: string;
    source_type?: string;
    credibility_score?: number;
  }
  
  // Topic types
  export interface Topic {
    id: number;
    name: string;
    description: string | null;
    search_count: number;
    created_at: string;
    updated_at: string | null;
    last_searched_at: string | null;
  }
  
  export interface TopicSearchRequest {
    topic: string;
    max_articles?: number;
  }
  
  export interface TopicSearchResponse {
    topic: Topic;
    is_new: boolean;
    articles_found: number;
    articles_stored: number;
    sources_found: number;
    sources_stored: number;
    errors: string[];
  }
  
  // Article types
  export interface Article {
    id: number;
    title: string;
    url: string;
    description: string | null;
    content: string | null;
    author: string | null;
    published_at: string | null;
    image_url: string | null;
    source_id: number | null;
    source_name: string | null;
    credibility_score: number | null;
    sentiment_score: number | null;
    sentiment_label: string | null;
    sentiment_confidence: number | null;
    political_bias_score: number | null;
    political_bias_label: string | null;
    sensationalism_score: number | null;
    sensationalism_label: string | null;
    bias_scores: Record<string, any> | null;
    created_at: string;
    updated_at: string | null;
    last_analyzed_at: string | null;
  }
  
  export interface ArticleList {
    items: Article[];
    total: number;
    page: number;
    size: number;
    pages: number;
  }
  
  // Error type
  export interface ApiError {
    detail: string;
  }