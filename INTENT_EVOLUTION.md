# INTENT EVOLUTION: tool-triage-flow-automator

## 历史脉络与未尽构想 (Emergence Ledger)

### 诞生背景
传统的 GitHub 仓库在 Issue 和 PR 产生后常常陷入“未分流状态”——没有标签、缺少 Reviewer 导致 PR 被搁置积压、长期无效 Issue 堆积成山。通过编排官方 labeler 与 stale 最佳实践，我们构建了开箱即用的分流器。

### 未尽地平线 (Future Horizons)
1. **AI 智能语义打标扩展**：结合大模型对 Issue 正文做多分类预测（如 `kind/bug`, `kind/feature`, `area/security`）。
2. **动态负载均衡审查指派**：根据团队成员当前在审 PR 积压量，智能轮换指派评审人。
3. **PR 拆分建议器**：当检测到 PR 超过 1000 行变更时，根据 commit 拓扑提出原子拆分建议。
