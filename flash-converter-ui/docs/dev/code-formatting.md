---
title: Code Formatting
description: Code formatting guidelines for the Flash Converter UI project.
keywords: formatting, style, guidelines, prettier
---

## Introduction

This project uses [Prettier](https://prettier.io/) to format code.

## Installation

### Installation of Prettier

This paragraph describes how to install Prettier in the project and configure it with the desired settings.
This instructions can be found in the [Installation Page][prettier-installation] of the Prettier documentation.

```shell
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

### Installation of ESLint configuration for Prettier

This paragraph describes how to install the ESLint configuration for Prettier in the project.
This instructions can be found in the [ESLint Plugin Page][eslint-plugin] in GitHub.

```shell
npm install --save-dev eslint-config-prettier
```

Add eslint-config-prettier to your ESLint configuration to `eslint.config.js` (flat config).

```javascript
import eslintConfigPrettier from "eslint-config-prettier";

export default tseslint.config(
  { ignores: ["dist"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended, eslintConfigPrettier],
    /* ... */
);
```

## Usage

You can format the code by running the following command:

```shell
npm run format
```

You can also check the code for errors and style issues by running the following command:

```shell
npm run lint
```

[prettier-installation]: https://prettier.io/docs/en/install.html

[eslint-plugin]: https://github.com/prettier/eslint-config-prettier#installation
