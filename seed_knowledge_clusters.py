# -*- coding: utf-8 -*-
"""
Django Management Command 种子数据
使用方式: python manage.py seed_knowledge_clusters

此文件由 cluster_manager.py 自动生成
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from knowledge.models import KnowledgeCategory, KnowledgeTag, KnowledgeArticle, ArticleSection


class Command(BaseCommand):
    help = "种子数据：导入主题集群知识架构"

    def handle(self, *args, **options):
        # 获取或创建管理员用户
        admin, _ = User.objects.get_or_create(username="admin", defaults={"is_superuser": True, "is_staff": True})

        # ═══════════════════════════════════════
        # 支柱: 安全运营中心（SOC）建设完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="soc-construction-guide",
            defaults={
                "name_zh": "安全运营中心（SOC）建设完全指南",
                "name_en": "Complete Guide to Building a Security Operations Center (SOC)",
                "tier": "domain",
                "description_zh": "从零到一搭建企业安全运营中心的系统性指南，涵盖组织架构、技术选型、运营流程和持续改进",
                "order": 0,
            }
        )

        # 集群: SIEM平台选型指南
        cat_siem-selection, _ = KnowledgeCategory.objects.get_or_create(
            slug="siem-selection",
            defaults={
                "name_zh": "SIEM平台选型指南",
                "name_en": "SIEM Platform Selection Guide",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "主流SIEM平台对比与选型方法论",
                "order": 1,
            }
        )

        # 文章: Splunk vs Elastic SIEM vs QRadar：企业级SIEM全面对比
        article_siem-platform-comparison, _ = KnowledgeArticle.objects.get_or_create(
            slug="siem-platform-comparison",
            defaults={
                "title_zh": "Splunk vs Elastic SIEM vs QRadar：企业级SIEM全面对比",
                "title_en": "Splunk vs Elastic SIEM vs QRadar: Enterprise SIEM Comparison",
                "category": cat_siem-selection,
                "summary_zh": "1. 三大平台核心架构对比",
                "content_zh": "# Splunk vs Elastic SIEM vs QRadar：企业级SIEM全面对比\n\n1. 三大平台核心架构对比\n2. 日志采集能力对比\n3. 关联分析引擎对比\n4. 许可证成本对比\n5. 部署复杂度对比\n6. 适合场景推荐",
                "ai_keywords": "SIEM选型,Splunk对比,Elastic SIEM,QRadar",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="siem选型", defaults={"name_zh": "SIEM选型"})
        article_siem-platform-comparison.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="splunk对比", defaults={"name_zh": "Splunk对比"})
        article_siem-platform-comparison.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="elastic-siem", defaults={"name_zh": "Elastic SIEM"})
        article_siem-platform-comparison.tags.add(tag)

        # 文章: SIEM部署架构设计：集中式 vs 分布式 vs 混合式
        article_siem-deployment-architecture, _ = KnowledgeArticle.objects.get_or_create(
            slug="siem-deployment-architecture",
            defaults={
                "title_zh": "SIEM部署架构设计：集中式 vs 分布式 vs 混合式",
                "title_en": "SIEM Deployment Architecture: Centralized vs Distributed vs Hybrid",
                "category": cat_siem-selection,
                "summary_zh": "1. 三种部署模式详解",
                "content_zh": "# SIEM部署架构设计：集中式 vs 分布式 vs 混合式\n\n1. 三种部署模式详解\n2. 各模式优缺点分析\n3. 不同企业规模的推荐方案\n4. 日志吞吐量评估方法\n5. 高可用设计要点",
                "ai_keywords": "SIEM部署,SIEM架构,日志平台设计",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="siem部署", defaults={"name_zh": "SIEM部署"})
        article_siem-deployment-architecture.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="siem架构", defaults={"name_zh": "SIEM架构"})
        article_siem-deployment-architecture.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="日志平台设计", defaults={"name_zh": "日志平台设计"})
        article_siem-deployment-architecture.tags.add(tag)

        # 集群: 日志源接入规范与最佳实践
        cat_log-source-integration, _ = KnowledgeCategory.objects.get_or_create(
            slug="log-source-integration",
            defaults={
                "name_zh": "日志源接入规范与最佳实践",
                "name_en": "Log Source Integration Standards and Best Practices",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "各类安全日志源的标准化接入方法",
                "order": 1,
            }
        )

        # 文章: Windows事件日志接入：安全审计事件全解析
        article_windows-event-log-integration, _ = KnowledgeArticle.objects.get_or_create(
            slug="windows-event-log-integration",
            defaults={
                "title_zh": "Windows事件日志接入：安全审计事件全解析",
                "title_en": "Windows Event Log Integration: Security Audit Events Analysis",
                "category": cat_log-source-integration,
                "summary_zh": "1. Windows安全事件ID分类",
                "content_zh": "# Windows事件日志接入：安全审计事件全解析\n\n1. Windows安全事件ID分类\n2. 需采集的关键事件清单\n3. WEF集中收集配置\n4. Syslog转发配置\n5. 常见接入问题排查",
                "ai_keywords": "Windows安全日志,事件ID,WEF配置",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="windows安全日志", defaults={"name_zh": "Windows安全日志"})
        article_windows-event-log-integration.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="事件id", defaults={"name_zh": "事件ID"})
        article_windows-event-log-integration.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="wef配置", defaults={"name_zh": "WEF配置"})
        article_windows-event-log-integration.tags.add(tag)

        # 文章: Linux系统日志与云原生日志接入指南
        article_linux-cloud-log-integration, _ = KnowledgeArticle.objects.get_or_create(
            slug="linux-cloud-log-integration",
            defaults={
                "title_zh": "Linux系统日志与云原生日志接入指南",
                "title_en": "Linux System Logs and Cloud-Native Log Integration Guide",
                "category": cat_log-source-integration,
                "summary_zh": "1. syslog/rsyslog配置",
                "content_zh": "# Linux系统日志与云原生日志接入指南\n\n1. syslog/rsyslog配置\n2. Docker容器日志采集\n3. K8s集群日志采集\n4. 云平台日志API接入\n5. 日志格式标准化规范",
                "ai_keywords": "Linux日志,容器日志采集,K8s日志",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="linux日志", defaults={"name_zh": "Linux日志"})
        article_linux-cloud-log-integration.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="容器日志采集", defaults={"name_zh": "容器日志采集"})
        article_linux-cloud-log-integration.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="k8s日志", defaults={"name_zh": "K8s日志"})
        article_linux-cloud-log-integration.tags.add(tag)

        # 集群: SOC事件响应流程与SOP制定
        cat_soc-incident-response, _ = KnowledgeCategory.objects.get_or_create(
            slug="soc-incident-response",
            defaults={
                "name_zh": "SOC事件响应流程与SOP制定",
                "name_en": "SOC Incident Response Procedures and SOP Development",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "标准化安全事件响应流程设计",
                "order": 1,
            }
        )

        # 文章: 安全事件分级分类标准与响应SLA制定
        article_incident-classification-sla, _ = KnowledgeArticle.objects.get_or_create(
            slug="incident-classification-sla",
            defaults={
                "title_zh": "安全事件分级分类标准与响应SLA制定",
                "title_en": "Security Incident Classification Standards and Response SLA",
                "category": cat_soc-incident-response,
                "summary_zh": "1. 事件严重性分级标准（P1-P4）",
                "content_zh": "# 安全事件分级分类标准与响应SLA制定\n\n1. 事件严重性分级标准（P1-P4）\n2. 事件类型分类（恶意软件/数据泄露/DDoS等）\n3. 各级别响应时间SLA\n4. 升级机制设计\n5. SLA监控与度量",
                "ai_keywords": "事件分级,响应SLA,安全事件分类",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="事件分级", defaults={"name_zh": "事件分级"})
        article_incident-classification-sla.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="响应sla", defaults={"name_zh": "响应SLA"})
        article_incident-classification-sla.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全事件分类", defaults={"name_zh": "安全事件分类"})
        article_incident-classification-sla.tags.add(tag)

        # 文章: SOC事件响应SOP模板：从检测到闭环的完整流程
        article_soc-incident-sop-template, _ = KnowledgeArticle.objects.get_or_create(
            slug="soc-incident-sop-template",
            defaults={
                "title_zh": "SOC事件响应SOP模板：从检测到闭环的完整流程",
                "title_en": "SOC Incident Response SOP Template: Detection to Closure",
                "category": cat_soc-incident-response,
                "summary_zh": "1. 检测与告警阶段SOP",
                "content_zh": "# SOC事件响应SOP模板：从检测到闭环的完整流程\n\n1. 检测与告警阶段SOP\n2. 初步研判阶段SOP\n3. 事件处置阶段SOP\n4. 根因分析阶段SOP\n5. 恢复与复盘阶段SOP\n6. SOP维护更新机制",
                "ai_keywords": "事件响应SOP,SOC流程,安全事件处置",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="事件响应sop", defaults={"name_zh": "事件响应SOP"})
        article_soc-incident-sop-template.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="soc流程", defaults={"name_zh": "SOC流程"})
        article_soc-incident-sop-template.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全事件处置", defaults={"name_zh": "安全事件处置"})
        article_soc-incident-sop-template.tags.add(tag)

        # 集群: SOC合规要求与等保映射
        cat_soc-compliance, _ = KnowledgeCategory.objects.get_or_create(
            slug="soc-compliance",
            defaults={
                "name_zh": "SOC合规要求与等保映射",
                "name_en": "SOC Compliance Requirements and Classiﬁed Protection Mapping",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "SOC建设相关的合规标准要求",
                "order": 2,
            }
        )

        # 文章: 等保2.0对安全运营中心的具体要求解读
        article_djb-2-0-soc-requirements, _ = KnowledgeArticle.objects.get_or_create(
            slug="djb-2-0-soc-requirements",
            defaults={
                "title_zh": "等保2.0对安全运营中心的具体要求解读",
                "title_en": "Classiﬁed Protection 2.0 Requirements for SOC",
                "category": cat_soc-compliance,
                "summary_zh": "1. 等保三级安全运维要求",
                "content_zh": "# 等保2.0对安全运营中心的具体要求解读\n\n1. 等保三级安全运维要求\n2. SOC建设对应控制点\n3. 审计日志留存要求\n4. 事件通报要求\n5. 合规差距分析方法",
                "ai_keywords": "等保2.0 SOC,安全运维合规,等保三级",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="等保2.0-soc", defaults={"name_zh": "等保2.0 SOC"})
        article_djb-2-0-soc-requirements.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全运维合规", defaults={"name_zh": "安全运维合规"})
        article_djb-2-0-soc-requirements.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="等保三级", defaults={"name_zh": "等保三级"})
        article_djb-2-0-soc-requirements.tags.add(tag)

        # 集群: SOC团队人员配置与能力模型
        cat_soc-staffing, _ = KnowledgeCategory.objects.get_or_create(
            slug="soc-staffing",
            defaults={
                "name_zh": "SOC团队人员配置与能力模型",
                "name_en": "SOC Team Staﬃng and Competency Model",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "SOC团队角色定义、人员编制和能力要求",
                "order": 2,
            }
        )

        # 文章: SOC岗位体系设计：L1/L2/L3分析师能力模型
        article_soc-analyst-competency-model, _ = KnowledgeArticle.objects.get_or_create(
            slug="soc-analyst-competency-model",
            defaults={
                "title_zh": "SOC岗位体系设计：L1/L2/L3分析师能力模型",
                "title_en": "SOC Role System Design: L1/L2/L3 Analyst Competency Model",
                "category": cat_soc-staffing,
                "summary_zh": "1. SOC组织架构模式（集中式/分布式/混合式）",
                "content_zh": "# SOC岗位体系设计：L1/L2/L3分析师能力模型\n\n1. SOC组织架构模式（集中式/分布式/混合式）\n2. L1初级分析师职责与技能\n3. L2高级分析师职责与技能\n4. L3威胁猎手职责与技能\n5. 人员编制计算方法\n6. 值班排班最佳实践",
                "ai_keywords": "SOC岗位,安全分析师,SOC人员配置",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="soc岗位", defaults={"name_zh": "SOC岗位"})
        article_soc-analyst-competency-model.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全分析师", defaults={"name_zh": "安全分析师"})
        article_soc-analyst-competency-model.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="soc人员配置", defaults={"name_zh": "SOC人员配置"})
        article_soc-analyst-competency-model.tags.add(tag)

        # 集群: SOC建设预算估算与ROI分析
        cat_soc-budget, _ = KnowledgeCategory.objects.get_or_create(
            slug="soc-budget",
            defaults={
                "name_zh": "SOC建设预算估算与ROI分析",
                "name_en": "SOC Budget Estimation and ROI Analysis",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "SOC建设各阶段成本估算与投资回报分析",
                "order": 3,
            }
        )

        # 文章: SOC建设预算清单：硬件/软件/人力/运营四维成本
        article_soc-budget-breakdown, _ = KnowledgeArticle.objects.get_or_create(
            slug="soc-budget-breakdown",
            defaults={
                "title_zh": "SOC建设预算清单：硬件/软件/人力/运营四维成本",
                "title_en": "SOC Budget Breakdown: Hardware/Software/Staffing/Operations",
                "category": cat_soc-budget,
                "summary_zh": "1. 一次性投入（硬件/软件许可/实施）",
                "content_zh": "# SOC建设预算清单：硬件/软件/人力/运营四维成本\n\n1. 一次性投入（硬件/软件许可/实施）\n2. 年度运营成本（人力/维护/培训）\n3. 不同规模企业预算参考\n4. 隐性成本容易被忽略的项\n5. ROI量化评估方法",
                "ai_keywords": "SOC预算,安全运营成本,SOC ROI",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="soc预算", defaults={"name_zh": "SOC预算"})
        article_soc-budget-breakdown.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全运营成本", defaults={"name_zh": "安全运营成本"})
        article_soc-budget-breakdown.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="soc-roi", defaults={"name_zh": "SOC ROI"})
        article_soc-budget-breakdown.tags.add(tag)


        # ═══════════════════════════════════════
        # 支柱: 企业风险评估与管控完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="risk-assessment-guide",
            defaults={
                "name_zh": "企业风险评估与管控完全指南",
                "name_en": "Complete Guide to Enterprise Risk Assessment and Management",
                "tier": "domain",
                "description_zh": "系统化的企业风险识别、评估、管控和持续监控方法论",
                "order": 0,
            }
        )

        # 集群: 风险识别方法论与工具
        cat_risk-identification, _ = KnowledgeCategory.objects.get_or_create(
            slug="risk-identification",
            defaults={
                "name_zh": "风险识别方法论与工具",
                "name_en": "Risk Identiﬁcation Methodology and Tools",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "系统化风险识别的流程和方法",
                "order": 1,
            }
        )

        # 文章: JSA/HAZOP/LOTO/LER：四大风险识别方法对比与适用场景
        article_risk-identification-methods-comparison, _ = KnowledgeArticle.objects.get_or_create(
            slug="risk-identification-methods-comparison",
            defaults={
                "title_zh": "JSA/HAZOP/LOTO/LER：四大风险识别方法对比与适用场景",
                "title_en": "JSA/HAZOP/LOTO/LER: Four Risk Identiﬁcation Methods Compared",
                "category": cat_risk-identification,
                "summary_zh": "1. JSA工作安全分析法详解",
                "content_zh": "# JSA/HAZOP/LOTO/LER：四大风险识别方法对比与适用场景\n\n1. JSA工作安全分析法详解\n2. HAZOP危险与可操作性研究\n3. LOTO锁标管理\n4. LER岗位风险评估\n5. 各方法适用场景对照表\n6. 组合使用最佳实践",
                "ai_keywords": "JSA方法,HAZOP分析,LOTO管理,风险识别",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="jsa方法", defaults={"name_zh": "JSA方法"})
        article_risk-identification-methods-comparison.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="hazop分析", defaults={"name_zh": "HAZOP分析"})
        article_risk-identification-methods-comparison.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="loto管理", defaults={"name_zh": "LOTO管理"})
        article_risk-identification-methods-comparison.tags.add(tag)

        # 文章: 企业风险登记册（Risk Register）建立与维护指南
        article_risk-register-guide, _ = KnowledgeArticle.objects.get_or_create(
            slug="risk-register-guide",
            defaults={
                "title_zh": "企业风险登记册（Risk Register）建立与维护指南",
                "title_en": "Enterprise Risk Register: Creation and Maintenance Guide",
                "category": cat_risk-identification,
                "summary_zh": "1. 风险登记册核心字段设计",
                "content_zh": "# 企业风险登记册（Risk Register）建立与维护指南\n\n1. 风险登记册核心字段设计\n2. 风险编号与分类规则\n3. 评估标准定义（可能性x后果）\n4. 风险登记册模板\n5. 动态更新与评审机制",
                "ai_keywords": "风险登记册,风险清单,风险管理模板",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="风险登记册", defaults={"name_zh": "风险登记册"})
        article_risk-register-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="风险清单", defaults={"name_zh": "风险清单"})
        article_risk-register-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="风险管理模板", defaults={"name_zh": "风险管理模板"})
        article_risk-register-guide.tags.add(tag)

        # 集群: 风险矩阵设计与等级评定
        cat_risk-matrix, _ = KnowledgeCategory.objects.get_or_create(
            slug="risk-matrix",
            defaults={
                "name_zh": "风险矩阵设计与等级评定",
                "name_en": "Risk Matrix Design and Rating",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "定量与定性风险评估矩阵的设计方法",
                "order": 1,
            }
        )

        # 文章: 5x5风险矩阵设计详解：从可能性到后果的量化评分
        article_risk-matrix-5x5-design, _ = KnowledgeArticle.objects.get_or_create(
            slug="risk-matrix-5x5-design",
            defaults={
                "title_zh": "5x5风险矩阵设计详解：从可能性到后果的量化评分",
                "title_en": "5x5 Risk Matrix Design: Quantitative Scoring from Likelihood to Consequence",
                "category": cat_risk-matrix,
                "summary_zh": "1. 风险矩阵原理",
                "content_zh": "# 5x5风险矩阵设计详解：从可能性到后果的量化评分\n\n1. 风险矩阵原理\n2. 可能性等级定义（1-5级）\n3. 后果严重性等级定义（1-5级）\n4. 风险等级划分（可接受/需管控/不可接受）\n5. ALARP原则\n6. 风险矩阵局限性及改进",
                "ai_keywords": "风险矩阵,5x5矩阵,风险评估等级",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="风险矩阵", defaults={"name_zh": "风险矩阵"})
        article_risk-matrix-5x5-design.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="5x5矩阵", defaults={"name_zh": "5x5矩阵"})
        article_risk-matrix-5x5-design.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="风险评估等级", defaults={"name_zh": "风险评估等级"})
        article_risk-matrix-5x5-design.tags.add(tag)

        # 集群: 风险管控措施层级与实施
        cat_risk-control-measures, _ = KnowledgeCategory.objects.get_or_create(
            slug="risk-control-measures",
            defaults={
                "name_zh": "风险管控措施层级与实施",
                "name_en": "Hierarchy of Risk Controls and Implementation",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "基于控制层级的风险管控措施选择与实施",
                "order": 1,
            }
        )

        # 文章: 本质安全到个人防护：风险管控措施五层级详解
        article_hierarchy-of-controls, _ = KnowledgeArticle.objects.get_or_create(
            slug="hierarchy-of-controls",
            defaults={
                "title_zh": "本质安全到个人防护：风险管控措施五层级详解",
                "title_en": "Inherent Safety to PPE: Five Levels of Risk Control Measures",
                "category": cat_risk-control-measures,
                "summary_zh": "1. 第一层：消除/替代（本质安全）",
                "content_zh": "# 本质安全到个人防护：风险管控措施五层级详解\n\n1. 第一层：消除/替代（本质安全）\n2. 第二层：工程控制\n3. 第三层：管理控制\n4. 第四层：行政控制\n5. 第五层：个人防护装备\n6. 各层级有效性对比\n7. 组合控制措施设计方法",
                "ai_keywords": "风险管控层级,本质安全,工程控制,安全措施",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="风险管控层级", defaults={"name_zh": "风险管控层级"})
        article_hierarchy-of-controls.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="本质安全", defaults={"name_zh": "本质安全"})
        article_hierarchy-of-controls.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="工程控制", defaults={"name_zh": "工程控制"})
        article_hierarchy-of-controls.tags.add(tag)

        # 集群: 动态风险评估与实时监控
        cat_dynamic-risk-assessment, _ = KnowledgeCategory.objects.get_or_create(
            slug="dynamic-risk-assessment",
            defaults={
                "name_zh": "动态风险评估与实时监控",
                "name_en": "Dynamic Risk Assessment and Real-time Monitoring",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "作业现场动态风险评估方法",
                "order": 2,
            }
        )

        # 文章: 作业前动态风险评估（Take 5 / STA）实施指南
        article_take-5-risk-assessment, _ = KnowledgeArticle.objects.get_or_create(
            slug="take-5-risk-assessment",
            defaults={
                "title_zh": "作业前动态风险评估（Take 5 / STA）实施指南",
                "title_en": "Pre-task Dynamic Risk Assessment (Take 5 / STA) Guide",
                "category": cat_dynamic-risk-assessment,
                "summary_zh": "1. Take 5五步法",
                "content_zh": "# 作业前动态风险评估（Take 5 / STA）实施指南\n\n1. Take 5五步法\n2. STA安全任务分析\n3. 动态风险 vs 静态风险\n4. 现场快速评估工具\n5. 数字化动态风险评估方案",
                "ai_keywords": "动态风险评估,Take 5,STA安全分析",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="动态风险评估", defaults={"name_zh": "动态风险评估"})
        article_take-5-risk-assessment.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="take-5", defaults={"name_zh": "Take 5"})
        article_take-5-risk-assessment.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="sta安全分析", defaults={"name_zh": "STA安全分析"})
        article_take-5-risk-assessment.tags.add(tag)


        # ═══════════════════════════════════════
        # 支柱: 应急管理体系建设完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="emergency-response-guide",
            defaults={
                "name_zh": "应急管理体系建设完全指南",
                "name_en": "Complete Guide to Emergency Response Management System",
                "tier": "domain",
                "description_zh": "企业应急预案编制、演练、响应和恢复的完整体系",
                "order": 0,
            }
        )

        # 集群: 应急预案编制规范与模板
        cat_emergency-plan-writing, _ = KnowledgeCategory.objects.get_or_create(
            slug="emergency-plan-writing",
            defaults={
                "name_zh": "应急预案编制规范与模板",
                "name_en": "Emergency Plan Writing Standards and Templates",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "各类应急预案的标准编写方法",
                "order": 1,
            }
        )

        # 文章: 生产安全事故应急预案编制指南（GB/T 29639对照）
        article_emergency-plan-gb-29639, _ = KnowledgeArticle.objects.get_or_create(
            slug="emergency-plan-gb-29639",
            defaults={
                "title_zh": "生产安全事故应急预案编制指南（GB/T 29639对照）",
                "title_en": "Production Safety Incident Emergency Plan Writing Guide (GB/T 29639)",
                "category": cat_emergency-plan-writing,
                "summary_zh": "1. GB/T 29639核心要求",
                "content_zh": "# 生产安全事故应急预案编制指南（GB/T 29639对照）\n\n1. GB/T 29639核心要求\n2. 综合应急预案结构\n3. 专项应急预案模板\n4. 现场处置方案模板\n5. 应急资源调查清单\n6. 预案评审与备案流程",
                "ai_keywords": "应急预案编制,GB/T 29639,事故应急预案",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="应急预案编制", defaults={"name_zh": "应急预案编制"})
        article_emergency-plan-gb-29639.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="gb-t-29639", defaults={"name_zh": "GB/T 29639"})
        article_emergency-plan-gb-29639.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="事故应急预案", defaults={"name_zh": "事故应急预案"})
        article_emergency-plan-gb-29639.tags.add(tag)

        # 文章: 消防应急预案编制要点与实战模板
        article_fire-emergency-plan-template, _ = KnowledgeArticle.objects.get_or_create(
            slug="fire-emergency-plan-template",
            defaults={
                "title_zh": "消防应急预案编制要点与实战模板",
                "title_en": "Fire Emergency Plan: Key Points and Practical Templates",
                "category": cat_emergency-plan-writing,
                "summary_zh": "1. 消防应急预案必备要素",
                "content_zh": "# 消防应急预案编制要点与实战模板\n\n1. 消防应急预案必备要素\n2. 火灾风险场景分类\n3. 疏散路线设计方法\n4. 应急组织架构\n5. 消防设施联动清单\n6. 预案模板下载",
                "ai_keywords": "消防应急预案,火灾应急预案,疏散方案",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="消防应急预案", defaults={"name_zh": "消防应急预案"})
        article_fire-emergency-plan-template.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="火灾应急预案", defaults={"name_zh": "火灾应急预案"})
        article_fire-emergency-plan-template.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="疏散方案", defaults={"name_zh": "疏散方案"})
        article_fire-emergency-plan-template.tags.add(tag)

        # 集群: 应急演练策划与评估
        cat_emergency-drill, _ = KnowledgeCategory.objects.get_or_create(
            slug="emergency-drill",
            defaults={
                "name_zh": "应急演练策划与评估",
                "name_en": "Emergency Drill Planning and Evaluation",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "应急演练的设计、执行和效果评估",
                "order": 1,
            }
        )

        # 文章: 应急演练类型选择：桌面推演 vs 功能演练 vs 全面演练
        article_emergency-drill-types, _ = KnowledgeArticle.objects.get_or_create(
            slug="emergency-drill-types",
            defaults={
                "title_zh": "应急演练类型选择：桌面推演 vs 功能演练 vs 全面演练",
                "title_en": "Emergency Drill Types: Tabletop vs Functional vs Full-scale",
                "category": cat_emergency-drill,
                "summary_zh": "1. 桌面推演（Tabletop）",
                "content_zh": "# 应急演练类型选择：桌面推演 vs 功能演练 vs 全面演练\n\n1. 桌面推演（Tabletop）\n2. 功能演练（Functional）\n3. 全面演练（Full-scale）\n4. 各类型适用场景\n5. 演练频率建议\n6. 演练计划模板",
                "ai_keywords": "应急演练,桌面推演,全面演练,功能演练",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="应急演练", defaults={"name_zh": "应急演练"})
        article_emergency-drill-types.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="桌面推演", defaults={"name_zh": "桌面推演"})
        article_emergency-drill-types.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="全面演练", defaults={"name_zh": "全面演练"})
        article_emergency-drill-types.tags.add(tag)

        # 集群: 事故调查方法与根因分析
        cat_incident-investigation, _ = KnowledgeCategory.objects.get_or_create(
            slug="incident-investigation",
            defaults={
                "name_zh": "事故调查方法与根因分析",
                "name_en": "Incident Investigation Methods and Root Cause Analysis",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "系统化的事故调查与根因分析方法",
                "order": 1,
            }
        )

        # 文章: 事故调查5Why法、鱼骨图与故障树分析实战
        article_incident-investigation-rca-methods, _ = KnowledgeArticle.objects.get_or_create(
            slug="incident-investigation-rca-methods",
            defaults={
                "title_zh": "事故调查5Why法、鱼骨图与故障树分析实战",
                "title_en": "Incident Investigation: 5-Why, Fishbone, and Fault Tree in Practice",
                "category": cat_incident-investigation,
                "summary_zh": "1. 事故调查基本流程",
                "content_zh": "# 事故调查5Why法、鱼骨图与故障树分析实战\n\n1. 事故调查基本流程\n2. 5Why分析法详解与案例\n3. 鱼骨图（石川图）绘制方法\n4. 故障树分析（FTA）入门\n5. 根因 vs 直接原因 vs 贡献因素\n6. 调查报告撰写规范",
                "ai_keywords": "事故调查,根因分析,5Why,鱼骨图,故障树",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="事故调查", defaults={"name_zh": "事故调查"})
        article_incident-investigation-rca-methods.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="根因分析", defaults={"name_zh": "根因分析"})
        article_incident-investigation-rca-methods.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="5why", defaults={"name_zh": "5Why"})
        article_incident-investigation-rca-methods.tags.add(tag)


        # ═══════════════════════════════════════
        # 支柱: 安全生产合规管理完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="compliance-management-guide",
            defaults={
                "name_zh": "安全生产合规管理完全指南",
                "name_en": "Complete Guide to Work Safety Compliance Management",
                "tier": "domain",
                "description_zh": "等保、ISO 45001、安全生产法等法规标准的合规实施",
                "order": 0,
            }
        )

        # 集群: ISO 45001职业健康安全管理体系实施
        cat_iso45001-implementation, _ = KnowledgeCategory.objects.get_or_create(
            slug="iso45001-implementation",
            defaults={
                "name_zh": "ISO 45001职业健康安全管理体系实施",
                "name_en": "ISO 45001 OH&S Management System Implementation",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "ISO 45001标准解读与认证实施",
                "order": 1,
            }
        )

        # 文章: ISO 45001:2018条款逐条解读与实施要点
        article_iso-45001-clauses-guide, _ = KnowledgeArticle.objects.get_or_create(
            slug="iso-45001-clauses-guide",
            defaults={
                "title_zh": "ISO 45001:2018条款逐条解读与实施要点",
                "title_en": "ISO 45001:2018 Clause-by-Clause Interpretation and Implementation",
                "category": cat_iso45001-implementation,
                "summary_zh": "1. 范围与引用标准",
                "content_zh": "# ISO 45001:2018条款逐条解读与实施要点\n\n1. 范围与引用标准\n2. 组织环境与相关方\n3. 领导作用与工作人员协商\n4. 策划（风险机遇）\n5. 支持（资源/能力/意识/沟通/文件）\n6. 运行（消除危险/变更管理/采购）\n7. 绩效评价（监视/内审/管理评审）\n8. 改进（事件/不符合/纠正措施）",
                "ai_keywords": "ISO 45001,职业健康安全,OHSE体系",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="iso-45001", defaults={"name_zh": "ISO 45001"})
        article_iso-45001-clauses-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="职业健康安全", defaults={"name_zh": "职业健康安全"})
        article_iso-45001-clauses-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="ohse体系", defaults={"name_zh": "OHSE体系"})
        article_iso-45001-clauses-guide.tags.add(tag)

        # 文章: ISO 45001认证全流程：从准备到拿证的完整攻略
        article_iso-45001-certification-process, _ = KnowledgeArticle.objects.get_or_create(
            slug="iso-45001-certification-process",
            defaults={
                "title_zh": "ISO 45001认证全流程：从准备到拿证的完整攻略",
                "title_en": "ISO 45001 Certification: Complete Guide from Preparation to Certificate",
                "category": cat_iso45001-implementation,
                "summary_zh": "1. 认证条件与适用范围",
                "content_zh": "# ISO 45001认证全流程：从准备到拿证的完整攻略\n\n1. 认证条件与适用范围\n2. 体系建立阶段（差距分析→文件编制→试运行）\n3. 内部审核准备\n4. 管理评审\n5. 外部审核流程\n6. 常见不符合项与整改\n7. 证书维护与监督审核",
                "ai_keywords": "ISO 45001认证,体系认证流程,职业安全认证",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="iso-45001认证", defaults={"name_zh": "ISO 45001认证"})
        article_iso-45001-certification-process.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="体系认证流程", defaults={"name_zh": "体系认证流程"})
        article_iso-45001-certification-process.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="职业安全认证", defaults={"name_zh": "职业安全认证"})
        article_iso-45001-certification-process.tags.add(tag)

        # 集群: 安全生产法律法规解读
        cat_work-safety-law, _ = KnowledgeCategory.objects.get_or_create(
            slug="work-safety-law",
            defaults={
                "name_zh": "安全生产法律法规解读",
                "name_en": "Work Safety Laws and Regulations Interpretation",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "核心安全生产法律法规条文解读",
                "order": 1,
            }
        )

        # 文章: 《安全生产法》2024修订版企业责任条款全解析
        article_work-safety-law-2024-enterprise, _ = KnowledgeArticle.objects.get_or_create(
            slug="work-safety-law-2024-enterprise",
            defaults={
                "title_zh": "《安全生产法》2024修订版企业责任条款全解析",
                "title_en": "Work Safety Law 2024 Revision: Enterprise Responsibility Clauses",
                "category": cat_work-safety-law,
                "summary_zh": "1. 企业的七项法定责任",
                "content_zh": "# 《安全生产法》2024修订版企业责任条款全解析\n\n1. 企业的七项法定责任\n2. 主要负责人职责\n3. 安全管理机构与人员配置要求\n4. 安全生产投入保障\n5. 事故隐患排查治理义务\n6. 法律责任与处罚标准\n7. 企业合规自查清单",
                "ai_keywords": "安全生产法,企业安全责任,安全法修订",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全生产法", defaults={"name_zh": "安全生产法"})
        article_work-safety-law-2024-enterprise.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="企业安全责任", defaults={"name_zh": "企业安全责任"})
        article_work-safety-law-2024-enterprise.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全法修订", defaults={"name_zh": "安全法修订"})
        article_work-safety-law-2024-enterprise.tags.add(tag)

        # 集群: 等保2.0合规实施指南
        cat_djb-2-0-guide, _ = KnowledgeCategory.objects.get_or_create(
            slug="djb-2-0-guide",
            defaults={
                "name_zh": "等保2.0合规实施指南",
                "name_en": "Classiﬁed Protection 2.0 Compliance Implementation Guide",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "等保2.0三级要求解读与实施路径",
                "order": 1,
            }
        )

        # 文章: 等保2.0三级测评要点与企业应对策略
        article_djb-2-0-level3-assessment, _ = KnowledgeArticle.objects.get_or_create(
            slug="djb-2-0-level3-assessment",
            defaults={
                "title_zh": "等保2.0三级测评要点与企业应对策略",
                "title_en": "Classiﬁed Protection 2.0 Level 3 Assessment Key Points",
                "category": cat_djb-2-0-guide,
                "summary_zh": "1. 等保2.0三级标准框架",
                "content_zh": "# 等保2.0三级测评要点与企业应对策略\n\n1. 等保2.0三级标准框架\n2. 安全物理环境要求\n3. 安全通信网络\n4. 安全区域边界\n5. 安全计算环境\n6. 安全管理中心\n7. 测评流程与准备\n8. 常见扣分项分析",
                "ai_keywords": "等保2.0三级,等级保护测评,网络安全等级保护",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="等保2.0三级", defaults={"name_zh": "等保2.0三级"})
        article_djb-2-0-level3-assessment.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="等级保护测评", defaults={"name_zh": "等级保护测评"})
        article_djb-2-0-level3-assessment.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="网络安全等级保护", defaults={"name_zh": "网络安全等级保护"})
        article_djb-2-0-level3-assessment.tags.add(tag)


        # ═══════════════════════════════════════
        # 支柱: 工艺安全管理（PSM）完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="process-safety-guide",
            defaults={
                "name_zh": "工艺安全管理（PSM）完全指南",
                "name_en": "Complete Guide to Process Safety Management (PSM)",
                "tier": "domain",
                "description_zh": "化工及高危行业工艺安全管理的14要素实施指南",
                "order": 0,
            }
        )

        # 集群: 工艺危害分析（PHA）方法
        cat_pha-methodology, _ = KnowledgeCategory.objects.get_or_create(
            slug="pha-methodology",
            defaults={
                "name_zh": "工艺危害分析（PHA）方法",
                "name_en": "Process Hazard Analysis (PHA) Methods",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "HAZOP、LOPA、FMEA等PHA方法详解",
                "order": 1,
            }
        )

        # 文章: HAZOP分析方法详解：引导词、偏差与保护层
        article_hazop-analysis-guide, _ = KnowledgeArticle.objects.get_or_create(
            slug="hazop-analysis-guide",
            defaults={
                "title_zh": "HAZOP分析方法详解：引导词、偏差与保护层",
                "title_en": "HAZOP Analysis: Guide Words, Deviations, and Protection Layers",
                "category": cat_pha-methodology,
                "summary_zh": "1. HAZOP基本原理",
                "content_zh": "# HAZOP分析方法详解：引导词、偏差与保护层\n\n1. HAZOP基本原理\n2. 引导词与参数矩阵\n3. 偏差识别方法\n4. 原因-后果-保护层分析\n5. HAZOP会议组织\n6. HAZOP报告模板\n7. HAZOP vs 其他PHA方法",
                "ai_keywords": "HAZOP,工艺危害分析,偏差分析",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="hazop", defaults={"name_zh": "HAZOP"})
        article_hazop-analysis-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="工艺危害分析", defaults={"name_zh": "工艺危害分析"})
        article_hazop-analysis-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="偏差分析", defaults={"name_zh": "偏差分析"})
        article_hazop-analysis-guide.tags.add(tag)

        # 文章: LOPA保护层分析：从场景到可接受风险的量化方法
        article_lopa-analysis-guide, _ = KnowledgeArticle.objects.get_or_create(
            slug="lopa-analysis-guide",
            defaults={
                "title_zh": "LOPA保护层分析：从场景到可接受风险的量化方法",
                "title_en": "LOPA: Quantitative Method from Scenario to Acceptable Risk",
                "category": cat_pha-methodology,
                "summary_zh": "1. LOPA基本概念",
                "content_zh": "# LOPA保护层分析：从场景到可接受风险的量化方法\n\n1. LOPA基本概念\n2. 独立保护层（IPL）识别\n3. IPL可信度评估\n4. 风险频率计算\n5. 可接受风险标准\n6. LOPA vs 定性 vs QRA\n7. LOPA案例实战",
                "ai_keywords": "LOPA,保护层分析,独立保护层,IPL",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="lopa", defaults={"name_zh": "LOPA"})
        article_lopa-analysis-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="保护层分析", defaults={"name_zh": "保护层分析"})
        article_lopa-analysis-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="独立保护层", defaults={"name_zh": "独立保护层"})
        article_lopa-analysis-guide.tags.add(tag)

        # 集群: 变更管理（MOC）程序设计
        cat_management-of-change, _ = KnowledgeCategory.objects.get_or_create(
            slug="management-of-change",
            defaults={
                "name_zh": "变更管理（MOC）程序设计",
                "name_en": "Management of Change (MOC) Procedure Design",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "工艺变更、设备变更的安全管理流程",
                "order": 1,
            }
        )

        # 文章: 变更管理（MOC）全流程：从申请到关闭的闭环控制
        article_moc-full-process, _ = KnowledgeArticle.objects.get_or_create(
            slug="moc-full-process",
            defaults={
                "title_zh": "变更管理（MOC）全流程：从申请到关闭的闭环控制",
                "title_en": "Management of Change (MOC): Full Process from Request to Closure",
                "category": cat_management-of-change,
                "summary_zh": "1. 变更定义与分类（重大/一般/紧急）",
                "content_zh": "# 变更管理（MOC）全流程：从申请到关闭的闭环控制\n\n1. 变更定义与分类（重大/一般/紧急）\n2. 变更申请与审批流程\n3. PHA风险评估\n4. 变更实施管理\n5. 投用前安全检查（PSSR）\n6. 变更关闭与文档更新\n7. MOC常见失败原因",
                "ai_keywords": "变更管理,MOC流程,PSSR",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="变更管理", defaults={"name_zh": "变更管理"})
        article_moc-full-process.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="moc流程", defaults={"name_zh": "MOC流程"})
        article_moc-full-process.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="pssr", defaults={"name_zh": "PSSR"})
        article_moc-full-process.tags.add(tag)


        # ═══════════════════════════════════════
        # 支柱: 安全文化建设与行为安全完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="safety-culture-guide",
            defaults={
                "name_zh": "安全文化建设与行为安全完全指南",
                "name_en": "Complete Guide to Safety Culture and Behavioral Safety",
                "tier": "domain",
                "description_zh": "企业安全文化评估、建设和持续改进方法论",
                "order": 0,
            }
        )

        # 集群: 安全文化评估工具与方法
        cat_safety-culture-assessment, _ = KnowledgeCategory.objects.get_or_create(
            slug="safety-culture-assessment",
            defaults={
                "name_zh": "安全文化评估工具与方法",
                "name_en": "Safety Culture Assessment Tools and Methods",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "安全文化成熟度评估与测量",
                "order": 2,
            }
        )

        # 文章: Bradley安全文化成熟度模型：从病态到 generative 的五级演进
        article_bradley-safety-culture-model, _ = KnowledgeArticle.objects.get_or_create(
            slug="bradley-safety-culture-model",
            defaults={
                "title_zh": "Bradley安全文化成熟度模型：从病态到 generative 的五级演进",
                "title_en": "Bradley Safety Culture Maturity Model: Five Levels from Pathological to Generative",
                "category": cat_safety-culture-assessment,
                "summary_zh": "1. 病态型（Pathological）",
                "content_zh": "# Bradley安全文化成熟度模型：从病态到 generative 的五级演进\n\n1. 病态型（Pathological）\n2. 反应型（Reactive）\n3. 计算型（Calculative）\n4. 主动型（Proactive）\n5. 生成型（Generative）\n6. 评估工具设计\n7. 评估结果解读与行动建议",
                "ai_keywords": "安全文化模型,安全成熟度,Bradley模型",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全文化模型", defaults={"name_zh": "安全文化模型"})
        article_bradley-safety-culture-model.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全成熟度", defaults={"name_zh": "安全成熟度"})
        article_bradley-safety-culture-model.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="bradley模型", defaults={"name_zh": "Bradley模型"})
        article_bradley-safety-culture-model.tags.add(tag)

        # 集群: 行为安全观察（BBS）实施指南
        cat_behavioral-safety, _ = KnowledgeCategory.objects.get_or_create(
            slug="behavioral-safety",
            defaults={
                "name_zh": "行为安全观察（BBS）实施指南",
                "name_en": "Behavior-Based Safety (BBS) Implementation Guide",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "基于行为的安全管理方法实施",
                "order": 2,
            }
        )

        # 文章: 行为安全观察（BBS）从设计到落地的完整方案
        article_bbs-implementation-guide, _ = KnowledgeArticle.objects.get_or_create(
            slug="bbs-implementation-guide",
            defaults={
                "title_zh": "行为安全观察（BBS）从设计到落地的完整方案",
                "title_en": "Behavior-Based Safety (BBS): Design to Implementation",
                "category": cat_behavioral-safety,
                "summary_zh": "1. BBS原理与核心要素",
                "content_zh": "# 行为安全观察（BBS）从设计到落地的完整方案\n\n1. BBS原理与核心要素\n2. 关键行为识别方法\n3. 观察清单设计\n4. 观察员培训\n5. 数据收集与分析\n6. 正向反馈与强化\n7. BBS项目常见失败原因与对策",
                "ai_keywords": "行为安全,BBS,安全观察",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="行为安全", defaults={"name_zh": "行为安全"})
        article_bbs-implementation-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="bbs", defaults={"name_zh": "BBS"})
        article_bbs-implementation-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全观察", defaults={"name_zh": "安全观察"})
        article_bbs-implementation-guide.tags.add(tag)


        # ═══════════════════════════════════════
        # 支柱: 安全培训教育体系建设完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="safety-training-guide",
            defaults={
                "name_zh": "安全培训教育体系建设完全指南",
                "name_en": "Complete Guide to Safety Training System Development",
                "tier": "domain",
                "description_zh": "企业安全培训需求分析、课程设计、效果评估和数字化培训平台建设",
                "order": 0,
            }
        )

        # 集群: 三级安全教育实施规范
        cat_three-level-safety-education, _ = KnowledgeCategory.objects.get_or_create(
            slug="three-level-safety-education",
            defaults={
                "name_zh": "三级安全教育实施规范",
                "name_en": "Three-Level Safety Education Implementation Standards",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "厂级、车间级、班组级三级安全教育",
                "order": 1,
            }
        )

        # 文章: 三级安全教育内容大纲与课时标准（最新版）
        article_three-level-education-syllabus, _ = KnowledgeArticle.objects.get_or_create(
            slug="three-level-education-syllabus",
            defaults={
                "title_zh": "三级安全教育内容大纲与课时标准（最新版）",
                "title_en": "Three-Level Safety Education Syllabus and Hour Standards (Latest Edition)",
                "category": cat_three-level-safety-education,
                "summary_zh": "1. 厂级安全教育内容（法规/风险/权利义务）",
                "content_zh": "# 三级安全教育内容大纲与课时标准（最新版）\n\n1. 厂级安全教育内容（法规/风险/权利义务）\n2. 车间级安全教育内容（现场风险/防护/应急）\n3. 班组级安全教育内容（岗位风险/操作规程/PPE）\n4. 各级课时要求\n5. 考核标准\n6. 特种作业人员附加要求",
                "ai_keywords": "三级安全教育,入厂安全教育,安全培训大纲",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="三级安全教育", defaults={"name_zh": "三级安全教育"})
        article_three-level-education-syllabus.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="入厂安全教育", defaults={"name_zh": "入厂安全教育"})
        article_three-level-education-syllabus.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全培训大纲", defaults={"name_zh": "安全培训大纲"})
        article_three-level-education-syllabus.tags.add(tag)

        # 集群: 安全培训效果评估与改进
        cat_safety-training-effectiveness, _ = KnowledgeCategory.objects.get_or_create(
            slug="safety-training-effectiveness",
            defaults={
                "name_zh": "安全培训效果评估与改进",
                "name_en": "Safety Training Effectiveness Evaluation and Improvement",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "Kirkpatrick四层评估模型在安全培训中的应用",
                "order": 2,
            }
        )

        # 文章: Kirkpatrick四层模型评估安全培训效果的方法论
        article_kirkpatrick-safety-training-evaluation, _ = KnowledgeArticle.objects.get_or_create(
            slug="kirkpatrick-safety-training-evaluation",
            defaults={
                "title_zh": "Kirkpatrick四层模型评估安全培训效果的方法论",
                "title_en": "Evaluating Safety Training with Kirkpatrick Four-Level Model",
                "category": cat_safety-training-effectiveness,
                "summary_zh": "1. 第一层：反应层（满意度）",
                "content_zh": "# Kirkpatrick四层模型评估安全培训效果的方法论\n\n1. 第一层：反应层（满意度）\n2. 第二层：学习层（知识掌握）\n3. 第三层：行为层（行为改变）\n4. 第四层：结果层（安全绩效）\n5. 各层评估工具设计\n6. 培训效果数据的收集与分析",
                "ai_keywords": "培训效果评估,Kirkpatrick,安全培训评估",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="培训效果评估", defaults={"name_zh": "培训效果评估"})
        article_kirkpatrick-safety-training-evaluation.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="kirkpatrick", defaults={"name_zh": "Kirkpatrick"})
        article_kirkpatrick-safety-training-evaluation.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="安全培训评估", defaults={"name_zh": "安全培训评估"})
        article_kirkpatrick-safety-training-evaluation.tags.add(tag)


        # ═══════════════════════════════════════
        # 支柱: 网络安全与数据保护完全指南
        # ═══════════════════════════════════════

        pillar_cat, _ = KnowledgeCategory.objects.get_or_create(
            slug="cybersecurity-guide",
            defaults={
                "name_zh": "网络安全与数据保护完全指南",
                "name_en": "Complete Guide to Cybersecurity and Data Protection",
                "tier": "domain",
                "description_zh": "企业网络安全体系规划、威胁防护、数据安全治理和个人信息保护合规",
                "order": 0,
            }
        )

        # 集群: 数据分类分级与安全治理
        cat_data-classification, _ = KnowledgeCategory.objects.get_or_create(
            slug="data-classification",
            defaults={
                "name_zh": "数据分类分级与安全治理",
                "name_en": "Data Classiﬁcation and Security Governance",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "企业数据资产分类分级方法与安全治理",
                "order": 1,
            }
        )

        # 文章: 企业数据分类分级实施指南：从资产盘点到标签落地
        article_data-classification-implementation, _ = KnowledgeArticle.objects.get_or_create(
            slug="data-classification-implementation",
            defaults={
                "title_zh": "企业数据分类分级实施指南：从资产盘点到标签落地",
                "title_en": "Enterprise Data Classification: From Asset Inventory to Labeling",
                "category": cat_data-classification,
                "summary_zh": "1. 数据资产盘点方法",
                "content_zh": "# 企业数据分类分级实施指南：从资产盘点到标签落地\n\n1. 数据资产盘点方法\n2. 数据分类标准设计\n3. 数据分级标准（公开/内部/机密/绝密）\n4. 自动化标签技术\n5. 数据生命周期管理\n6. 数据安全治理组织架构",
                "ai_keywords": "数据分类分级,数据安全治理,数据资产",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="数据分类分级", defaults={"name_zh": "数据分类分级"})
        article_data-classification-implementation.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="数据安全治理", defaults={"name_zh": "数据安全治理"})
        article_data-classification-implementation.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="数据资产", defaults={"name_zh": "数据资产"})
        article_data-classification-implementation.tags.add(tag)

        # 集群: 个人信息保护合规（PIPL）
        cat_personal-information-protection, _ = KnowledgeCategory.objects.get_or_create(
            slug="personal-information-protection",
            defaults={
                "name_zh": "个人信息保护合规（PIPL）",
                "name_en": "Personal Information Protection Compliance (PIPL)",
                "tier": "category",
                "parent": pillar_cat,
                "description_zh": "个人信息保护法合规实施",
                "order": 1,
            }
        )

        # 文章: 《个人信息保护法》企业合规实施全攻略
        article_pipl-compliance-guide, _ = KnowledgeArticle.objects.get_or_create(
            slug="pipl-compliance-guide",
            defaults={
                "title_zh": "《个人信息保护法》企业合规实施全攻略",
                "title_en": "PIPL Enterprise Compliance: Complete Implementation Guide",
                "category": cat_personal-information-protection,
                "summary_zh": "1. PIPL核心义务梳理",
                "content_zh": "# 《个人信息保护法》企业合规实施全攻略\n\n1. PIPL核心义务梳理\n2. 个人信息处理合法性基础\n3. 知情同意机制设计\n4. 数据处理者义务\n5. 跨境数据传输合规\n6. 隐私政策撰写规范\n7. 合规自查清单",
                "ai_keywords": "个人信息保护法,PIPL,数据合规,隐私保护",
                "author": admin,
                "status": "draft",
                "access_level": "free",
            }
        )
        tag, _ = KnowledgeTag.objects.get_or_create(slug="个人信息保护法", defaults={"name_zh": "个人信息保护法"})
        article_pipl-compliance-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="pipl", defaults={"name_zh": "PIPL"})
        article_pipl-compliance-guide.tags.add(tag)
        tag, _ = KnowledgeTag.objects.get_or_create(slug="数据合规", defaults={"name_zh": "数据合规"})
        article_pipl-compliance-guide.tags.add(tag)


        self.stdout.write(self.style.SUCCESS("主题集群种子数据导入完成"))