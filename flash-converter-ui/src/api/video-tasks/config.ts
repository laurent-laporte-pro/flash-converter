import axios from 'axios'
/// <reference types="node" />

export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 secondes
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})
