//import React from 'react';
import AppRouter from './router';
import { SourceProvider } from './context/SourceContext';
import './index.css';

function App() {
  return (
    <SourceProvider>
      <AppRouter />
    </SourceProvider>
  );
}

export default App;
