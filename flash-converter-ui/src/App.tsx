import flashConverterLogo from '/flash-converter-icon.png'
import './App.css'
import VideoTaskList from './components/video-tasks/VideoTaskList.tsx'
import { useVideoTasks } from './store/video-tasks/useVideoTasks.ts'
import { VideoTask } from './types/video-tasks/videoTask.ts'
import { videoProcessingService } from './api/video-tasks/service.ts'
import { useEffect } from 'react'

function App () {
  const { state, actions } = useVideoTasks()
  const tasks = state.tasks

  const updateTaskStatus = async (videoTask: VideoTask) => {
    if (videoTask.taskStatus === 'PENDING' || videoTask.taskStatus === 'STARTED' || videoTask.taskStatus === 'RETRY') {
      try {
        const status = await videoProcessingService.getTaskStatus(videoTask.taskId)
        actions.updateTaskStatus(videoTask.taskId, status)
      } catch (error) {
        if (error instanceof Error) {
          actions.updateTaskError(videoTask.taskId, error.message)
        } else {
          actions.updateTaskError(videoTask.taskId, `An error occurred: ${error}`)
        }
      }
    }
  }

  // Pooling of the tasks in PENDING or PROCESSING status, every second
  useEffect(() => {
    const interval = setInterval(async () => state.tasks.forEach(updateTaskStatus), 1000)
    return () => clearInterval(interval)
  }, [tasks, actions])

  return (
    <>
      <div>
        <img src={flashConverterLogo} className="logo" alt="Flash Converter Logo" />
      </div>
      <h1>Téléchargez une vidéo</h1>
      <div className="card">
        <input type={'file'} placeholder={'Téléchargez une vidéo'} accept="video/*" />
        <button>Convertir</button>
      </div>
      <div className="card">
        <VideoTaskList tasks={tasks} />
      </div>
    </>
  )
}

export default App
