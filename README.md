# tool-triage-flow-automator

> **GitHub 议题与拉取请求自动化分流、智能路径打标、僵尸生命周期闭环与 PR 尺寸门禁编排引擎**  
> Universal CLI Facade (UCFS v1.0) 标准实现 | 100% 离线自洽 | 零第三方依赖 | GitHub 官方分流基线对齐

---

## 🌟 核心价值与实用性痛点解答

在日常开源协作与团队研发中，Issue 与 Pull Request 管理面临严重的分流痛点：
1. **代码变更无序积压**：提交的 PR 缺少标签，外部协作者与维护者无法快速分辨是文档改动、前端界面还是核心后端重构 [^1]。
2. **巨型 PR 审查噩梦**：没有尺寸门禁，开发者提交动辄两千行代码的超级 PR，审查者望而生畏导致代码积压变质 [^2]。
3. **僵尸议题污染积压**：未闭环的 Issue 长期无人跟进，历史脏数据消耗社区精力，缺少自动化清理闭环 [^3]。
4. **审查人指派依赖人肉提醒**：提了 PR 缺少自动分配机制，导致团队成员互相等待 [^4]。

`tool-triage-flow-automator` 一键解决上述协同分流痛点：
- **路径自动化打标**：自动合成 `.github/labeler.yml` 与工作流，修改 `docs/` 自动附加 `documentation`，修改 `core/` 自动附加 `backend`。
- **PR 尺寸分级门禁**：自动标注 `size/XS` 至 `size/XL`，对超千行 PR 提出原子拆分警示。
- **Stale 沉寂议题生命周期**：定时扫描无响应议题与 PR，发出友好警告并在超时后优雅归档。
- **离线路径仿真测试器**：提供毫秒级本地测试，输入改动文件列表即可精准预测打标结果。

---

## 🏛️ 技术思想源流与对标选型 (Heritage & Benchmarking)

| 对标项目 / 规范源流 | 类别 | 权威链接 | 核心思想 / 架构洞察 | 吸收借鉴点 | 取舍与舍弃理由 (Trade-offs) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **actions/labeler@v5** | 官方核心标准 | [GitHub Actions Labeler](https://github.com/actions/labeler) [^1] | 声明式基于变更文件 glob 路径的动态 PR 打标标准 | 吸收其最新 v5 版嵌套 glob 语法与权限隔离定义 | 补全本地离线仿真预测器，无需反复在 GitHub 调试 yaml |
| **CodelyTV/pr-size-labeler** | 社区高星实践 | [GitHub 仓库](https://github.com/CodelyTV/pr-size-labeler) [^2] | 敏捷研发代码审查门禁：PR 尺寸分级与超大 PR 警示 | 吸收其 XS/S/M/L/XL 变更阈值与非侵入式提示逻辑 | 将尺寸打标与全套分流工作流有机统一编排，避免碎片化配置 |
| **actions/stale@v9** | 官方运维标准 | [GitHub Actions Stale](https://github.com/actions/stale) [^3] | 异步定时 Cron 轮询与豁免标签（pinned/security）状态机 | 吸纳其友好提示词与安全豁免标签设计 | 去除冗余复杂的多轮警告，提供极简高信噪比清理闭环 |
| **kentaro-m/auto-assign-action** | 协同编排开源 | [GitHub 仓库](https://github.com/kentaro-m/auto-assign-action) [^4] | 自动指派审查人与组织团队轮换分配机制 | 吸收其配置文件驱动的 Reviewer 声明模式 | 结合本地工作流自动生成，避免手写配置拼写错误 |

---

## ⚡ 极速开始 (Quick Start in 3 Seconds)

```bash
# 1. 环境校验
python main.py setup

# 2. 为当前仓库一键脚手架并校验全套分流工作流
python main.py run

# 3. 运行离线单元测试 (100% 通过)
python main.py test

# 4. 核心组件健康诊断
python main.py health

# 5. 清理临时缓存
python main.py clean
```

### 高级用法：定制脚手架、校验与本地路径仿真

```bash
# 生成全套分流工作流 (.github/labeler.yml, stale.yml, pr-size.yml 等)
python main.py scaffold

# 本地离线仿真：预测给定文件变更将触发哪些标签
python main.py simulate docs/architecture.md core/engine.py

# 校验当前仓库的分流配置与 GitHub Actions 权限完备度
python main.py validate
```

---

## 🛡️ 架构与不变式

- **纯标准库实现**：无第三方依赖，内置基于 fnmatch 的路径模式匹配仿真器。
- **最小特权原则**：工作流显式声明最小必需权限（`contents: read`, `pull-requests: write`, `issues: write`），拒绝全权滥用。

---

## 🚫 Non-Goals (明确非目标)

1. **不干预构建与测试**：本工具专注议题与 PR 状态流转与打标，不负责 CI 编译与自动化测试执行。
2. **不越权关闭正常议题**：Stale 配置严格尊重 `pinned` 与 `security` 标签，绝不强行清理白名单议题。
3. **不替代代码审查本身**：PR 尺寸门禁仅作容量警示与提示建议，不强行阻断紧急热修复合入。

---

## 📚 引用脚注 (Footnotes)

[^1]: GitHub Actions Official Labeler: https://github.com/actions/labeler
[^2]: CodelyTV PR Size Labeler Action: https://github.com/CodelyTV/pr-size-labeler
[^3]: GitHub Actions Official Stale Bot: https://github.com/actions/stale
[^4]: Kentaro-m Auto Assign Pull Request Reviewer Action: https://github.com/kentaro-m/auto-assign-action
