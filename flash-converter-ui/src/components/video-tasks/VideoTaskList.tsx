/**
 * Ce composant est utilisé pour afficher la liste des tâches de conversion vidéo.
 */

import { VideoTask } from '../../types/video-tasks/videoTask.ts'

/**
 * VideoTaskList component displays a list of video conversion tasks.
 *
 * @param tasks - The list of video tasks.
 * @constructor
 */
export const VideoTaskList = ({ tasks }: { tasks: VideoTask[] }) => (
  <div>
    <h2>Video Tasks</h2>
    {tasks.length === 0 ? (
      <p>Aucune tâche de conversion.</p>
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
              ) : '–'}
            </td>
          </tr>
        ))}
        </tbody>
      </table>
    )}
  </div>
)

export default VideoTaskList
