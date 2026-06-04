# 仪哥安全智库 - 主题集群知识架构

> **架构模型**: Hub-and-Spoke（支柱-集群模型）
> **用途**: GEO内容架构优化，提升AI搜索引擎可见性和权威性

---

## 架构说明

### 核心概念

| 概念 | 英文 | 说明 |
|------|------|------|
| 支柱（Pillar） | Pillar Page | 核心主题的"完全指南"页面，3000-8000字，覆盖主题全貌，是GEO流量锚点 |
| 集群（Cluster） | Cluster | 围绕支柱的子主题深度文章，2000-5000字，覆盖具体场景和实操方法，是长尾流量入口 |
| 集群互联（Cross-link） | Cross-linking | 集群之间的双向语义链接，增强整个主题权威度 |

### 模型优势

1. **权威性信号**：支柱页面作为主题权威中心，AI搜索引擎识别为该领域的完整知识源
2. **语义覆盖**：集群覆盖长尾关键词，形成完整的语义网络
3. **内部链接**：支柱→集群→集群的链接结构，传递语义权重
4. **结构化数据**：每个支柱配备 FAQPage + Article JSON-LD，增强AI理解

---

## 支柱总览

| # | 支柱主题 | 集群数 | 总文章数 | Schema类型 |
|---|----------|--------|----------|------------|
| 1 | 安全运营中心（SOC）建设完全指南 | 6 | 10 | Article, BreadcrumbList, FAQPage |
| 2 | 企业风险评估与管控完全指南 | 4 | 6 | Article, BreadcrumbList, FAQPage |
| 3 | 应急管理体系建设完全指南 | 3 | 5 | Article, BreadcrumbList, FAQPage |
| 4 | 安全生产合规管理完全指南 | 3 | 5 | Article, BreadcrumbList, FAQPage |
| 5 | 工艺安全管理（PSM）完全指南 | 2 | 4 | Article, BreadcrumbList, FAQPage |
| 6 | 安全文化建设与行为安全完全指南 | 2 | 3 | Article, BreadcrumbList, FAQPage |
| 7 | 安全培训教育体系建设完全指南 | 2 | 3 | Article, BreadcrumbList, FAQPage |
| 8 | 网络安全与数据保护完全指南 | 2 | 3 | Article, BreadcrumbList, FAQPage |

---

## 支柱详情

### 安全运营中心（SOC）建设完全指南
> 从零到一搭建企业安全运营中心的系统性指南，涵盖组织架构、技术选型、运营流程和持续改进
>
> - **主关键词**: 安全运营中心建设
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: risk-assessment-guide, emergency-response-guide, compliance-management-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P1 | SIEM平台选型指南 | 2 | 92/100 | 高 |
| P1 | 日志源接入规范与最佳实践 | 2 | 85/100 | 中高 |
| P1 | SOC事件响应流程与SOP制定 | 2 | 88/100 | 高 |
| P2 | SOC合规要求与等保映射 | 1 | 80/100 | 中 |
| P2 | SOC团队人员配置与能力模型 | 1 | 78/100 | 中 |
| P3 | SOC建设预算估算与ROI分析 | 1 | 75/100 | 中低 |

### 企业风险评估与管控完全指南
> 系统化的企业风险识别、评估、管控和持续监控方法论
>
> - **主关键词**: 企业风险评估
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: soc-construction-guide, compliance-management-guide, safety-culture-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P1 | 风险识别方法论与工具 | 2 | 90/100 | 高 |
| P1 | 风险矩阵设计与等级评定 | 1 | 87/100 | 高 |
| P1 | 风险管控措施层级与实施 | 1 | 85/100 | 中高 |
| P2 | 动态风险评估与实时监控 | 1 | 82/100 | 中 |

### 应急管理体系建设完全指南
> 企业应急预案编制、演练、响应和恢复的完整体系
>
> - **主关键词**: 应急管理体系建设
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: soc-construction-guide, risk-assessment-guide, process-safety-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P1 | 应急预案编制规范与模板 | 2 | 91/100 | 高 |
| P1 | 应急演练策划与评估 | 1 | 86/100 | 中高 |
| P1 | 事故调查方法与根因分析 | 1 | 89/100 | 高 |

### 安全生产合规管理完全指南
> 等保、ISO 45001、安全生产法等法规标准的合规实施
>
> - **主关键词**: 安全生产合规管理
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: soc-construction-guide, risk-assessment-guide, safety-training-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P1 | ISO 45001职业健康安全管理体系实施 | 2 | 93/100 | 高 |
| P1 | 安全生产法律法规解读 | 1 | 88/100 | 高 |
| P1 | 等保2.0合规实施指南 | 1 | 86/100 | 中高 |

### 工艺安全管理（PSM）完全指南
> 化工及高危行业工艺安全管理的14要素实施指南
>
> - **主关键词**: 工艺安全管理
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: emergency-response-guide, risk-assessment-guide, compliance-management-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P1 | 工艺危害分析（PHA）方法 | 2 | 91/100 | 高 |
| P1 | 变更管理（MOC）程序设计 | 1 | 84/100 | 中高 |

### 安全文化建设与行为安全完全指南
> 企业安全文化评估、建设和持续改进方法论
>
> - **主关键词**: 安全文化建设
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: risk-assessment-guide, compliance-management-guide, safety-training-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P2 | 安全文化评估工具与方法 | 1 | 83/100 | 中 |
| P2 | 行为安全观察（BBS）实施指南 | 1 | 80/100 | 中 |

### 安全培训教育体系建设完全指南
> 企业安全培训需求分析、课程设计、效果评估和数字化培训平台建设
>
> - **主关键词**: 安全培训体系
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: compliance-management-guide, safety-culture-guide, risk-assessment-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P1 | 三级安全教育实施规范 | 1 | 90/100 | 高 |
| P2 | 安全培训效果评估与改进 | 1 | 79/100 | 中 |

### 网络安全与数据保护完全指南
> 企业网络安全体系规划、威胁防护、数据安全治理和个人信息保护合规
>
> - **主关键词**: 网络安全与数据保护
> - **目标字数**: 8000
> - **Schema**: Article, BreadcrumbList, FAQPage
> - **交叉链接**: soc-construction-guide, compliance-management-guide

| 优先级 | 集群主题 | 文章数 | GEO潜力 | 搜索量预估 |
| P1 | 数据分类分级与安全治理 | 1 | 87/100 | 高 |
| P1 | 个人信息保护合规（PIPL） | 1 | 89/100 | 高 |

---

## 优先创作清单（P1-P2）

以下集群建议优先创作内容：

| # | 支柱 | 集群 | 优先级 | GEO潜力 | 文章数 |
|---|------|------|--------|---------|--------|
| 1 | 安全生产合规管理完全指南 | ISO 45001职业健康安全管理体系实施 | P1 | 93/100 | 2 |
| 2 | 安全运营中心（SOC）建设完全指南 | SIEM平台选型指南 | P1 | 92/100 | 2 |
| 3 | 应急管理体系建设完全指南 | 应急预案编制规范与模板 | P1 | 91/100 | 2 |
| 4 | 工艺安全管理（PSM）完全指南 | 工艺危害分析（PHA）方法 | P1 | 91/100 | 2 |
| 5 | 企业风险评估与管控完全指南 | 风险识别方法论与工具 | P1 | 90/100 | 2 |
| 6 | 安全培训教育体系建设完全指南 | 三级安全教育实施规范 | P1 | 90/100 | 1 |
| 7 | 应急管理体系建设完全指南 | 事故调查方法与根因分析 | P1 | 89/100 | 1 |
| 8 | 网络安全与数据保护完全指南 | 个人信息保护合规（PIPL） | P1 | 89/100 | 1 |
| 9 | 安全运营中心（SOC）建设完全指南 | SOC事件响应流程与SOP制定 | P1 | 88/100 | 2 |
| 10 | 安全生产合规管理完全指南 | 安全生产法律法规解读 | P1 | 88/100 | 1 |
| 11 | 企业风险评估与管控完全指南 | 风险矩阵设计与等级评定 | P1 | 87/100 | 1 |
| 12 | 网络安全与数据保护完全指南 | 数据分类分级与安全治理 | P1 | 87/100 | 1 |
| 13 | 应急管理体系建设完全指南 | 应急演练策划与评估 | P1 | 86/100 | 1 |
| 14 | 安全生产合规管理完全指南 | 等保2.0合规实施指南 | P1 | 86/100 | 1 |
| 15 | 安全运营中心（SOC）建设完全指南 | 日志源接入规范与最佳实践 | P1 | 85/100 | 2 |
| 16 | 企业风险评估与管控完全指南 | 风险管控措施层级与实施 | P1 | 85/100 | 1 |
| 17 | 工艺安全管理（PSM）完全指南 | 变更管理（MOC）程序设计 | P1 | 84/100 | 1 |
| 18 | 安全文化建设与行为安全完全指南 | 安全文化评估工具与方法 | P2 | 83/100 | 1 |
| 19 | 企业风险评估与管控完全指南 | 动态风险评估与实时监控 | P2 | 82/100 | 1 |
| 20 | 安全运营中心（SOC）建设完全指南 | SOC合规要求与等保映射 | P2 | 80/100 | 1 |
| 21 | 安全文化建设与行为安全完全指南 | 行为安全观察（BBS）实施指南 | P2 | 80/100 | 1 |
| 22 | 安全培训教育体系建设完全指南 | 安全培训效果评估与改进 | P2 | 79/100 | 1 |
| 23 | 安全运营中心（SOC）建设完全指南 | SOC团队人员配置与能力模型 | P2 | 78/100 | 1 |

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `knowledge_graph.json` | 完整知识图谱JSON数据 |
| `seed_knowledge_clusters.py` | Django Management Command种子数据 |
| `cross_link_matrix.json` | 支柱间交叉链接矩阵 |
| `priority_cluster_list.json` | 优先创作清单（P1-P2） |
| `ARCHITECTURE.md` | 本架构文档 |

## 使用方式

```bash
# 1. 运行cluster_manager生成所有文件
python knowledge_graph/cluster_manager.py

# 2. 将seed文件复制到Django项目
cp knowledge_graph/subject_clusters/seed_knowledge_clusters.py yigeworks_django/knowledge/management/commands/

# 3. 在服务器上执行种子数据导入
python manage.py seed_knowledge_clusters
```