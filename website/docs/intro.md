---
sidebar_position: 1
---

# Tutorial Intro

Let's discover how to use **Docusaurus in less than 5 minutes**.

## Getting Started

You can get started by **creating a new site** on your local machine.

Or, you can **try Docusaurus immediately** in your browser with **[docusaurus.new](https://docusaurus.new)**.

### What You'll Need

- [Node.js](https://nodejs.org/en/download/) version 20.0 or above.
  - When installing Node.js, we recommend checking all checkboxes related to dependencies to ensure all necessary tools are installed.

## Generate a New Site

You can generate a new Docusaurus site by using the **classic template**.

The classic template will automatically be added to your project when you run the following command:

```bash
npm init docusaurus@latest my-website classic
```

You can type this command into Command Prompt, PowerShell, Terminal, or any other integrated terminal in your code editor.

This command also installs all the necessary dependencies you need to run Docusaurus.

## Start Your Site

To start your site, run the development server:

```bash
cd my-website
npm run start
```

The `cd` command changes the directory you're working in. To work with your newly created Docusaurus site, you'll need to navigate into that directory in your terminal.

The `npm run start` command builds your website locally and serves it through a development server. You can view it at http://localhost:3000/.

Open the `docs/intro.md` file (which is this page) and edit a few lines. The site will **reload automatically** and display your changes instantly.
