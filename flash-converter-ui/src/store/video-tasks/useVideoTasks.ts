/**
 * Ce hook permet de gérer les tâches de conversion de vidéos
 * depuis le videoTasksReducer.
 */
import { useCallback, useEffect, useReducer } from 'react'
import { videoTasksReducer, VideoTasksState } from './videoTasksReducer.ts'
import { loadTasksFromStorage } from './videoTasksStore.ts'
import { TaskId, TaskStatus, VideoTask } from '../../types/video-tasks/videoTask.ts'

const INITIAL_STATE: VideoTasksState = {
  tasks: []
}

export const useVideoTasks = () => {
  const [state, dispatch] = useReducer(videoTasksReducer, INITIAL_STATE)

  useEffect(() => {
    const tasks = loadTasksFromStorage()
    dispatch({ type: 'LOAD_TASKS', payload: tasks })
  }, [])

  const appendTask = (task: VideoTask) => {
    dispatch({ type: 'APPEND_TASK', payload: task })
  }

  const deleteTask = (taskId: TaskId) => {
    dispatch({ type: 'DELETE_TASK', payload: taskId })
  }

  const updateTaskStatus = (taskId: TaskId, taskStatus: TaskStatus) => {
    dispatch({ type: 'UPDATE_TASK_STATUS', payload: { taskId, taskStatus } })
  }

  const updateTaskError = (taskId: TaskId, errorMessage: string) => {
    dispatch({ type: 'UPDATE_TASK_ERROR', payload: { taskId, errorMessage } })
  }

  return {
    state,
    actions: {
      appendTask: useCallback(appendTask, []),
      deleteTask: useCallback(deleteTask, []),
      updateTaskStatus: useCallback(updateTaskStatus, []),
      updateTaskError: useCallback(updateTaskError, []),
    }
  }
}
