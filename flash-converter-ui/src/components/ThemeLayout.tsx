import React, { useMemo, useState } from "react";
import {
  AppBar,
  Box,
  IconButton,
  Menu,
  MenuItem,
  PaletteMode,
  Toolbar,
  Typography,
  useMediaQuery,
} from "@mui/material";
import { BrightnessAuto as AutoIcon, DarkMode as DarkIcon, LightMode as LightIcon } from "@mui/icons-material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import App from "../App.tsx";
import flashConverterLogo from "/flash-converter-icon.png";

const ThemeLayout = () => {
  const prefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)");
  const [mode, setMode] = useState("auto");
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleThemeMenuClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleThemeMenuClose = () => {
    setAnchorEl(null);
  };

  const handleThemeChange = (newMode: string) => {
    setMode(newMode);
    handleThemeMenuClose();
  };

  const theme = useMemo(() => {
    const actualMode = mode === "auto" ? (prefersDarkMode ? "dark" : "light") : mode;

    return createTheme({
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
        mode: actualMode as PaletteMode,
      },
      typography: {
        h1: {
          fontSize: "3.2em",
          lineHeight: 1.1,
        },
      },
    });
  }, [mode, prefersDarkMode]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          flexGrow: 1,
          height: "100vh",
          display: "flex",
          flexDirection: "column",
          width: "100vw",
          position: "fixed",
          top: 0,
          left: 0,
        }}
      >
        <AppBar position="static">
          <Toolbar>
            <img
              src={flashConverterLogo}
              alt="Flash Converter Logo"
              style={{ marginRight: "16px", width: "36px", height: "36px" }}
            />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Flash Video Converter
            </Typography>
            <IconButton color="inherit" onClick={handleThemeMenuClick} size="large">
              {mode === "auto" ? <AutoIcon /> : mode === "light" ? <LightIcon /> : <DarkIcon />}
            </IconButton>
            <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleThemeMenuClose}>
              <MenuItem onClick={() => handleThemeChange("auto")}>
                <AutoIcon sx={{ mr: 1 }} /> Auto
              </MenuItem>
              <MenuItem onClick={() => handleThemeChange("light")}>
                <LightIcon sx={{ mr: 1 }} /> Light
              </MenuItem>
              <MenuItem onClick={() => handleThemeChange("dark")}>
                <DarkIcon sx={{ mr: 1 }} /> Dark
              </MenuItem>
            </Menu>
          </Toolbar>
        </AppBar>
        <Box component="main" sx={{ flexGrow: 1, p: 3, overflowY: "auto" }}>
          <App />
        </Box>{" "}
      </Box>
    </ThemeProvider>
  );
};

export default ThemeLayout;
