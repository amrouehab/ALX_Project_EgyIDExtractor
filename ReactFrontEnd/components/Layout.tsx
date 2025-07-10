
import React, { ReactNode } from 'react';
import Header from './Header';

interface LayoutProps {
  children: ReactNode;
  onSettingsClick: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, onSettingsClick }) => {
  return (
    <div className="min-h-screen bg-gray-800">
      <Header onSettingsClick={onSettingsClick} />
      <main className="container mx-auto px-4 py-6">
        {children}
      </main>
    </div>
  );
};

export default Layout;
