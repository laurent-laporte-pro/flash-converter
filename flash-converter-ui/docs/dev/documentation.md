---
title: Documentation
description: Documentation for the Flash Converter UI project.
keywords: mkdocs, documentation, guidelines
---

## Introduction

This project uses [MkDocs](https://www.mkdocs.org/) to generate documentation.

## Installation

This paragraph describes how to install MkDocs in the project and configure it with the desired settings.
This instructions can be found in the [Installation Page][mkdocs-installation] of the MkDocs documentation.

```shell
pip install mkdocs
```

## Usage

This paragraph describes how to use MkDocs to generate the documentation.
This instructions can be found in the [CLI Page][mkdocs-cli] of the MkDocs documentation.

To serve the documentation locally, run the following command:

```shell
mkdocs serve -a localhost:8001
```

**Note:** The documentation will be available at `http://localhost:8001` to avoid conflicts with the Flash Converter
API running on `http://localhost:8000` by default.

[mkdocs-installation]: https://www.mkdocs.org/user-guide/installation/
[mkdocs-cli]: https://www.mkdocs.org/user-guide/cli/#mkdocs-serve
