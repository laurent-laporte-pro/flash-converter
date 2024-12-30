import { VideoTask } from './videoTask.ts'

export type TaskCommand = (task: VideoTask) => void;

export interface TaskCommands {
  download: TaskCommand;
  cancel: TaskCommand;
  delete: TaskCommand;
}
