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
          <th>Status</th>
          <th>Message</th>
        </tr>
        </thead>
        <tbody>
        {tasks.map((task: VideoTask) => (
          <tr key={task.taskId}>
            <td>{task.videoName}</td>
            <td>{task.taskStatus}</td>
            <td>
              {task.errorMessage ? (
                <span style={{ color: 'red' }}>{task.errorMessage}</span>
              ) : "–"}
            </td>
          </tr>
        ))}
        </tbody>
      </table>
    )}  </div>
)

export default VideoTaskList
