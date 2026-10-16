# Project Technical Documentation

This directory serves as the technical documentation repository for the Sales Performance and Revenue Growth Dashboard. It provides comprehensive specifications, architectural designs, data pipelines, module breakdowns, analytical models, validation routines, and interview preparation materials.

---

## Master Interview and Technical Reference

* **[Technical Interview Handbook](interview_handbook.md):** The primary reference for technical and managerial interview preparation. Provides detailed answers to questions regarding architecture, data flows, modules, dataset hygiene, Star Schema modeling, DAX engine design, Holt-Winters model scoring, test frameworks, business insights, and engineering trade-offs.

---

## Documentation Index

### Core Technical Architecture and Data Engineering
| Document | Focus and Content | File Link |
| :--- | :--- | :--- |
| **Technical Interview Handbook** | Comprehensive interview questions, architectural answers, and performance scores | [interview_handbook.md](interview_handbook.md) |
| **System Architecture** | Decoupled 4-tier architectural blueprint, layer responsibilities, and technology stack | [architecture.md](architecture.md) |
| **Data Flow and Pipeline** | Sequence diagram, 5-stage transformation pipeline, and data movement | [data_flow.md](data_flow.md) |
| **System Modules Breakdown** | Script-by-script inventory, inputs, outputs, and operational responsibilities | [modules.md](modules.md) |
| **Dataset Specification** | Data dictionary, provenance, column schemas, types, and constraints | [dataset.md](dataset.md) |
| **Data Quality Report** | Cleansing logic, macro financial reconciliation ($0.00 delta), and integrity audits | [data_quality_report.md](data_quality_report.md) |

### Dimensional Modeling, DAX, and Visual Design
| Document | Focus and Content | File Link |
| :--- | :--- | :--- |
| **Data Model Specification** | Normalized Star Schema diagram, grain definitions, surrogate keys, and M code | [data_model_specification.md](data_model_specification.md) |
| **DAX Measures Library** | Complete formulas for 11 explicit DAX measures, time intelligence, and edge-case handling | [dax_measures_library.md](dax_measures_library.md) |
| **Dashboard Layout Spec** | Canvas grid structure, visual field wells, sort orders, and corporate theme tokens | [dashboard_layout_specification.md](dashboard_layout_specification.md) |

### Predictive Modeling and Testing Framework
| Document | Focus and Content | File Link |
| :--- | :--- | :--- |
| **Forecasting and Growth Analysis** | Holt-Winters Damped ETS algorithm, holdout scores (MAPE 30.16%), and H1 2026 forecast | [forecasting_and_growth_analysis.md](forecasting_and_growth_analysis.md) |
| **Model Learning and Evaluation** | Mathematical formulation of Holt-Winters equations, damping factor, and backtesting | [model_learning.md](model_learning.md) |
| **Validation Framework** | 5 automated test scripts, mathematical parity checks, and assertion gates | [validation_framework.md](validation_framework.md) |
| **Execution Log** | Step-by-step development audit trail and verification milestones | [execution_log.md](execution_log.md) |

### Business Case and Enterprise Strategy
| Document | Focus and Content | File Link |
| :--- | :--- | :--- |
| **Business Case Proposal** | Executive problem statement, core capabilities, user personas, and investment criteria | [../documentation/business_case/business_case.md](../documentation/business_case/business_case.md) |
| **Claim Validation Register** | Empirical verification of market size, platform market share, and productivity claims | [../documentation/business_case/claim_validation_register.md](../documentation/business_case/claim_validation_register.md) |
| **Financial ROI Framework** | Capital payback formulas, sensitivity analysis matrix, and valuation worksheet | [../documentation/business_case/roi_framework.md](../documentation/business_case/roi_framework.md) |
| **Technical Architecture** | Enterprise data pipeline, refresh schedule, and security architecture | [../documentation/business_case/technical_architecture.md](../documentation/business_case/technical_architecture.md) |
| **Publishing Guide** | Power BI Service deployment, workspace roles, and gateway configuration | [../documentation/publishing_guide.md](../documentation/publishing_guide.md) |
| **GitHub Deployment Guide** | Version control standards, .gitignore policies, and staging protocol | [../documentation/github_deployment_guide.md](../documentation/github_deployment_guide.md) |

---

## Documentation Standards
1. **Mathematical Precision:** Every formula, metric, and percentage has been reconciled to source data.
2. **Independent Reproducibility:** Every script can be executed independently from the command line using Anaconda Python.
3. **Auditability:** Every metric cited in documentation matches an automated test assertion.
