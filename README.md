# quick-deck-mcp
an MCP Server for generating decks / slides.

# Installation
You need python 3.13.
You can use the [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage the virtual environment and dependencies.
And you may need [rust](https://www.rust-lang.org/tools/install) to build some dependencies.
```bash
uv venv --python=3.13 --seed
. .venv/bin/activate
uv sync
```


# Execute via Docker
```bash
docker run -it --rm -v $(pwd):/app -w /app
```

# Running
You can install this server in Claude Desktop and interact with it right away by running:
```bash
uv run mcp install __main__.py
```
Alternatively, you can test it with the MCP Inspector:

```bash
uv run mcp dev __main__.py
```

Or you can run it as real http server:

```bash
uv run --with mcp mcp run __main__.py -t sse
```



# Example Usage for agenda generation
Make sure the server is running in sse mode:

```bash

curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "generate_agenda",
      "arguments":  {
          "topic": "Git Introduction",
          "audience": "Young IT Professionals",
          "style": "Fun educational content",
          "language": "English"
        }
      }
    }'
```
Example output:
```json
{
  "result": [
    "# Agenda for Git Introduction Presentation\n\n",
    "\n\n## Understanding Git Basics: \n- Introduction to version control systems.\n- What Git is: Definition and key features.\n- The advantages of using Git for project collaboration.\n\n",
    "\n\n## Git History and Evolution:\n- The origin of Git and its creator, Linus Torvalds.\n- Milestones in Git's development.\n- How Git has become a standard in software development.\n\n",
    "\n\n## Core Git Concepts:\n- Repository: What it is and how it works.\n- Commits, branches, and merges: Basic terminology explained.\n- Local vs. remote repositories and their significance.\n\n",
    "\n\n## Setting Up Git:\n- Overview of the installation process for different operating systems.\n- Configuring Git for first-time users.\n- Creating your first repository: A step-by-step guide.\n\n",
    "\n\n## Basic Git Commands:\n- Introduction to essential Git commands: `git init`, `git clone`, `git add`, and `git commit`.\n- Understanding the Git workflow.\n- Practical examples of using commands in a project setting.\n\n",
    "\n\n## Collaboration with Git:\n- Working with branches: How to create and manage them.\n- Pull requests: What they are and how to use them.\n- Resolving merge conflicts: Tips and techniques.\n\n",
    "\n\n## Best Practices and Tips:\n- Writing meaningful commit messages.\n- Regularly pushing changes: Why it’s important.\n- Staying organized with branches and workflows.\n\n",
    "\n\n## Resources for Further Learning:\n- Recommended books, websites, and tutorials for mastering Git.\n- Communities and forums for support and networking.\n- Opportunities for practical, real-world experience with Git. \n\n",
    " \n\n## Q&A Session:\n- Open floor for questions and clarifications.\n- Discuss common challenges and solutions encountered when using Git."
  ]
}
```

# Example Usage for deck generation
Make sure the server is running in sse mode:
```bash
curl -X POST http://localhost:8000/tools/call \
    -H "Content-Type: application/json" \
    -d '{
      "jsonrpc": "2.0",
      "id": "1",
      "method": "tools/call",
      "params": {
        "name": "generate_deck",
        "arguments":  {
            "topic": "Git Introduction",
            "audience": "Young IT Professionals",
            "style": "Fun educational content",
            "language": "English",
            "agenda": [
    "# Agenda for Git Introduction Presentation\n\n",
    "\n\n## Understanding Git Basics: \n- Introduction to version control systems.\n- What Git is: Definition and key features.\n- The advantages of using Git for project collaboration.\n\n",
    "\n\n## Git History and Evolution:\n- The origin of Git and its creator, Linus Torvalds.\n- Milestones in Git's development.\n- How Git has become a standard in software development.\n\n",
    "\n\n## Core Git Concepts:\n- Repository: What it is and how it works.\n- Commits, branches, and merges: Basic terminology explained.\n- Local vs. remote repositories and their significance.\n\n",
    "\n\n## Setting Up Git:\n- Overview of the installation process for different operating systems.\n- Configuring Git for first-time users.\n- Creating your first repository: A step-by-step guide.\n\n",
    "\n\n## Basic Git Commands:\n- Introduction to essential Git commands: `git init`, `git clone`, `git add`, and `git commit`.\n- Understanding the Git workflow.\n- Practical examples of using commands in a project setting.\n\n",
    "\n\n## Collaboration with Git:\n- Working with branches: How to create and manage them.\n- Pull requests: What they are and how to use them.\n- Resolving merge conflicts: Tips and techniques.\n\n",
    "\n\n## Best Practices and Tips:\n- Writing meaningful commit messages.\n- Regularly pushing changes: Why it’s important.\n- Staying organized with branches and workflows.\n\n",
    "\n\n## Resources for Further Learning:\n- Recommended books, websites, and tutorials for mastering Git.\n- Communities and forums for support and networking.\n- Opportunities for practical, real-world experience with Git. \n\n",
    " \n\n## Q&A Session:\n- Open floor for questions and clarifications.\n- Discuss common challenges and solutions encountered when using Git."
  ]
          }
        }
      }'

# Example output of the content generation
```json
{
  "result": [
    {
      "title": "# Agenda for Git Introduction Presentation\n\n",
      "content": "## Agenda for Git Introduction Presentation\n- Overview of Version Control Systems\n- Introduction to Git\n- Key Features of Git\n- Installing Git\n- Basic Git Commands\n- Branching and Merging in Git\n- Working with Remote Repositories\n- Best Practices for Using Git\n- Q&A Session  \n::: notes\nThis presentation will provide a comprehensive introduction to Git, starting with an overarching view of version control systems and moving into the specifics of Git itself. We'll explore its key features, how to install it, and the basic commands you need to get started. Additionally, we'll delve into important concepts such as branching and merging, how to work with remote repositories, and best practices for using Git effectively in your projects. The session will conclude with a Q&A to address any remaining questions.\n:::"
    },
    {
      "title": "\n\n## Understanding Git Basics: \n- Introduction to version control systems.\n- What Git is: Definition and key features.\n- The advantages of using Git for project collaboration.\n\n",
      "content": "## Understanding Git Basics\n- Version control systems track changes in files and coordinate work among multiple people.\n- Git is a popular distributed VCS, known for its speed, flexibility, and support for nonlinear development.\n- Advantages of Git include better collaboration, enhanced backup and recovery options, and the ability to branch and merge easily.\n\n::: notes\nVersion control systems (VCS) are essential tools for managing changes to documents, code, and other files, especially in collaborative environments. Git, a distributed version control system, is favored for its efficiency and powerful branching features, which allow multiple developers to work on their own segments of a project simultaneously without interfering with one another. The advantages of using Git include improved teamwork with features like pull requests and code reviews, automatic backups through remote repositories, and the capability to create distinct branches for new features or experiments, which can be merged back into the main project when ready. Understanding these basics will set the foundation for working effectively with Git in your projects.\n:::"
    },
    {
      "title": "\n\n## Git History and Evolution:\n- The origin of Git and its creator, Linus Torvalds.\n- Milestones in Git's development.\n- How Git has become a standard in software development.\n\n",
      "content": "## Git History and Evolution\n- Git was created by Linus Torvalds in 2005 for the Linux kernel development.\n- Key milestones include the release of version 1.0 in 2005, introduction of support for branching and merging, and the integration of Git with platforms like GitHub.\n- Git has become the standard version control system due to its powerful features and flexibility, now widely adopted in both open-source and enterprise environments.\n\n::: notes\nGit was developed by Linus Torvalds in 2005 to assist with the management of the Linux kernel source code. Since its inception, it has undergone significant milestones, including the release of its first stable version, 1.0, and the enhancement of branching and merging capabilities which greatly improved its usability. The integration of Git with popular platforms such as GitHub has also played a crucial role in its adoption. Today, Git stands as the standard version control system in software development, favored for its powerful features, strong community support, and ability to facilitate collaboration among developers.\n:::"
    },
    {
      "title": "\n\n## Core Git Concepts:\n- Repository: What it is and how it works.\n- Commits, branches, and merges: Basic terminology explained.\n- Local vs. remote repositories and their significance.\n\n",
      "content": "## Core Git Concepts\n- Repository: A storage space for your project files and version history.\n::: notes\nA repository in Git is a location where all your project files are stored, including their entire version history. It can be located on your local machine or hosted remotely, allowing you to manage changes and collaborate with others more effectively.\n:::"
    },
    {
      "title": "\n\n## Core Git Concepts:\n- Repository: What it is and how it works.\n- Commits, branches, and merges: Basic terminology explained.\n- Local vs. remote repositories and their significance.\n\n",
      "content": "## Commits, Branches, and Merges\n- Commits: Snapshots of your project at specific points in time.\n- Branches: Independent lines of development.\n- Merges: Combining changes from different branches.\n::: notes\nCommits are like snapshots that capture the state of your project at a given moment. Branches allow multiple lines of development to happen simultaneously, enabling features or fixes to be developed in isolation. Merging is the process of combining those branches back together, ensuring all changes are incorporated in the main project.\n:::"
    },
    {
      "title": "\n\n## Core Git Concepts:\n- Repository: What it is and how it works.\n- Commits, branches, and merges: Basic terminology explained.\n- Local vs. remote repositories and their significance.\n\n",
      "content": "## Local vs. Remote Repositories\n- Local repositories: Your workspace on your computer.\n- Remote repositories: Hosted on a server for collaboration.\n- Significance: Understanding where and how to save your work.\n::: notes\nLocal repositories are the copies of your project on your own machine, where you can make changes without affecting others. Remote repositories are hosted on platforms like GitHub or GitLab, allowing for collaboration and access by multiple users. Understanding the distinction helps in managing your workflow and sharing your code effectively.\n:::"
    },
    {
      "title": "\n\n## Setting Up Git:\n- Overview of the installation process for different operating systems.\n- Configuring Git for first-time users.\n- Creating your first repository: A step-by-step guide.\n\n",
      "content": "## Setting Up Git \n- Installation Process\n  - Steps for Windows, macOS, and Linux.\n  - Downloading from the official website.\n\n- Configuring Git\n  - Setting up your username and email.\n  - Important commands to run for first-time configuration.\n\n- Creating Your First Repository\n  - Step-by-step guide to initialize a repository.\n  - Basic Git commands to add and commit files.\n\n::: notes\nIn this section, we will walk through the process of setting up Git on your system. We'll begin by discussing how to install Git on various operating systems, highlighting any differences between Windows, macOS, and Linux. \n\nNext, we'll go over the critical configurations needed for first-time users. This includes setting up your global username and email address, which are essential for recording your contributions accurately. You'll also learn some fundamental commands to get you started.\n\nFinally, we will create your first Git repository together, covering the steps necessary to initialize it, add files, and make your first commit. By the end of this section, you will have a functioning repository ready for your projects.\n:::"
    },
    {
      "title": "\n\n## Basic Git Commands:\n- Introduction to essential Git commands: `git init`, `git clone`, `git add`, and `git commit`.\n- Understanding the Git workflow.\n- Practical examples of using commands in a project setting.\n\n",
      "content": "## Basic Git Commands\n- Introduction to essential Git commands: `git init`, `git clone`, `git add`, and `git commit`.\n- Understanding the Git workflow.\n- Practical examples of using commands in a project setting.\n::: notes\nIn this section, we will cover the essential Git commands that are crucial for managing your projects. We'll start with `git init`, which initializes a new Git repository, and `git clone`, which allows you to copy an existing repository to your local machine. Following that, we'll discuss `git add`, which is used to stage changes for the next commit, and `git commit`, which records the changes in the repository history.\n\nWe will also dive into the Git workflow, which is a series of steps that developers follow when working with Git. This includes making changes to files, staging those changes, and committing them to track your project’s history.\n\nLastly, we will provide practical examples of using these commands in a project setting, illustrating how to utilize them effectively in real-world scenarios. \n:::"
    },
    {
      "title": "\n\n## Collaboration with Git:\n- Working with branches: How to create and manage them.\n- Pull requests: What they are and how to use them.\n- Resolving merge conflicts: Tips and techniques.\n\n",
      "content": "## Collaboration with Git\n- Working with branches: Create and manage branches to keep features separate.\n- Pull requests: Essential for code review and collaboration, submit changes for others to review.\n- Resolving merge conflicts: Strategies for identifying and resolving conflicting changes.\n\n::: notes\nCollaboration in Git is key to successful teamwork. First, working with branches allows developers to isolate their work, making it easier to manage different features or fixes simultaneously without interfering with the main codebase. Branches can be created and managed simply with Git commands.\n\nNext, pull requests are a crucial part of collaboration in Git. They enable developers to request the integration of changes from a feature branch back into the main branch. Pull requests facilitate code reviews, discussions, and can include automated tests to ensure quality.\n\nLastly, resolving merge conflicts is an inevitable part of collaboration. Understanding how to identify these conflicts and effectively resolve them is essential for a smooth workflow. Techniques include using diff tools, reviewing changes carefully, and communicating with team members to agree on solutions.\n:::"
    },
    {
      "title": "\n\n## Best Practices and Tips:\n- Writing meaningful commit messages.\n- Regularly pushing changes: Why it’s important.\n- Staying organized with branches and workflows.\n\n",
      "content": "## Best Practices and Tips\n- Writing meaningful commit messages.\n- Regularly pushing changes: Why it’s important.\n- Staying organized with branches and workflows.\n::: notes\nWhen working with git, following best practices can significantly improve your workflow and collaboration with others. \n\n1. **Writing meaningful commit messages**: Always write clear and descriptive messages for your commits to provide context about what changes were made and why. This makes it easier for others (and yourself in the future) to understand the history of changes in the project.\n\n2. **Regularly pushing changes**: Make it a habit to push your changes frequently. This helps to keep your local work backed up, makes it easier to collaborate with others, and ensures that your teammates are aware of your progress. It also reduces the chances of running into conflicts later on.\n\n3. **Staying organized with branches and workflows**: Use branches to manage different features, fixes, or experiments. Keep your main branch (usually 'main' or 'master') stable and deployable. Having a structured workflow (like Git Flow) can help streamline collaboration and improve efficiency within your team.\n:::"
    },
    {
      "title": "\n\n## Resources for Further Learning:\n- Recommended books, websites, and tutorials for mastering Git.\n- Communities and forums for support and networking.\n- Opportunities for practical, real-world experience with Git. \n\n",
      "content": "## Resources for Further Learning\n- **Books**: Consider reading \"Pro Git\" by Scott Chacon and Ben Straub for in-depth understanding, or \"Git Pocket Guide\" by Richard E. Silverman for quick reference.\n- **Websites**: Explore the official Git documentation at git-scm.com, and platforms like Atlassian's Git tutorials for comprehensive guides.\n- **Tutorials**: Websites like Codecademy and freeCodeCamp offer interactive tutorials to practice Git commands in a hands-on manner.\n- **Communities**: Join forums such as Stack Overflow or the Git subreddit for community support, discussions, and solutions to Git-related issues.\n- **Networking**: Participate in local meetups or online communities focused on software development to connect with other developers and share knowledge about Git.\n- **Practical Experience**: Contribute to open-source projects on GitHub to gain real-world experience and apply your Git skills in collaborative settings.\n\n::: notes\nThere are several resources available for mastering Git. Recommended books include \"Pro Git,\" which provides a thorough understanding of all Git functionalities, and \"Git Pocket Guide,\" useful for quick references. Websites like git-scm.com offer official documentation while platforms such as Atlassian provide excellent tutorials, making it easier for beginners to learn. Interactive learning can be pursued through courses on websites like Codecademy and freeCodeCamp.\n\nFor community support, engaging in forums like Stack Overflow or joining the Git subreddit can be beneficial for troubleshooting and networking with fellow developers. Additionally, attending local meetups or participating in online communities fosters connections and knowledge sharing.\n\nLastly, to gain practical experience, contributing to open-source projects on platforms like GitHub allows you to apply your skills in real-world scenarios and collaborate with others, which can significantly enhance your understanding of Git.\n:::"
    },
    {
      "title": " \n\n## Q&A Session:\n- Open floor for questions and clarifications.\n- Discuss common challenges and solutions encountered when using Git.",
      "content": "## Q&A Session\n- Open floor for questions and clarifications.\n- Discuss common challenges and solutions encountered when using Git.\n::: notes\nThis session is designed to address any questions you might have about Git. Feel free to ask about any specific challenges you've encountered during your projects. We will discuss common issues such as merge conflicts, branching strategies, and best practices for committing changes. Sharing solutions and experiences can greatly enhance our understanding and usage of Git. Don't hesitate to speak up!\n:::"
    }
  ]
}
```