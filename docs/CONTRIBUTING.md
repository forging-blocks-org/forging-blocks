# Contributing to Building Blocks

We welcome contributions from the community! Whether you're fixing a bug, adding a feature, or improving documentation, your help is appreciated.

## Development Setup

To get started with development, follow these steps:

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** to your local machine:
    ```bash
    git clone https://github.com/YOUR-USERNAME/building-blocks.git
    cd building-blocks
    ```
3.  **Set up the development environment** using Poetry:
    ```bash
    poetry install
    ```
    This command installs all dependencies, including development tools.

4.  **Activate the pre-commit hooks**:
    ```bash
    poetry run pre-commit install
    ```
    This will set up the git hooks that automatically run our code quality checks before each commit. This ensures that all contributions adhere to the project's standards.

## Contribution Workflow

1.  **Create a new branch** for your changes:
    ```bash
    git checkout -b my-feature-branch
    ```
2.  **Make your changes**. Write code, add tests, and update documentation as needed.
3.  **Commit your changes**. When you run `git commit`, the pre-commit hooks will automatically run. If they fail, you'll need to fix the issues before you can commit.
4.  **Push your changes** to your fork:
    ```bash
    git push origin my-feature-branch
    ```
5.  **Create a pull request** to the `main` branch of the `building-blocks-org/building-blocks` repository.

## Code Style & Quality

We use the following tools to maintain code quality, which are all managed by the pre-commit hooks:

-   **`black`**: For consistent code formatting.
-   **`isort`**: For standardized import sorting.
-   **`mypy`**: For static type checking.
-   **`bandit`**: For identifying common security issues.

If you want to run all checks manually across the entire codebase, you can use this command:
```bash
poetry run pre-commit run --all-files
```

## Reporting Bugs

If you find a bug, please open an issue on our [GitHub issue tracker](https://github.com/gbrennon/building-blocks/issues). Include as much detail as possible, such as:

-   A clear description of the bug.
-   Steps to reproduce the bug.
-   The expected behavior.
-   The actual behavior.
-   Your Python version and the version of `building_blocks`.

Thank you for contributing!
