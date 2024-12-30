import flashConverterLogo from '/flash-converter-icon.png'
import './App.css'
import VideoTaskList from './components/video-tasks/VideoTaskList.tsx'
import { useVideoTasks } from './store/video-tasks/useVideoTasks.ts'
import { VideoTask } from './types/video-tasks/videoTask.ts'
import { videoProcessingService } from './api/video-tasks/service.ts'
import { useEffect } from 'react'
import UploadForm from './components/video-tasks/UploadForm.tsx'

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

  useEffect(() => {
    const interval = setInterval(async () => state.tasks.forEach(updateTaskStatus), 5000)
    return () => clearInterval(interval)
  }, [tasks, actions])

  const handleDownload = (task: VideoTask) => {
    try {
      videoProcessingService.getTaskResult(task.taskId).then()
    } catch (error) {
      if (error instanceof Error) {
        actions.updateTaskError(task.taskId, error.message)
      } else {
        actions.updateTaskError(task.taskId, `An error occurred: ${error}`)
      }
    }
  }

  return (
    <>
      <div><img src={flashConverterLogo} className="logo" alt="Flash Converter Logo" /></div>
      <h2>Téléchargez une vidéo</h2>
      <div className="card">
        <UploadForm appendTask={actions.appendTask} />
      </div>
      <div className="card">
        <VideoTaskList tasks={tasks} handleDownload={handleDownload} />
      </div>
    </>
  )
}

export default App
