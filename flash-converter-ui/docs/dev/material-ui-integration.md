---
title: Material-UI Integration
description: Material-UI integration guidelines for the Flash Converter UI project.
keywords: material-ui, MUI, guidelines, components
---

## Introduction

This project uses [Material-UI](https://mui.com/material-ui/) to create the user interface.
Material UI is a component library that implements Google's Material Design.

## Installation

Run the following commands to add Material UI, Emotion, and Roboto to the project:

```shell
npm install @mui/material @emotion/react @emotion/styled
npm install @fontsource/roboto
npm install @mui/icons-material
```

Please note that [react][react] and [react-dom][react-dom] are peer dependencies, meaning you should ensure they
are installed before installing Material UI.

Update the `peerDependencies` section of the `package.json` file to include the following:

```json
{
  "peerDependencies": {
    "react": "^17.0.0 || ^18.0.0 || ^19.0.0",
    "react-dom": "^17.0.0 || ^18.0.0 || ^19.0.0"
  }
}
```

## Source code integration

### Using Roboto font

To install Roboto through the Google Web Fonts CDN, add the following code inside your project's `<head />` tag:

The following lines of code are added to the `index.html` file:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" />
```

### Using Material-UI in the main component

The following lines of code are added in the `main.tsx` file:

```tsx
// Import Roboto font for Material-UI
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

// Import React and ReactDOM
import React from "react";
import ReactDOM from "react-dom/client";

// Rendering the App component
ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>{/* Add the App component here */}</React.StrictMode>,
);
```

### Using Material-UI in the application

You can use Material-UI components in your application by importing them from the `@mui/material` package:

```tsx
import { Paper, Typography, Button } from "@mui/material";
```

Read the [Material-UI documentation][material-ui-components] for more information.

[react]: https://www.npmjs.com/package/react
[react-dom]: https://www.npmjs.com/package/react-dom
[material-ui-components]: https://mui.com/material-ui/all-components/
