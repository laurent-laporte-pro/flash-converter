/**
 * Represents a task for converting a video.
 */
export interface VideoTask {
  /**
   * The name of the video file.
   */
  videoName: string;

  /**
   * The unique identifier for the task.
   */
  taskID: string;

  /**
   * The current status of the task (Celery task status).
   */
  taskStatus: 'PENDING' | 'STARTED' | 'RETRY' | 'FAILURE' | 'SUCCESS' | 'REVOKED' | 'IGNORED';
}
