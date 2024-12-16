import flashConverterLogo from '/flash-converter-icon.png'
import './App.css'
import { VideoTask } from './types/video-task.ts'
import VideoTaskList from './components/VideoTaskList.tsx'

function App () {

  const videoTasks: VideoTask[] = [
    { videoName: 'video1.mp4', taskID: 'task_001', taskStatus: 'PENDING' },
    { videoName: 'video2.mp4', taskID: 'task_002', taskStatus: 'STARTED' },
    { videoName: 'video3.mp4', taskID: 'task_003', taskStatus: 'RETRY' },
    { videoName: 'video4.mp4', taskID: 'task_004', taskStatus: 'FAILURE' },
    { videoName: 'video5.mp4', taskID: 'task_005', taskStatus: 'SUCCESS' },
  ]

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
