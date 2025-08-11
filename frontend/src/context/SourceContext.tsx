import React, { createContext, useContext, useState, useEffect, type ReactNode } from 'react';
import type { Source, SourceCreate, SourceUpdate } from '../types/api';
import { sourceApi } from '../services/api';

// Define context type
interface SourceContextType {
  sources: Source[];
  loading: boolean;
  error: string | null;
  fetchSources: () => Promise<void>;
  createSource: (source: SourceCreate) => Promise<Source | null>;
  updateSource: (id: number, source: SourceUpdate) => Promise<Source | null>;
  deleteSource: (id: number) => Promise<boolean>;
}

// Create context with default values
const SourceContext = createContext<SourceContextType>({
  sources: [],
  loading: false,
  error: null,
  fetchSources: async () => {},
  createSource: async () => null,
  updateSource: async () => null,
  deleteSource: async () => false,
});

// Create provider component
export const SourceProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch all sources
  const fetchSources = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await sourceApi.getSources();
      setSources(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  // Create a new source
  const createSource = async (source: SourceCreate): Promise<Source | null> => {
    try {
      setLoading(true);
      setError(null);
      const newSource = await sourceApi.createSource(source);
      setSources(prev => [...prev, newSource]);
      return newSource;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Update a source
  const updateSource = async (id: number, source: SourceUpdate): Promise<Source | null> => {
    try {
      setLoading(true);
      setError(null);
      const updatedSource = await sourceApi.updateSource(id, source);
      setSources(prev => prev.map(s => s.id === id ? updatedSource : s));
      return updatedSource;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      return null;
    } finally {
      setLoading(false);
    }
  };

  // Delete a source
  const deleteSource = async (id: number): Promise<boolean> => {
    try {
      setLoading(true);
      setError(null);
      
      // Call the API to delete the source
      await sourceApi.deleteSource(id);
      
      // If the API call was successful (didn't throw an error), then we consider it a success
      setSources(prev => prev.filter(s => s.id !== id));
      
      return true;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // Initial load of sources
  useEffect(() => {
    fetchSources();
  }, []);

  // Provide context value
  const contextValue: SourceContextType = {
    sources,
    loading,
    error,
    fetchSources,
    createSource,
    updateSource,
    deleteSource,
  };

  return (
    <SourceContext.Provider value={contextValue}>
      {children}
    </SourceContext.Provider>
  );
};

// Custom hook for using the source context
export const useSources = () => useContext(SourceContext);