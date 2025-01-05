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

To install Roboto through the Google Web Fonts CDN, add the following code inside your project's `<head />` tag:

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link
  rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
/>
```

[react]: https://www.npmjs.com/package/react

[react-dom]: https://www.npmjs.com/package/react-dom
