import React, { useState, useCallback, useEffect } from 'react';
import { IDData, ConfigData, CardSide, FrontApiResponse, BackApiResponse } from '../types';
import { uploadAndProcessImage, saveIdData, saveConfig } from '../services/OCRService';
import Layout from '../components/Layout';
import IdCardSection from '../components/IdCardSection';
import SettingsModal from '../components/SettingsModal';
import Spinner from '../components/Spinner';

const IDExtractorPage: React.FC = () => {
    const initialIdData: IDData = {
        name: '', address: '', idNumber: '', dob: '',
        profession: '', gender: '', maritalStatus: '',
        religion: '', expiryDate: '', husbandName: '',
    };
    
    const [idData, setIdData] = useState<IDData>(initialIdData);
    const [config, setConfig] = useState<ConfigData>({ savePath: '', backPath: '', frontPath: '' });
    const [loadingSide, setLoadingSide] = useState<CardSide | null>(null);
    const [error, setError] = useState<string>('');
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);
    const [frontImagePreview, setFrontImagePreview] = useState<string | null>(null);
    const [backImagePreview, setBackImagePreview] = useState<string | null>(null);
    const [faceImagePreview, setFaceImagePreview] = useState<string | null>(null);
    const [threshold, setThreshold] = useState<number>(110);

    useEffect(() => {
        try {
            const savedConfig = localStorage.getItem('idExtractorConfig');
            if (savedConfig) {
                setConfig(JSON.parse(savedConfig));
            }
        } catch (e) {
            console.error("Failed to load config from localStorage", e);
        }
    }, []);

    const handleDataChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setIdData(prev => ({ ...prev, [name]: value }));
    }, []);

    const handleImageUpload = async (file: File, side: CardSide) => {
        setLoadingSide(side);
        setError('');
        
        if (side === 'front') {
            // Clear all previous data when new front is uploaded
            setIdData(initialIdData);
            setBackImagePreview(null);
            setFaceImagePreview(null);
        }
        
        try {
            const result = await uploadAndProcessImage(file, side, threshold);
            
            if (side === 'front' && result) {
                const frontData = result as FrontApiResponse;
                setIdData(prev => ({
                    ...initialIdData, // Start fresh
                    name: frontData.name, 
                    address: frontData.address, 
                    idNumber: frontData.ID, 
                    dob: frontData.DOB 
                }));
                setFrontImagePreview(`data:image/jpeg;base64,${frontData.image}`);
                setFaceImagePreview(`data:image/jpeg;base64,${frontData.face}`);
            } else if (side === 'back' && result) {
                const backData = result as BackApiResponse;
                setIdData(prev => ({
                    ...prev, 
                    profession: backData.profession, 
                    gender: backData.gender, 
                    maritalStatus: backData.marital_status, 
                    religion: backData.religion, 
                    expiryDate: backData.enddate, 
                    husbandName: backData.husband_name || ''
                }));
                setBackImagePreview(`data:image/jpeg;base64,${backData.image}`);
            }
        } catch (err: any) {
            setError(err.message || 'An unknown error occurred.');
        } finally {
            setLoadingSide(null);
        }
    };

    const handleSaveData = async () => {
        if (!idData.idNumber) {
            alert('Cannot save. Please process an ID card first.');
            return;
        }
        try {
            await saveIdData(idData);
            alert('Data saved successfully!');
            // Reset state after saving
            setIdData(initialIdData);
            setFrontImagePreview(null);
            setBackImagePreview(null);
            setFaceImagePreview(null);
        } catch(err: any) {
            alert(`Saving Failed: ${err.message}`);
        }
    };

    const handleConfigSave = async (newConfig: ConfigData) => {
        setIsSettingsOpen(false);
        try {
            await saveConfig(newConfig);
            setConfig(newConfig);
            localStorage.setItem('idExtractorConfig', JSON.stringify(newConfig));
            alert('Configuration saved successfully to backend and localStorage.');
        } catch (err: any) {
             alert(`Failed to save configuration: ${err.message}`);
        }
    };

    return (
        <Layout onSettingsClick={() => setIsSettingsOpen(true)}>
            <div className="p-4 md:p-8">
                {error && <div className="bg-red-500 text-white p-3 rounded-md mb-6 text-center">{error}</div>}

                <div className="mb-6 bg-gray-700 p-4 rounded-lg shadow-lg max-w-md mx-auto">
                    <label htmlFor="thresholdSlider" className="block text-white text-center font-medium mb-2">
                        Set Threshold: <span className="font-bold text-lg text-blue-400">{threshold}</span>
                    </label>
                    <input
                        type="range"
                        id="thresholdSlider"
                        min="0"
                        max="255"
                        value={threshold}
                        onChange={(e) => setThreshold(Number(e.target.value))}
                        className="w-full h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer accent-blue-500"
                    />
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <IdCardSection
                        title="Front ID"
                        side="front"
                        onImageUpload={handleImageUpload}
                        data={idData}
                        onDataChange={handleDataChange}
                        isLoading={loadingSide === 'front'}
                        imagePreview={frontImagePreview}
                        faceImagePreview={faceImagePreview}
                    />
                    <IdCardSection
                        title="Back ID"
                        side="back"
                        onImageUpload={handleImageUpload}
                        data={idData}
                        onDataChange={handleDataChange}
                        isLoading={loadingSide === 'back'}
                        imagePreview={backImagePreview}
                    />
                </div>

                <div className="mt-8 flex justify-center">
                    <button 
                        onClick={handleSaveData}
                        className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-lg shadow-lg transition duration-300 transform hover:scale-105 disabled:bg-gray-500 disabled:cursor-not-allowed"
                        disabled={loadingSide !== null || !idData.idNumber}
                    >
                        {loadingSide ? <Spinner/> : 'Save Data'}
                    </button>
                </div>
            </div>
            <SettingsModal 
                isOpen={isSettingsOpen} 
                onClose={() => setIsSettingsOpen(false)}
                config={config}
                onSave={handleConfigSave}
            />
        </Layout>
    );
};

export default IDExtractorPage;
