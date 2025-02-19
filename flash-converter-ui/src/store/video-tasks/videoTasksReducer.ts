import { TaskId, TaskStatus, VideoTask } from "../../types/video-tasks/videoTask.ts";
import { saveTasksToStorage } from "./videoTasksStore.ts";

export interface VideoTasksState {
  tasks: VideoTask[];
}

export type VideoTasksAction =
  | { type: "LOAD_TASKS"; payload: VideoTask[] }
  | { type: "APPEND_TASK"; payload: VideoTask }
  | { type: "DELETE_TASK"; payload: TaskId }
  | { type: "UPDATE_TASK_STATUS"; payload: { taskId: TaskId; taskStatus: TaskStatus } }
  | { type: "UPDATE_TASK_ERROR"; payload: { taskId: TaskId; errorMessage: string } };

export const videoTasksReducer = (state: VideoTasksState, action: VideoTasksAction): VideoTasksState => {
  const actionType = action.type;
  switch (actionType) {
    case "LOAD_TASKS": {
      saveTasksToStorage(action.payload);
      return { tasks: action.payload };
    }

    case "APPEND_TASK": {
      const updatedTasks = [action.payload, ...state.tasks];
      saveTasksToStorage(updatedTasks);
      return { tasks: updatedTasks };
    }

    case "DELETE_TASK": {
      const updatedWithoutDeleted = state.tasks.filter((task) => task.taskId !== action.payload);
      saveTasksToStorage(updatedWithoutDeleted);
      return { tasks: updatedWithoutDeleted };
    }

    case "UPDATE_TASK_STATUS": {
      const updatedWithStatus = state.tasks.map((task) =>
        task.taskId === action.payload.taskId
          ? {
              ...task,
              taskStatus: action.payload.taskStatus,
              errorMessage: undefined,
            }
          : task,
      );
      saveTasksToStorage(updatedWithStatus);
      return { tasks: updatedWithStatus };
    }

    case "UPDATE_TASK_ERROR": {
      const updatedWithError = state.tasks.map((task) =>
        task.taskId === action.payload.taskId
          ? {
              ...task,
              errorMessage: action.payload.errorMessage,
            }
          : task,
      );
      saveTasksToStorage(updatedWithError);
      return { tasks: updatedWithError };
    }

    default:
      throw new Error(`Unhandled action type: ${actionType}`);
  }
};
