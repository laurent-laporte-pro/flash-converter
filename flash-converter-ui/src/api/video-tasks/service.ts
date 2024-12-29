import { TaskId, TaskStatus } from '../../types/video-tasks/videoTask.ts'
import axios from 'axios'
import { apiClient } from './config.ts'
import { HTTPValidationError } from '../../types/common/errors.ts'

class VideoProcessingService {
  async createTask (videoFile: File): Promise<TaskId> {
    const formData = new FormData()
    formData.append('video', videoFile)

    try {
      const { data } = await apiClient.post<TaskId>('/tasks/', formData)
      return data
    } catch (error) {
      if (axios.isAxiosError<HTTPValidationError>(error)) {
        const defaultMsg = `Failed to create task: ${error.message}`
        throw new Error(error.response?.data.detail?.[0]?.msg || defaultMsg)
      }
      throw error
    }
  }

  async getTaskStatus (taskId: string): Promise<TaskStatus> {
    try {
      const { data } = await apiClient.get<TaskStatus>(`/tasks/${taskId}/status`)
      return data
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const defaultMsg = `Failed to get task status: ${error.message}`
        throw new Error(defaultMsg)
      }
      throw error
    }
  }

  async getTaskResult (taskId: string, timeout = 60): Promise<void> {
    try {
      // Use axios directly to get the response headers
      const response = await apiClient.get(`/tasks/${taskId}/result`, {
        params: { timeout },
        responseType: 'blob', // Important pour recevoir les données binaires
      })

      // Récupération du nom du fichier depuis les headers
      const contentDisposition = response.headers['content-disposition']
      let filename = 'video.mp4'

      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(.+)$/)
        if (filenameMatch) {
          filename = filenameMatch[1].replace(/["']/g, '')
        }
      }

      // Création d'une URL pour le blob
      const url = window.URL.createObjectURL(new Blob([response.data]))

      // Création d'un élément a temporaire pour le téléchargement
      const link = document.createElement('a')
      try {
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
      } finally {
        link.remove()
        window.URL.revokeObjectURL(url)
      }
    } catch (error) {
      if (axios.isAxiosError<HTTPValidationError>(error)) {
        const defaultMsg = `Failed to download video: ${error.message}`
        throw new Error(error.response?.data.detail?.[0]?.msg || defaultMsg)
      }
      throw error
    }
  }

  async revokeTask (taskId: string, timeout = 1): Promise<void> {
    try {
      await apiClient.delete(`/tasks/${taskId}`, {
        params: { timeout }
      })
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const defaultMsg = `Failed to revoke task: ${error.message}`
        throw new Error(defaultMsg)
      }
      throw error
    }
  }

  async checkHealth (): Promise<Record<string, string>> {
    try {
      const { data } = await apiClient.get<Record<string, string>>('/health/celery')
      return data
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const defaultMsg = `Failed to check health status: ${error.message}`
        throw new Error(defaultMsg)
      }
      throw error
    }
  }
}

export const videoProcessingService = new VideoProcessingService()
