import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface Voter {
  serial_no?: string;
  name?: string;
  voter_id?: string;
  father_name?: string;
  mother_name?: string;
  occupation?: string;
  date_of_birth?: string;
  address?: string;
  district?: string;
  upazila?: string;
  union?: string;
  ward_number?: string;
  voter_area?: string;
  voter_area_code?: string;
}

export interface ExtractionResult {
  job_id: string;
  status: string;
  total_voters: number;
  data: Voter[];
}

export interface Metadata {
  district: string;
  upazila: string;
  union: string;
  ward_number: string;
  voter_area: string;
  voter_area_code: string;
}

export const uploadPDF = async (file: File, metadata: Metadata): Promise<ExtractionResult> => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('district', metadata.district);
  formData.append('upazila', metadata.upazila);
  formData.append('union', metadata.union);
  formData.append('ward_number', metadata.ward_number);
  formData.append('voter_area', metadata.voter_area);
  formData.append('voter_area_code', metadata.voter_area_code);

  const response = await axios.post<ExtractionResult>(`${API_BASE_URL}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};
