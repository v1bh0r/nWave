---
description: "Designs CI/CD pipelines, infrastructure, observability, and deployment strategy. Use when preparing platform readiness for a feature."
---

# NW-DEVOPS: Platform Readiness and Infrastructure Design

**Wave**: DEVOPS (wave 4 of 6)

Invoke `#agent:nw-platform-architect` to execute the DEVOPS wave.

## Usage

```
/nw-devops [deployment-target]
```

## Prior Wave Consultation

Before beginning DEVOPS work, read:

1. **DESIGN** artifacts from `docs/feature/{feature-id}/design/`:
   - `architecture-design.md` — components to operationalize
   - `component-boundaries.md` — deployment units
   - `technology-stack.md` — infrastructure requirements

2. **DISCUSS** artifacts: `docs/feature/{feature-id}/discuss/outcome-kpis.md` — KPIs become SLOs.

## Interactive Decisions

The agent will ask:
1. **Deployment target**: Cloud-native (AWS/GCP/Azure) / On-premise / Hybrid / Edge
2. **Container orchestration**: Kubernetes / Docker Compose / Serverless / None
3. **CI/CD platform**: GitHub Actions / GitLab CI / Jenkins / Azure DevOps / Other
4. **Existing infrastructure**: Describe what exists; Apex integrates rather than replaces

## What the Agent Produces

- `docs/feature/{feature-id}/devops/ci-cd-pipeline.md` — pipeline design with stages
- `docs/feature/{feature-id}/devops/infrastructure-design.md` — IaC approach (Terraform/Pulumi/etc.)
- `docs/feature/{feature-id}/devops/observability-design.md` — metrics, logging, alerting, SLOs
- `docs/feature/{feature-id}/devops/deployment-strategy.md` — blue/green, canary, rollback plan
- `docs/feature/{feature-id}/devops/wave-decisions.md` — summary for downstream waves

## Non-Negotiable Requirements

- Rollback plan is defined before deployment is designed
- SLOs defined before alert thresholds
- DORA metrics tracked: deployment frequency, lead time, MTTR, change failure rate

After completion, invoke `#agent:nw-platform-architect-reviewer` for peer review.

## Next Wave

After DEVOPS: `/nw-distill` to create acceptance tests that include infrastructure concerns.
