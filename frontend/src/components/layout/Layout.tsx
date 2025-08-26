import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';
import { BackendStatusBanner } from '../BackendStatusBanner';

export default function Layout() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Backend status banner at the top */}
      <BackendStatusBanner />
      
      <Header />
      <main className="flex-grow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Outlet />
        </div>
      </main>
      <Footer />
    </div>
  );
}
