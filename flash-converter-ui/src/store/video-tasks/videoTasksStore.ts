/**
 * This module contains the logic to save and load video tasks from the local storage.
 */
import { VideoTask } from '../../types/video-tasks/videoTask.ts'

const STORAGE_KEY = 'flash-converter__video-tasks'

/**
 * Save the given tasks to the local storage.
 * @param tasks The tasks to save.
 */
export const saveTasksToStorage = (tasks: VideoTask[]) => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(tasks))
}

/**
 * Load the tasks from the local storage.
 * @returns The loaded tasks.
 */
export const loadTasksFromStorage = (): VideoTask[] => {
  const stored = localStorage.getItem(STORAGE_KEY)
  try {
    return stored ? JSON.parse(stored) : []
  } catch (error) {
    console.error('Failed to load tasks from storage:', error)
    return []
  }
}
