/**
 * Test the videoTasksStore module.
 *
 * Use Vitest to test the videoTasksStore module.
 */

import { saveTasksToStorage, loadTasksFromStorage } from './videoTasksStore'
import { VideoTask } from '../../types/video-tasks/videoTask'
import { describe, it, expect } from 'vitest'

describe('videoTasksStore', () => {
  const task1: VideoTask = { videoName: 'video1.mp4', taskId: '75cb2396-8158-4907-98cb-60348d15d967', taskStatus: 'PENDING' }
  const task2: VideoTask = { videoName: 'video2.mp4', taskId: 'fa4d622a-d5bc-49a3-a7e6-4021af0f48f2', taskStatus: 'STARTED' }
  const task3: VideoTask = { videoName: 'video3.mp4', taskId: '8dba3398-6d82-484e-9025-24b92a6fc7d3', taskStatus: 'RETRY' }
  const task4: VideoTask = { videoName: 'video4.mp4', taskId: '4767b64a-6963-422c-ba90-a111d745f6cd', taskStatus: 'FAILURE' }
  const task5: VideoTask = { videoName: 'video5.mp4', taskId: '093320c7-6bb1-4c51-8787-f8bbdf3a5e51', taskStatus: 'SUCCESS' }

  it('should save and load tasks', () => {
    const tasks: VideoTask[] = [task1, task2, task3, task4, task5]

    saveTasksToStorage(tasks)

    const loadedTasks = loadTasksFromStorage()

    expect(loadedTasks).toEqual(tasks)
  })

  it('should return an empty array if the storage is empty', () => {
    localStorage.clear()

    const loadedTasks = loadTasksFromStorage()

    expect(loadedTasks).toEqual([])
  })

  it('should return an empty array if the storage contains invalid data', () => {
    localStorage.setItem('flash-converter__video-tasks', 'invalid data')

    const loadedTasks = loadTasksFromStorage()

    expect(loadedTasks).toEqual([])
  })
})
