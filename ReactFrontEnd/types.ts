export interface IDData {
  name: string;
  address: string;
  idNumber: string;
  dob: string;
  profession: string;
  gender: string;
  maritalStatus: string;
  religion: string;
  expiryDate: string;
  husbandName: string;
}

export interface ConfigData {
  savePath: string;
  backPath: string;
  frontPath: string;
}

export type CardSide = 'front' | 'back';

export interface FrontApiResponse {
    image: string; // base64
    face: string; // base64
    name: string;
    address: string;
    ID: string;
    DOB: string;
}

export interface BackApiResponse {
    image: string; // base64
    profession: string;
    gender: string;
    marital_status: string;
    religion: string;
    enddate: string;
    husband_name?: string;
}
