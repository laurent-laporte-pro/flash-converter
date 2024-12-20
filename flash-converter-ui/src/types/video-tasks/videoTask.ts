/**
 * ID of a task
 */
export type TaskID = string;

/**
 * Status of a task
 */
export type TaskStatus = 'PENDING' | 'STARTED' | 'RETRY' | 'FAILURE' | 'SUCCESS' | 'REVOKED' | 'IGNORED';

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
  taskID: TaskID;

  /**
   * The current status of the task (Celery task status).
   */
  taskStatus: TaskStatus;
}

