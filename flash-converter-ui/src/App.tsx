import "./App.css";
import VideoTaskList from "./components/video-tasks/VideoTaskList.tsx";
import { useVideoTasks } from "./store/video-tasks/useVideoTasks.ts";
import { VideoTask } from "./types/video-tasks/videoTask.ts";
import { videoProcessingService } from "./api/video-tasks/service.ts";
import { useEffect } from "react";
import UploadForm from "./components/video-tasks/UploadForm.tsx";
import { TaskCommands } from "./types/video-tasks/taskCommands.ts";
import { Paper, Typography } from "@mui/material";

function App() {
  const { state, actions } = useVideoTasks();
  const tasks = state.tasks;

  const updateTaskStatus = async (videoTask: VideoTask) => {
    if (videoTask.taskStatus === "PENDING" || videoTask.taskStatus === "STARTED" || videoTask.taskStatus === "RETRY") {
      try {
        const status = await videoProcessingService.getTaskStatus(videoTask.taskId);
        actions.updateTaskStatus(videoTask.taskId, status);
      } catch (error) {
        if (error instanceof Error) {
          actions.updateTaskError(videoTask.taskId, error.message);
        } else {
          actions.updateTaskError(videoTask.taskId, `An error occurred: ${error}`);
        }
      }
    }
  };

  useEffect(() => {
    const interval = setInterval(async () => state.tasks.forEach(updateTaskStatus), 5000);
    return () => clearInterval(interval);
  });

  const downloadTaskCommand = (task: VideoTask) => {
    try {
      videoProcessingService.getTaskResult(task.taskId).then();
    } catch (error) {
      if (error instanceof Error) {
        actions.updateTaskError(task.taskId, error.message);
      } else {
        actions.updateTaskError(task.taskId, `An error occurred: ${error}`);
      }
    }
  };

  const cancelTaskCommand = (task: VideoTask) => {
    try {
      videoProcessingService.revokeTask(task.taskId).then(() => actions.updateTaskStatus(task.taskId, "REVOKED"));
    } catch (error) {
      if (error instanceof Error) {
        actions.updateTaskError(task.taskId, error.message);
      } else {
        actions.updateTaskError(task.taskId, `An error occurred: ${error}`);
      }
    }
  };

  const deleteTaskCommand = (task: VideoTask) => {
    try {
      videoProcessingService.revokeTask(task.taskId).then(() => actions.updateTaskStatus(task.taskId, "REVOKED"));
      actions.deleteTask(task.taskId);
    } catch (error) {
      if (error instanceof Error) {
        actions.updateTaskError(task.taskId, error.message);
      } else {
        actions.updateTaskError(task.taskId, `An error occurred: ${error}`);
      }
    }
  };

  const taskCommands: TaskCommands = {
    download: downloadTaskCommand,
    cancel: cancelTaskCommand,
    delete: deleteTaskCommand,
  };

  return (
    <>
      <Typography variant="h6" color="textPrimary" gutterBottom>
        Ajoutez des sous-titres à vos vidéos en un clin d’œil
      </Typography>
      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <UploadForm appendTask={actions.appendTask} />
      </Paper>
      <Paper elevation={3} sx={{ p: 2, mb: 2 }}>
        <VideoTaskList tasks={tasks} commands={taskCommands} />
      </Paper>
    </>
  );
}

export default App;
