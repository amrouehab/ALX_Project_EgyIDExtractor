import { IDData, ConfigData, CardSide, FrontApiResponse, BackApiResponse } from '../types';

const BASE_URL = 'http://127.0.0.1:5000';

const getApiSide = (side: CardSide): 'F' | 'B' => {
    return side === 'front' ? 'F' : 'B';
};
    
async function handleApiResponse(response: Response) {
    if (!response.ok) {
        const errorText = await response.text().catch(() => 'Could not read error response.');
        throw new Error(`API Error: ${response.status} - ${errorText}`);
    }
    // The original backend often returns a JSON string, so we parse it manually.
    const text = await response.text();
    try {
        return JSON.parse(text);
    } catch(e){
        console.error("Failed to parse API response JSON:", text);
        throw new Error("Received an invalid response from the server.");
    }
}


export const uploadAndProcessImage = async (
    file: File,
    side: CardSide,
    threshold: number
): Promise<FrontApiResponse | BackApiResponse> => {
    const apiSide = getApiSide(side);
    const formData = new FormData();
    formData.append('image', file);

    const requestUrl = `${BASE_URL}/recognize-text/${apiSide}/${threshold}`;

    try {
        const response = await fetch(requestUrl, {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Accept': 'application/json',
            },
            body: formData,
        });
        return handleApiResponse(response);
    } catch (error) {
        console.error("Error uploading and processing image:", error);
        throw new Error("Failed to process image. Is the backend server running at http://127.0.0.1:5000?");
    }
};

export const saveIdData = async (data: IDData): Promise<any> => {
    const apiData = {
        Name: data.name,
        Address: data.address,
        NationalID: data.idNumber,
        DOB: data.dob,
        Profision: data.profession,
        Gender: data.gender,
        MartialStat: data.maritalStatus,
        Religion: data.religion,
        EndDate: data.expiryDate,
        Husband_name: data.husbandName,
    };

    const requestUrl = `${BASE_URL}/save`;

    try {
        const response = await fetch(requestUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(apiData),
        });
        return handleApiResponse(response);
    } catch (error) {
        console.error("Error saving data:", error);
        throw error;
    }
};

export const saveConfig = async (config: ConfigData): Promise<any> => {
    const requestUrl = `${BASE_URL}/save-config`;
    try {
        const response = await fetch(requestUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config),
        });
        return handleApiResponse(response);
    } catch (error) {
        console.error("Error saving config:", error);
        throw new Error("Failed to save config on the backend.");
    }
};
