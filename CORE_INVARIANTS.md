# CORE INVARIANTS: tool-triage-flow-automator

## 1. 绝对职责边界 (Single Responsibility & Bounded Context)
- `tool-triage-flow-automator` 专职负责 Issue 与 PR 的动态生命周期分流：路径标签自动打标 (`actions/labeler`)、长期沉寂议题自动归档 (`actions/stale`)、PR 变更行数大小门禁与审查人自动指派。
- 绝不侵入业务构建测试逻辑，不越界修改用户源码。

## 2. 离线确定性与仿真 (Deterministic Simulation)
- 提供离线路径匹配仿真器，在不连接 GitHub 远端的情况下，预测任意修改文件列表将触发的标签集合。
- 工作流文件严格遵循最小权限原则（Principle of Least Privilege），仅授予必要的 `pull-requests: write` 与 `issues: write`。

## 3. 防腐与合规验证 (Defensive Auditing)
- 严密校验 `.github/labeler.yml` 语法与工作流权限，杜绝因权限缺失导致的 CI 运行期死锁与报错。
