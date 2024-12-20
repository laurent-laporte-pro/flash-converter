/**
 * Ce composant est utilisé pour afficher la liste des tâches de conversion vidéo.
 */

import React from 'react'
import { VideoTask } from '../../types/video-tasks/videoTask.ts'

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
      <table>
        <thead>
        <tr>
          <th>Video</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        {tasks.map((task: VideoTask) => (
          <tr key={task.taskID}>
            <td>{task.videoName}</td>
            <td>{task.taskStatus}</td>
          </tr>
        ))}
        </tbody>
      </table>
    )}  </div>
)

export default VideoTaskList
