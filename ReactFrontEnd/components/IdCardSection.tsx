import React, { useRef } from 'react';
import { IDData, CardSide } from '../types';
import FormField from './FormField';
import Spinner from './Spinner';

interface IdCardSectionProps {
  title: string;
  side: CardSide;
  onImageUpload: (file: File, side: CardSide) => void;
  data: IDData;
  onDataChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  isLoading: boolean;
  imagePreview: string | null;
  faceImagePreview?: string | null;
}

const IdCardSection: React.FC<IdCardSectionProps> = ({
  title, side, onImageUpload, data, onDataChange, isLoading, imagePreview, faceImagePreview
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onImageUpload(file, side);
    }
    e.target.value = ''; // Reset file input
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="bg-gray-700 p-6 rounded-lg shadow-lg flex flex-col">
      <h3 className="text-xl font-bold mb-4 text-center text-white">{title}</h3>
      <div className="mb-4">
        <button
          onClick={handleUploadClick}
          className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-md transition duration-300"
          disabled={isLoading}
        >
          {isLoading ? <Spinner/> : `Upload ${title} Image`}
        </button>
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          className="hidden"
          accept="image/png, image/jpeg"
        />
      </div>

      <div className={`grid gap-4 mb-4 ${side === 'front' ? 'grid-cols-2' : 'grid-cols-1'}`}>
          <div className="imageContainer h-48 bg-gray-800 rounded-md flex items-center justify-center border-2 border-dashed border-gray-500 overflow-hidden">
            {isLoading && side === 'front' ? (
              <Spinner />
            ) : imagePreview ? (
              <img src={imagePreview} alt={`${title} preview`} className="h-full w-full object-contain" />
            ) : (
              <span className="text-gray-500">Image Preview</span>
            )}
          </div>
          
          {side === 'front' && (
              <div 
                className="faceImageBox h-48 bg-gray-800 rounded-md flex items-center justify-center border-2 border-dashed border-gray-500 bg-cover bg-center overflow-hidden"
                style={{ backgroundImage: faceImagePreview ? `url(${faceImagePreview})` : 'none' }}
              >
                  {isLoading && <Spinner />}
                  {!faceImagePreview && !isLoading && <span className="text-gray-500">Face Preview</span>}
              </div>
          )}
      </div>

      <div className="space-y-4">
        {side === 'front' ? (
          <>
            <FormField label="Name" labelArabic="الاسم" id="name" name="name" value={data.name} onChange={onDataChange} placeholder="Name" />
            <FormField label="Address" labelArabic="العنوان" id="address" name="address" value={data.address} onChange={onDataChange} placeholder="Address" />
            <FormField label="National ID" labelArabic="الرقم القومي" id="idNumber" name="idNumber" value={data.idNumber} onChange={onDataChange} placeholder="ID Number" />
            <FormField label="Date of Birth" labelArabic="تاريخ الميلاد" id="dob" name="dob" value={data.dob} onChange={onDataChange} placeholder="YYYY-MM-DD" />
          </>
        ) : (
          <>
            <FormField label="Profession" labelArabic="المهنة" id="profession" name="profession" value={data.profession} onChange={onDataChange} placeholder="Profession" />
            <FormField label="Gender" labelArabic="النوع" id="gender" name="gender" value={data.gender} onChange={onDataChange} placeholder="Gender" />
            <FormField label="Marital Status" labelArabic="الحالة الاجتماعية" id="maritalStatus" name="maritalStatus" value={data.maritalStatus} onChange={onDataChange} placeholder="Marital Status" />
            <FormField label="Religion" labelArabic="الديانة" id="religion" name="religion" value={data.religion} onChange={onDataChange} placeholder="Religion" />
            <FormField label="Expiry Date" labelArabic="صالحة حتى" id="expiryDate" name="expiryDate" value={data.expiryDate} onChange={onDataChange} placeholder="YYYY-MM-DD" />
            {data.husbandName && (
                 <FormField label="Husband's Name" labelArabic="اسم الزوج" id="husbandName" name="husbandName" value={data.husbandName} onChange={onDataChange} placeholder="Husband's Name" />
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default IdCardSection;
