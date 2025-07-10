
import React from 'react';

interface FormFieldProps {
  label: string;
  labelArabic: string;
  id: string;
  name: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder: string;
  type?: string;
}

const FormField: React.FC<FormFieldProps> = ({
  label, labelArabic, id, name, value, onChange, placeholder, type = 'text'
}) => {
  return (
    <div>
      <label htmlFor={id} className="flex justify-between items-center text-sm font-medium text-gray-300 mb-1">
        <span>{label}</span>
        <span className="font-bold">{labelArabic}</span>
      </label>
      <input
        type={type}
        id={id}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="w-full bg-gray-800 border border-gray-600 rounded-md p-2 text-white focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />
    </div>
  );
};

export default FormField;
