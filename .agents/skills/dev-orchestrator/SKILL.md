---
name: dev-orchestrator
description: 为采用 AI 开发工作流的 GitHub 项目初始化开发规则、拆分和分派 Issue、安排每日工作、核验审查和准备授权合并。
---

# AI 开发工作流

从项目根目录读取 `AGENTS.md`、`PROJECT.md` 和 `docs/workflow.md`。派发任务时使用 `docs/task-briefs.md` 中对应角色的格式。

- 初始化时先确定第一版交付标准、技术方案、项目风险边界和 CI 命令，再起草 Issue。
- 每日调度按 `docs/workflow.md` 给出可执行项、并行关系和逐项任务书。收到开发或审查回执时，核对 GitHub 当前提交和证据，再给下一角色的任务书。
- 用户要求某个具体角色时，仅执行该角色获授权的工作。
