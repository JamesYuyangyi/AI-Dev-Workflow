# AI 开发工作流

一套可复制到新项目的 GitHub 协作模板。你定目标和授权，AI 编排者（例如 ChatGPT）负责拆任务、排优先级和核验结果。开发、独立审查和合并按角色交接，各角色可以选用不同供应商的模型和工具。

## 新项目怎么开始

1. 在 GitHub 仓库首页点 **Use this template → Create a new repository**。
2. 和你选用的 AI 编排者说「我要用 AI 开发工作流开始一个新项目」，描述想做的产品，并提供新仓库链接。让它读取 [项目规则模板](PROJECT.md) 和 [工作流](docs/workflow.md)，一起确定第一版交付标准、技术方案、风险边界和测试命令，再建立第一批 Issue。
3. 在本地打开新仓库。Codex 可调用 `$dev-orchestrator`，Claude Code 可调用 `/dev-orchestrator`。也可以直接把 [任务书](docs/task-briefs.md) 发给对应的 AI 助手。
4. 填好[编排者指令模板](docs/orchestrator-instructions.md)，放进所用工具的项目指令，或在新会话开头发送。让编排者读取 GitHub，或提供当前 Issue、PR 和检查结果。在总控会话说「开工」领取任务和逐项提示词，每个执行中的 Issue 用独立会话接收[开发和审查回执](docs/task-briefs.md#开发回执)。

## 已有项目怎么用

让 AI 先读目标仓库现有的规则、模板和 CI，提出最小接入方案。优先复用已有的 Issue、测试和分支保护，从一个新的低风险 Issue 试跑。为新任务明确生效日期，进行中的任务按原约定交付。

## 自动检查

`工作流检查` 验证模板、规则文件和检查程序。PR 另有 `PR 信息检查`，检查关联 Issue、风险、变更说明和验证证据是否填写。创建新项目后，在 CI 中加入该项目的实际测试命令。

如需让 GitHub 阻止检查失败的 PR 合并，在目标项目的分支保护规则中把这两项设为必需检查。独立审查、产品验收和合并授权由工作流中的对应角色核验。

本地运行 `python -B -m unittest discover -s tests -v` 即可验证模板与检查程序。

## 许可证

本模板采用 [MIT 许可证](LICENSE)。
