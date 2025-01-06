import React, { useCallback, useState } from "react";
import { Alert, Box, Button, LinearProgress, Paper, Typography } from "@mui/material";
import { CloudUpload, Movie } from "@mui/icons-material";
import { VideoTask } from "../../types/video-tasks/videoTask.ts";
import { videoProcessingService } from "../../api/video-tasks/service.ts";

/**
 * UploadForm component allows users to upload a video file for conversion.
 *
 * @param {Object} props - The component props.
 * @param {Function} props.appendTask - Function to append a new video task.
 */
function UploadForm({ appendTask }: { appendTask: (task: VideoTask) => void }) {
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState("");
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    if (event.type === "dragenter" || event.type === "dragover") {
      setDragActive(true);
    } else if (event.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    setDragActive(false);

    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith("video/")) {
      setVideoFile(file);
      setUploadError("");
    } else {
      setUploadError("Le fichier doit être une vidéo");
    }
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files ? event.target.files[0] : null;
    if (file) {
      setVideoFile(file);
      setUploadError("");
    }
  };

  const handleUpload = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!videoFile) return;

    setUploading(true);
    setUploadError("");

    try {
      const taskId = await videoProcessingService.createTask(videoFile);
      const videoTask: VideoTask = { taskId, videoName: videoFile.name, taskStatus: "PENDING" };
      appendTask(videoTask);
      const formElement = event.target as HTMLFormElement;
      formElement.reset();
      setVideoFile(null);
    } catch (error) {
      if (error instanceof Error) {
        setUploadError(error.message);
      } else {
        setUploadError(`An error occurred: ${error}`);
      }
    } finally {
      setUploading(false);
    }
  };

  const handleFileInputClick = () => {
    const inputElement = document.getElementById("video-upload-input");
    if (inputElement) {
      inputElement.click();
    }
  };

  return (
    <Box component="form" onSubmit={handleUpload} sx={{ width: "100%", maxWidth: 600, mx: "auto" }}>
      <input
        type="file"
        accept="video/*"
        onChange={handleFileChange}
        style={{ display: "none" }}
        id="video-upload-input"
      />

      <Paper
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        sx={{
          p: 3,
          mb: 2,
          border: "2px dashed",
          borderColor: dragActive ? "primary.main" : "grey.300",
          backgroundColor: dragActive ? "action.hover" : "background.paper",
          cursor: "pointer",
          transition: "all 0.2s ease",
          textAlign: "center",
        }}
        onClick={handleFileInputClick}
      >
        {videoFile ? (
          <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 2 }}>
            <Movie color="primary" />
            <Typography>{videoFile.name}</Typography>
          </Box>
        ) : (
          <Box>
            <CloudUpload sx={{ fontSize: 48, color: "primary.main", mb: 2 }} />
            <Typography>Glissez et déposez une vidéo ici ou cliquez pour sélectionner</Typography>
            <Typography variant="body2" color="textSecondary">
              Formats acceptés: MP4, AVI, MOV, etc.
            </Typography>
          </Box>
        )}
      </Paper>

      {videoFile && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="textSecondary">
            {frenchFileSize(videoFile.size, 2)}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Type: {videoFile.type}
          </Typography>
        </Box>
      )}

      {uploadError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {uploadError}
        </Alert>
      )}

      {uploading && (
        <Box sx={{ mb: 2 }}>
          <LinearProgress />
          <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
            Téléchargement en cours...
          </Typography>
        </Box>
      )}

      <Button
        type="submit"
        variant="contained"
        disabled={!videoFile || uploading}
        startIcon={<CloudUpload />}
        fullWidth
      >
        {uploading ? "Conversion en cours..." : "Convertir"}
      </Button>
    </Box>
  );
}

/**
 * Formats a file size in bytes to a human-readable string.
 *
 * @param size - The file size in bytes.
 * @param digits - The number of digits to display after the decimal point.
 */
function frenchFileSize(size: number, digits: number = 2): string {
  const order = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
  const converted = size / Math.pow(1024, order);
  const unit = ["o", "ko", "Mo", "Go", "To"][order];
  const formatter = new Intl.NumberFormat("fr-FR", { minimumFractionDigits: digits, maximumFractionDigits: digits });
  return `${formatter.format(converted)} ${unit}`;
}

export default UploadForm;
