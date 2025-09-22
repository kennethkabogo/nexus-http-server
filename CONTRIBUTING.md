# Contributing to Gemini HTTP Server

First off, thank you for considering contributing to Gemini HTTP Server! It's people like you that make this open source project such a great tool for developers.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [your-email@example.com].

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for Gemini HTTP Server. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

*   **Use a clear and descriptive title** for the issue to identify the problem.
*   **Describe the exact steps which reproduce the problem** in as many details as possible.
*   **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples.
*   **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
*   **Explain which behavior you expected to see instead and why.**
*   **Include screenshots and animated GIFs** which show you following the described steps and clearly demonstrate the problem.
*   **If the problem is related to performance or memory**, include a CPU profile capture with your report.
*   **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Gemini HTTP Server, including completely new features and minor improvements to existing functionality.

*   **Use a clear and descriptive title** for the issue to identify the suggestion.
*   **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
*   **Provide specific examples to demonstrate the steps**.
*   **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
*   **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of Gemini HTTP Server which the suggestion is related to.
*   **Explain why this enhancement would be useful** to most Gemini HTTP Server users.
*   **List some other projects where this enhancement exists.**

### Pull Requests

The process described here has several goals:

*   Maintain Gemini HTTP Server's quality
*   Fix problems that are important to users
*   Engage the community in working toward the best possible Gemini HTTP Server
*   Enable a sustainable system for Gemini HTTP Server's maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1.  Follow all instructions in [the template](PULL_REQUEST_TEMPLATE.md)
2.  Follow the [styleguides](#styleguides)
3.  After you submit your pull request, verify that all [status checks](https://help.github.com/articles/about-status-checks/) are passing

While the prerequisites above must be satisfied prior to having your pull request reviewed, the reviewer(s) may ask you to complete additional design work, tests, or other changes before your pull request can be ultimately accepted.

## Styleguides

### Git Commit Messages

*   Use the present tense ("Add feature" not "Added feature")
*   Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
*   Limit the first line to 72 characters or less
*   Reference issues and pull requests liberally after the first line
*   When only changing documentation, include `[ci skip]` in the commit title

### Python Styleguide

All Python code must adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/).

*   Use 4 spaces for indentation, not tabs
*   Limit all lines to a maximum of 79 characters
*   Use descriptive variable and function names
*   Use docstrings for all public modules, functions, classes, and methods
*   Write comments that explain "why" not just "what"

### JavaScript Styleguide

All JavaScript code must adhere to [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript).

### CSS/HTML Styleguide

*   Use semantic HTML5 where possible
*   Use CSS classes prefixed with the component name
*   Follow BEM methodology for CSS class naming
*   Use CSS custom properties (variables) for consistent theming

### Documentation Styleguide

*   Use [Markdown](https://daringfireball.net/projects/markdown/) for documentation
*   Reference methods and classes in documentation using backticks
*   Use proper spelling and grammar
*   Keep documentation concise but comprehensive

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

*   `bug` - Issues that are bugs.
*   `enhancement` - Issues that are feature requests.
*   `documentation` - Issues or pull requests related to documentation.
*   `security` - Issues or pull requests related to security.
*   `beginner` - Good for newcomers.
*   `help wanted` - Extra attention is needed.
*   `question` - Further information is requested.
