import React from 'react';

const About: React.FC = () => {
  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">About BeInformed</h1>
      
      {/* Mission section */}
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Our Mission</h2>
        <p className="text-gray-700 mb-4">
          BeInformed aims to revolutionize information consumption by providing deep, nuanced, and transparent 
          analysis of complex topics through advanced AI-driven insights.
        </p>
        <p className="text-gray-700">
          In today's world of information overload, we believe that everyone deserves access to tools 
          that can help them understand the context, credibility, and nuances of the information they consume.
          Our platform bridges the gap between raw information and actionable knowledge.
        </p>
      </div>
      
      {/* Features section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Key Features</h2>
          <ul className="space-y-3">
            <li className="flex">
              <svg className="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <span className="font-medium text-gray-800">Multi-source information gathering</span>
                <p className="text-sm text-gray-600">Collect and analyze information from diverse sources</p>
              </div>
            </li>
            <li className="flex">
              <svg className="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <span className="font-medium text-gray-800">Semantic search capabilities</span>
                <p className="text-sm text-gray-600">Find information based on meaning, not just keywords</p>
              </div>
            </li>
            <li className="flex">
              <svg className="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <span className="font-medium text-gray-800">Multi-level summarization</span>
                <p className="text-sm text-gray-600">Get summaries tailored to different knowledge levels</p>
              </div>
            </li>
            <li className="flex">
              <svg className="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <span className="font-medium text-gray-800">Bias detection</span>
                <p className="text-sm text-gray-600">Identify potential biases in information sources</p>
              </div>
            </li>
            <li className="flex">
              <svg className="w-6 h-6 text-blue-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <span className="font-medium text-gray-800">Credibility scoring</span>
                <p className="text-sm text-gray-600">Evaluate the reliability of different sources</p>
              </div>
            </li>
          </ul>
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Our Technology</h2>
          <p className="text-gray-700 mb-4">
            BeInformed leverages cutting-edge artificial intelligence and natural language processing 
            to analyze information from multiple sources.
          </p>
          <p className="text-gray-700 mb-4">
            Our platform combines techniques from machine learning, information retrieval, and computational 
            linguistics to provide insights that would be difficult or time-consuming for humans to discover manually.
          </p>
          <div className="mt-6 space-y-4">
            <div className="flex items-center">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div>
                <h3 className="font-medium text-gray-800">Natural Language Processing</h3>
                <p className="text-sm text-gray-600">Understanding and analyzing human language</p>
              </div>
            </div>
            <div className="flex items-center">
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <div>
                <h3 className="font-medium text-gray-800">Machine Learning</h3>
                <p className="text-sm text-gray-600">Systems that learn and improve from experience</p>
              </div>
            </div>
            <div className="flex items-center">
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mr-4">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div>
                <h3 className="font-medium text-gray-800">Data Visualization</h3>
                <p className="text-sm text-gray-600">Making complex information accessible and understandable</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;