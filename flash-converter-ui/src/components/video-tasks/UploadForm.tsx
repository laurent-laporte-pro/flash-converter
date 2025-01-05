import React, { useState } from "react";
import { videoProcessingService } from "../../api/video-tasks/service.ts";
import { VideoTask } from "../../types/video-tasks/videoTask.ts";

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

  /**
   * Handles the change event for the video file input.
   *
   * @param {React.ChangeEvent<HTMLInputElement>} event - The change event.
   */
  const handleVideoFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setVideoFile(event.target.files[0]);
    } else {
      setVideoFile(null);
    }
  };

  /**
   * Handles the form submission for uploading the video file.
   *
   * @param {React.FormEvent<HTMLFormElement>} event - The form submission event.
   */
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

  return (
    <form onSubmit={handleUpload}>
      <input type={"file"} placeholder={"Téléchargez une vidéo"} accept="video/*" onChange={handleVideoFileChange} />
      <button type="submit" disabled={uploading}>
        Convertir
      </button>
      <FileInfo file={videoFile} />
      <UploadError error={uploadError} />
      <ProgressBar uploading={uploading} />
    </form>
  );
}

/**
 * Formats a file size in bytes to a human-readable string.
 *
 * @param size - The file size in bytes.
 * @param digits - The number of digits to display after the decimal point.
 */
function humanFileSize(size: number, digits: number = 2): string {
  const order = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
  const converted = size / Math.pow(1024, order);
  const unit = ["o", "ko", "Mo", "Go", "To"][order];
  const formatter = new Intl.NumberFormat("fr-FR", { minimumFractionDigits: digits, maximumFractionDigits: digits });
  return `${formatter.format(converted)} ${unit}`;
}

/**
 * FileInfo component displays information about a file (e.g., type and size).
 *
 * @param file - The file to display information for.
 */
function FileInfo({ file }: { file: File | null }) {
  if (!file) return null;
  return (
    <p>
      <span>
        🎥 fichier <strong>{file.type}</strong> sélectionné
      </span>{" "}
      <span>({humanFileSize(file.size)})</span>
    </p>
  );
}

/**
 * UploadError component displays an error message if an error occurred during the upload.
 * @param error - The error message to display.
 */

function UploadError({ error }: { error: string }) {
  if (!error) return null;
  return <p style={{ color: "red" }}>{error}</p>;
}

/**
 * ProgressBar component displays a progress bar when uploading a file.
 * @param uploading - Whether a file is currently being uploaded.
 */
function ProgressBar({ uploading }: { uploading: boolean }) {
  if (!uploading) return null;
  return <p>Téléversement en cours…</p>;
}

export default UploadForm;
