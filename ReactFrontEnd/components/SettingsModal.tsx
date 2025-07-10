
import React, { useState, useEffect, FormEvent } from 'react';
import { ConfigData } from '../types';

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  config: ConfigData;
  onSave: (newConfig: ConfigData) => void;
}

const SettingsModal: React.FC<SettingsModalProps> = ({ isOpen, onClose, config, onSave }) => {
  const [currentConfig, setCurrentConfig] = useState<ConfigData>(config);

  useEffect(() => {
    setCurrentConfig(config);
  }, [config]);

  if (!isOpen) {
    return null;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCurrentConfig(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSave(currentConfig);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-70 flex justify-center items-center z-50" onClick={onClose}>
      <div className="bg-gray-700 rounded-lg shadow-xl p-6 w-full max-w-md" onClick={e => e.stopPropagation()}>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-white">Settings</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white">&times;</button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="savePath" className="block text-sm font-medium text-gray-300 mb-1">Save Path</label>
              <input
                type="text"
                id="savePath"
                name="savePath"
                value={currentConfig.savePath}
                onChange={handleChange}
                placeholder="e.g., C:\\SavedData"
                className="w-full bg-gray-600 border border-gray-500 rounded-md p-2 text-white focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label htmlFor="backPath" className="block text-sm font-medium text-gray-300 mb-1">Scanner Back ID Path</label>
              <input
                type="text"
                id="backPath"
                name="backPath"
                value={currentConfig.backPath}
                onChange={handleChange}
                placeholder="e.g., C:\\Scanner\\Back"
                className="w-full bg-gray-600 border border-gray-500 rounded-md p-2 text-white focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label htmlFor="frontPath" className="block text-sm font-medium text-gray-300 mb-1">Scanner Front ID Path</label>
              <input
                type="text"
                id="frontPath"
                name="frontPath"
                value={currentConfig.frontPath}
                onChange={handleChange}
                placeholder="e.g., C:\\Scanner\\Front"
                className="w-full bg-gray-600 border border-gray-500 rounded-md p-2 text-white focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          <div className="mt-6 flex justify-end">
            <button type="submit" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-md transition duration-300">
              Save Config
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SettingsModal;
