/**
 * Ce composant est utilisé pour afficher la liste des tâches de conversion vidéo.
 */

import React from 'react'
import { VideoTask } from '../types/video-task.ts'

interface VideoTaskListProps {
  /**
   * List of video tasks to display.
   */
  tasks: VideoTask[];
}

export const VideoTaskList: React.FC<VideoTaskListProps> = ({ tasks }) => (
  <div>
    <h2>Video Tasks</h2>
    {tasks.length === 0 ? (
      <p>No conversion tasks.</p>
    ) : (
      <ul style={{ listStyleType: 'none' }}>
        {tasks.map((task: VideoTask) => (
          <li key={task.taskID}>
            {task.videoName} - {task.taskStatus}
          </li>
        ))}
      </ul>
    )}  </div>
)

export default VideoTaskList
