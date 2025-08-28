export interface SearchResult {
  title: string;
  url: string;
  source: 'forums' | 'docs' | 'tickets';
  snippet: string;
  updated_at: string;
  breadcrumb?: string;
  author?: string;
  tags?: string[];
  score?: number;
}

export interface Citation {
  id: number;
  title: string;
  url: string;
  source: 'forums' | 'docs' | 'tickets';
  snippet?: string;
}

export interface SearchResponse {
  query: string;
  answer?: string;
  citations: Citation[];
  results: SearchResult[];
  did_you_mean?: string;
  total_results: number;
  search_time_ms: number;
  filters: {
    source: string[];
    time: string[];
  };
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  citations?: Citation[];
  tools_used?: string[];
}

export interface ChatSession {
  id: string;
  messages: ChatMessage[];
  created_at: Date;
  updated_at: Date;
}

export interface SearchFilters {
  sources: ('forums' | 'docs' | 'tickets')[];
  timeRange: 'any' | 'past_week' | 'past_month' | 'past_year';
  sortBy: 'relevance' | 'date' | 'source';
}

export interface SearchSuggestion {
  text: string;
  type: 'query' | 'completion';
  source?: string;
  highlight?: number[];
}

export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  groups: string[];
  permissions: string[];
  is_admin?: boolean;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  token?: string;
}

export interface SearchState {
  query: string;
  results: SearchResult[];
  isLoading: boolean;
  error: string | null;
  filters: SearchFilters;
  activeTab: 'all' | 'forums' | 'docs' | 'tickets' | 'ai-deeper';
  totalResults: number;
  searchTime: number;
  suggestions: SearchSuggestion[];
}

export interface ChatState {
  currentSession: ChatSession | null;
  sessions: ChatSession[];
  isLoading: boolean;
  error: string | null;
  isStreaming: boolean;
}

// API Error types
export interface ApiError {
  message: string;
  code?: string;
  details?: Record<string, any>;
}

// Component prop types
export interface SearchInputProps {
  onSearch: (query: string) => void;
  onSuggestionSelect: (suggestion: SearchSuggestion) => void;
  value: string;
  onChange: (value: string) => void;
  suggestions: SearchSuggestion[];
  isLoading: boolean;
  placeholder?: string;
}

export interface SearchResultsProps {
  results: SearchResult[];
  query: string;
  totalResults: number;
  searchTime: number;
  isLoading: boolean;
  error: string | null;
  onLoadMore?: () => void;
  hasMore?: boolean;
}

export interface ChatInterfaceProps {
  session: ChatSession | null;
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  error: string | null;
  isStreaming: boolean;
}

export interface FilterPanelProps {
  filters: SearchFilters;
  onFiltersChange: (filters: SearchFilters) => void;
  resultCounts: Record<string, number>;
}

// Configuration types
export interface AppConfig {
  apiBaseUrl: string;
  googleClientId: string;
  features: {
    grokPrivate: boolean;
    openSearch: boolean;
    debugPrompts: boolean;
  };
  search: {
    maxResults: number;
    defaultResults: number;
    suggestionsCount: number;
  };
  chat: {
    maxHistory: number;
    streamingEnabled: boolean;
  };
}
