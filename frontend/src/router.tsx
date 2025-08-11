import React from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

// Layout and pages
import Layout from './components/layout/Layout';
import Dashboard from './pages/Dashboard';
import Search from './pages/Search';
import About from './pages/About';
import TopicDetail from './pages/TopicDetail';

// Error page
const ErrorPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
        <svg className="w-16 h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Page Not Found</h1>
        <p className="text-gray-600 mb-4">The page you are looking for doesn't exist or has been moved.</p>
        <a href="/" className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded inline-block transition-colors">
          Go Home
        </a>
      </div>
    </div>
  );
};

// Create router
const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    errorElement: <ErrorPage />,
    children: [
      {
        index: true, // Default route
        element: <Dashboard />
      },
      {
        path: "search",
        element: <Search />
      },
      {
        path: "about",
        element: <About />
      },
      {
        path: "topics/:topicId",
        element: <TopicDetail />
      }
    ]
  }
]);

// Router component to be used in App.tsx
const AppRouter: React.FC = () => {
  return <RouterProvider router={router} />;
};

export default AppRouter;