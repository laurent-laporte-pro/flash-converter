import flashConverterLogo from '/flash-converter-icon.png'
import './App.css'
import VideoTaskList from './components/video-tasks/VideoTaskList.tsx'
import { useVideoTasks } from './store/video-tasks/useVideoTasks.ts'
import { VideoTask } from './types/video-tasks/videoTask.ts'
import { videoProcessingService } from './api/video-tasks/service.ts'
import { useEffect, useState } from 'react'

function App () {
  const [videoFile, setVideoFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [uploadError, setUploadError] = useState('')
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

  const handleVideoFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setVideoFile(event.target.files[0])
    } else {
      setVideoFile(null)
    }
  }

  const handleUpload = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!videoFile) return
    setUploading(true)
    setUploadError('')
    try {
      const taskId = await videoProcessingService.createTask(videoFile)
      const videoTask: VideoTask = { taskId, videoName: videoFile.name, taskStatus: 'PENDING' }
      actions.createTask(videoTask)
      const formElement = event.target as HTMLFormElement
      formElement.reset()
      setVideoFile(null)
    } catch (error) {
      if (error instanceof Error) {
        setUploadError(error.message)
      } else {
        setUploadError(`An error occurred: ${error}`)
      }
    } finally {
      setUploading(false)
    }
  }

  return (
    <>
      <div><img src={flashConverterLogo} className="logo" alt="Flash Converter Logo" /></div>
      <h2>Téléchargez une vidéo</h2>
      <div className="card">
        <form className="card" onSubmit={handleUpload}>
          <input type={'file'} placeholder={'Téléchargez une vidéo'} accept="video/*"
                 onChange={handleVideoFileChange} />
          <button type="submit" disabled={uploading}>Télécharger</button>
          <FileInfo file={videoFile} />
          <UploadError error={uploadError} />
        </form>
      </div>
      <div className="card">
        <VideoTaskList tasks={tasks} />
      </div>
    </>
  )
}

function humanFileSize (size: number, digits: number = 2): string {
  const order = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024))
  const converted = size / Math.pow(1024, order)
  const unit = ['o', 'ko', 'Mo', 'Go', 'To'][order]
  const formatter = new Intl.NumberFormat('fr-FR', { minimumFractionDigits: digits, maximumFractionDigits: digits })
  return `${formatter.format(converted)} ${unit}`
}

function FileInfo ({ file }: { file: File | null }) {
  if (!file) return null
  return (
    <p>
      <span>🎥 fichier <strong>{file.type}</strong> sélectionné</span> <span>({humanFileSize(file.size)})</span>
    </p>
  )
}

function UploadError ({ error }: { error: string }) {
  if (!error) return null
  return <p style={{ color: 'red' }}>{error}</p>
}

export default App
