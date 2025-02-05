# Getting started with Kestra

## 🚀 Quickstart

Start Kestra in a Docker container and create your first flow.

[Quickstart Video YT](https://www.youtube.com/watch?v=a2BZ7vOihjg)

```bash
docker run --pull=always --rm -it -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v /tmp:/tmp kestra/kestra:latest-full server local
```

Open <http://localhost:8080> in your browser.

### Inside Platform

- Workflows known as `Flows`
- Declared in YAML
- Works with any language

## Run a flow

You need three properties to run a flow:

- `id`: name of your flow
- `namespace`: environment for your flow (helps to separate dev and prod)
- `tasks`: list of tasks to execute in your flow

Example flow:

```yaml
id: getting_started
namespace: example
tasks:
  - id: hello_world
    type: io.kestra.core.tasks.log.Log
    message: Hello, World!
```

## Extra Concepts to get full power of Kestra

### Inputs

Instead of hardcoding values, especially repeating yourself, you can define them on the top bit like constant variables in other programming languages.

```yaml
inputs:
  - id: variable_name
    type: STRING
    defaults: example_string
```

`{{ inputs.variable_name }}`

### Outputs

Some tasks generate outputs. You can reference them in other tasks.

`{{ outputs.task_id.vars.output_name }}`

Super useful if you got files or variables you want to use later on.

### Triggers

Other than having to manually press execute, you can start a flow under certain conditions. Schedule, web hooks, or something else. Flexibility is key.

```yaml
triggers:
  - id: hour_manual
    type: io.kestra.core.triggers.types.Schedule
    cron: 0 * * * *
```

watched video [Automate Your Stock Market Portfolio for FREE (Python, Kestra, AWS Tutorial)](https://www.youtube.com/watch?v=3q8FbiR-t8g)
