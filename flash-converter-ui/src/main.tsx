// Import Roboto font for Material-UI
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

// Import React and ReactDOM
import React from "react";
import ReactDOM from "react-dom/client";

// Import the project's App component
import ThemeLayout from "./components/ThemeLayout.tsx";

// Rendering the App component
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ThemeLayout />
  </React.StrictMode>,
);
