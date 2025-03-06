# Vibe Coding Tutorial and Best Practices

Elaborate with LLM on the specs of the project (or just take one-shot)

```text
write a spec for an application, that will be a <something> clone. be as specific as possible. we're going to be using <python> for the backend.
```

IDE: Cursor or Windsurf

Tell what technologies you would use, how you want to code, what workflow you would follow in the rules section (kind of system message).

Model: claude-3.7-sonnet-thinking / Agent mode


```text
Descrption: How we should prefer to code

# Coding pattern preferences

- Always prefer simple solutions
- Avoid duplication of code whenever possible, which means checking for other areas of the codebase that might already have similar code and functionality (DRY principle)
- Write code that takes into account the different environments: dev, test, and prod
- You are careful to only make changes that are requested or you are confident are well understood and related to the change being requested
- When fixing an issue or bug, do not introduce a new pattern or technology without first exhausting all options for the existing implementation. and if you finally do this, make sure to remove the old implementation afterwards so we don't have duplicate logic.
- Keep the codebase very clean and organized.
- Avoid writing scripts in files if possible, especially if the script is likely only to be run once.
- Avoid having files over 200-300 lines of code. Refactor at that point.
- Mock data is only needed for tests, never mock data for dev or prod
- Never add stubbing or fake data patterns to code that affects the dev or prod environments
- Never override my .env file without first asking and confirming
```

```text
Descrption: This is the project's tech stack

# Technical stack

- Python for the backend
- html/js for the frontend
- SQL databases, never JSON file storage
- Separate databases for dev, test, and prod
- Elasticsearch for search, using elastic.co hosting
- Elastic.co will have dev and prod indexes
- Python tests
```

```text
Descrption: How I like to code (workflow)

# Coding workflow preferences

- Focus on the areas of code relevant to the task
- Do not touch code that is unrelated to the task
- Write thorough tests for all major functionality
- Avoid making major changes to the patterns and architecture of how a feature works, after it has shown to work well, unless explicitly instructed
- Always think about what other methods and areas of code might be affected by code changes
```

Copy the spec into prompt of IDE.

Be aware of how much context you give to the model. (e.g. "Start new for better results")

Always write tests and make sure they pass, do integration tests. Use popular stack.

example prompt for editing:

```text
enforce a maximum tag length limit of 20 chars, make sure we dont already have code for this, write tests for this after implementation
```

YOLO mode directly pushes everything (risky), manual mode asks for confirmation, auto mode is in between.

Commands can take up to 15 min to finish, but you can work on different tasks in different branches in differnet windows. Refactor code if needed. Commit often.

Replit on mobile is the future?


