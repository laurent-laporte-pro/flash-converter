// Import Roboto font for Material-UI
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

// Import React and ReactDOM
import React from "react";
import ReactDOM from "react-dom/client";

// Import the Material-UI components
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

// Import the project's App component
import App from "./App";

// Create a theme instance
const theme = createTheme({
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          display: "flex",
          minWidth: "320px",
          minHeight: "100vh",
        },
        a: {
          textDecoration: "none",
          "&:hover": {
            color: "#535bf2",
          },
        },
        table: {
          width: "100%",
          borderCollapse: "collapse",
        },
        "th, td": {
          padding: "0.5em",
          textAlign: "left",
          borderBottom: "1px solid rgba(224, 224, 224, 1)",
        },
      },
    },
  },
  palette: {
    // Gérer le mode sombre/clair
    mode: "light", // ou 'dark'
  },
  typography: {
    h1: {
      fontSize: "3.2em",
      lineHeight: 1.1,
    },
  },
});

// 6. Rendu de l'application
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
    </ThemeProvider>
  </React.StrictMode>,
);
