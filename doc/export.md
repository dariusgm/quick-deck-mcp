
# Generate PDF from Markdown using Export Tool
# This example shows how to generate a PDF from a Markdown file using the export tool.
# Make sure the server is running:
```bash
uvicorn main:app --port 8000 --host 127.0.0.1 --workers 4
```

Now we can trigger the export tool using the previously generated Markdown file `git.md`.
Here is a example of the Markdown file:

```markdown
## Agenda for Git Introduction Presentation
- Understanding the Basics of Version Control 
- Why Git? Benefits and Features
- Setting Up Git: Installation and Configuration 
- Key Git Commands: The Building Blocks 
- Branching and Merging: Navigating Project Changes 
- Collaboration Made Easy: Working with Remote Repositories 
- Best Practices for Using Git Effectively 
- Q&A Session: Your Git Queries Answered!

::: notes
Welcome to the Git Introduction Presentation! Today, we'll dive into the exciting world of version control with Git. Our agenda will cover the essentials, starting with the basics of version control and transitioning to why Git stands out among the other systems. We will guide you through the setup process, introduce key commands that every Git user should know, and discuss branching and merging to keep your projects organized.

Collaboration is a crucial aspect of modern development, and Git makes it a breeze. We’ll explore how to work with remote repositories effectively and cover best practices to ensure you make the most of Git in your projects. Finally, we’ll wrap up with a Q&A session where you can ask any questions you may have. Get ready to embark on this exciting journey into version control!
## What is Version Control?
- A system that records changes to files over time.
- Enables collaboration and backup of work.
::: notes
Version control is a system that records changes to files over time, allowing users to revisit previous versions. It is vital for collaborative work as it manages changes made by multiple individuals, reducing risks of conflicts. Think of it as a superhero for your files, always standing by to save the day when things go wrong!
:::
---

## Why Use Version Control?
- Keeps track of every modification.
- Helps you collaborate without chaos.
::: notes
Using version control offers numerous benefits, such as keeping track of every modification made to a file, which is essential in understanding the evolution of a project. It allows teams to work together without chaos, ensuring everyone’s changes are integrated smoothly and in an organized fashion. Imagine working on a group project where everyone contributes, but without version control, it would feel like herding cats!
:::
---
```

```bash
curl -X POST http://127.0.0.1:8000/tools/call/export  -F "file=@git.md" | jq '.job_id' > job_id.txt
```
The above command will return a job ID, which you can use to check the status of the export job.
Using curl, you can get the status, while its running (or any error)

```bash
curl -X GET http://127.0.0.1:8000/tools/call/export_status?job_id=$(cat job_id.txt | sed 's/"//g') 
```

Once the job is completed, you can download the PDF file using the job ID:

```bash
curl -X GET http://127.0.0.1:8000/tools/call/export?job_id=$(cat job_id.txt | sed 's/"//g') -o git.pdf
```

