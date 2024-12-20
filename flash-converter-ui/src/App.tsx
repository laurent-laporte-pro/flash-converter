import flashConverterLogo from '/flash-converter-icon.png'
import './App.css'
import { VideoTask } from './types/video-tasks/videoTask.ts'
import VideoTaskList from './components/video-tasks/VideoTaskList.tsx'
import { useEffect, useState } from 'react'
import { loadTasksFromStorage, saveTasksToStorage } from './store/video-tasks/videoTasksStore.ts'

function App () {
  const [videoTasks, setVideoTasks] = useState<VideoTask[]>([])

  useEffect(() => {
    // fetch the tasks from the local storage
    const tasks = loadTasksFromStorage()

    // If empty, use the default list and save it to the local storage
    if (tasks.length === 0) {
      const defaultTasks: VideoTask[] = [
        { videoName: 'video1.mp4', taskID: 'task_001', taskStatus: 'PENDING' },
        { videoName: 'video2.mp4', taskID: 'task_002', taskStatus: 'STARTED' },
        { videoName: 'video3.mp4', taskID: 'task_003', taskStatus: 'RETRY' },
        { videoName: 'video4.mp4', taskID: 'task_004', taskStatus: 'FAILURE' },
        { videoName: 'video5.mp4', taskID: 'task_005', taskStatus: 'SUCCESS' },
      ]
      setVideoTasks(defaultTasks)
      saveTasksToStorage(defaultTasks)
    } else {
      setVideoTasks(tasks)
    }
  }, [])

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
        <VideoTaskList tasks={videoTasks} />
      </div>
    </>
  )
}

export default App
