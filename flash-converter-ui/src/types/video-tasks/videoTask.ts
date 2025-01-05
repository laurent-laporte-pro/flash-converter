/**
 * Name of a video file
 */
export type VideoName = string;

/**
 * ID of a task
 */
export type TaskId = string;

/**
 * Status of a task
 */
export type TaskStatus = "PENDING" | "STARTED" | "RETRY" | "FAILURE" | "SUCCESS" | "REVOKED" | "IGNORED";

/**
 * Represents a task for converting a video.
 */
export interface VideoTask {
  /**
   * The name of the video file.
   */
  videoName: VideoName;

  /**
   * The unique identifier for the task.
   */
  taskId: TaskId;

  /**
   * The current status of the task (Celery task status).
   */
  taskStatus: TaskStatus;

  /**
   * Error message if the task failed.
   */
  errorMessage?: string;
}
