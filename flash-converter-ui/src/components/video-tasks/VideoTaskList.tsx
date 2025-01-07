import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Typography,
  ButtonGroup,
  Box,
} from "@mui/material";
import { Download as DownloadIcon, Delete as DeleteIcon, Cancel as CancelIcon } from "@mui/icons-material";
import { TaskStatus, VideoTask } from "../../types/video-tasks/videoTask.ts";
import { TaskCommands } from "../../types/video-tasks/taskCommands.ts";

const VideoTaskMenu = ({ task, commands }: { task: VideoTask; commands: TaskCommands }) => {
  const status: TaskStatus = task.taskStatus;

  const buttonProps = {
    sx: { mx: 0.5 },
  };

  switch (status) {
    case "PENDING":
      return (
        <ButtonGroup size="small">
          <Button
            variant="outlined"
            color="warning"
            startIcon={<CancelIcon />}
            onClick={() => commands.cancel(task)}
            {...buttonProps}
          >
            Annuler
          </Button>
          <Button
            variant="outlined"
            color="error"
            startIcon={<DeleteIcon />}
            onClick={() => commands.delete(task)}
            {...buttonProps}
          >
            Supprimer
          </Button>
        </ButtonGroup>
      );
    case "STARTED":
    case "RETRY":
    case "FAILURE":
      return (
        <Button
          variant="outlined"
          color="warning"
          startIcon={<CancelIcon />}
          onClick={() => commands.cancel(task)}
          {...buttonProps}
        >
          Annuler
        </Button>
      );
    case "SUCCESS":
      return (
        <ButtonGroup size="small">
          <Button
            variant="outlined"
            color="primary"
            startIcon={<DownloadIcon />}
            onClick={() => commands.download(task)}
            {...buttonProps}
          >
            Télécharger
          </Button>
          <Button
            variant="outlined"
            color="error"
            startIcon={<DeleteIcon />}
            onClick={() => commands.delete(task)}
            {...buttonProps}
          >
            Supprimer
          </Button>
        </ButtonGroup>
      );
    case "REVOKED":
    case "IGNORED":
      return (
        <Button
          variant="outlined"
          color="error"
          startIcon={<DeleteIcon />}
          onClick={() => commands.delete(task)}
          {...buttonProps}
        >
          Supprimer
        </Button>
      );
    default:
      throw new Error(`Unknown task status: ${status}`);
  }
};

const getStatusColor = (status: TaskStatus) => {
  switch (status) {
    case "SUCCESS":
      return "success.main";
    case "FAILURE":
      return "error.main";
    case "STARTED":
    case "RETRY":
      return "info.main";
    case "PENDING":
      return "warning.main";
    case "REVOKED":
    case "IGNORED":
      return "text.disabled";
    default:
      return "text.primary";
  }
};

const getStatusMessage = (status: TaskStatus) => {
  switch (status) {
    case "SUCCESS":
      return "Terminé";
    case "FAILURE":
      return "Erreur";
    case "STARTED":
      return "En cours";
    case "RETRY":
      return "Nouvel essai";
    case "PENDING":
      return "En attente";
    case "REVOKED":
      return "Annulé";
    case "IGNORED":
      return "Ignoré";
    default:
      return "Inconnu";
  }
};

export const VideoTaskList = ({ tasks, commands }: { tasks: VideoTask[]; commands: TaskCommands }) => (
  <Box sx={{ width: "100%" }}>
    <Typography variant="h6" color="textPrimary" sx={{ mb: 2 }}>
      Tâches de conversion
    </Typography>

    {tasks.length === 0 ? (
      <Typography color="text.secondary">Aucune tâche de conversion.</Typography>
    ) : (
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="video tasks table">
          <TableHead>
            <TableRow>
              <TableCell>Video</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Message</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {tasks.map((task: VideoTask) => (
              <TableRow key={task.taskId} sx={{ "&:last-child td, &:last-child th": { border: 0 } }}>
                <TableCell component="th" scope="row">
                  {task.videoName}
                </TableCell>
                <TableCell>
                  <Typography color={getStatusColor(task.taskStatus)}>{getStatusMessage(task.taskStatus)}</Typography>
                </TableCell>
                <TableCell>
                  {task.errorMessage ? <Typography color="error">{task.errorMessage}</Typography> : "–"}
                </TableCell>
                <TableCell align="right">
                  <VideoTaskMenu task={task} commands={commands} />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    )}
  </Box>
);

export default VideoTaskList;
