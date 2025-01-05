---
title: Code Formatting
description: Code formatting guidelines for the Flash Converter UI project.
keywords: formatting, style, guidelines, prettier
---

# Code Formatting

This project uses [Prettier](https://prettier.io/) to format code.

## Installation

This paragraph describes how to install Prettier in the project and configure it with the desired settings.
This instructions can be found in the [Installation Page][prettier-installation] of the Prettier documentation.

```bash
# Change the current directory to the root of the project
cd "$(node find-package-dir.js)"
npm install --save-dev --save-exact prettier
node --eval "fs.writeFileSync('.prettierrc','{\n  \"printWidth\": 120\n}\n')"
node --eval "fs.writeFileSync('.prettierignore','# Ignore artifacts:\nbuild\ncoverage\n')"
git add .prettierrc .prettierignore
```

You can also add a script to your `package.json` file to format the code:

```json
{
  "scripts": {
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,scss,md}\""
  }
}
```

## Usage

You can format the code by running the following command:

```bash
npm run format
```
