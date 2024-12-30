/**
 * Ce composant est utilisé pour afficher la liste des tâches de conversion vidéo.
 */

import { TaskStatus, VideoTask } from '../../types/video-tasks/videoTask.ts'

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
          <th>Actions</th>
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
            <td>
              <VideoTaskMenu task={task} />
            </td>
          </tr>
        ))}
        </tbody>
      </table>
    )}
  </div>
)

/**
 * VideoTaskMenu component displays a dropdown menu of actions for a video task.
 *
 * @param task - The video task.
 * @constructor
 */
const VideoTaskMenu = ({ task }: { task: VideoTask }) => {
  const status: TaskStatus = task.taskStatus  // 'PENDING' | 'STARTED' | 'RETRY' | 'FAILURE' | 'SUCCESS' | 'REVOKED' | 'IGNORED'
  switch (status) {
    case 'PENDING':
    case 'STARTED':
    case 'RETRY':
    case 'FAILURE':
      return <button>Annuler</button>
    case 'SUCCESS':
      return <button>Télécharger</button>
    case 'REVOKED':
    case 'IGNORED':
      return <button>Supprimer</button>
    default:
      throw new Error(`Unknown task status: ${status}`)
  }
}

export default VideoTaskList
