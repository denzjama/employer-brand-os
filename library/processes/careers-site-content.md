---
id: careers-site-content
domain: content
name: Careers site content
name_ru: Карьерный сайт
default_autonomy: L1
external_facing: true
---

## Purpose
Keeps careers site pages accurate and consistent with the brand core: finds outdated facts, broken promises, pages that contradict each other, and drafts updates that use only confirmed facts.

## Fits when
- The company has a careers site or careers section with several pages.
- Pages were written at different times by different people.

## Triggers
Quarterly review; when a fact in the brand core changes; on request.

## Inputs
Page texts (fetched from the site or placed in `eb/inbox/site/`); `eb/brand-core/*`.

## Outputs
`eb/work/careers-site-content/<date>-review.md`: issues per page with the evidence, proposed edits as before → after.

## Human checkpoint
The owner approves edits; the site team publishes.

## Suggested ritual
Quarterly site review with the web owner.

## Metrics
Outdated facts found and fixed; pages reviewed per quarter.

## Risks and limits
Before → after edits use only CONFIRMED facts. Passes the quality gate. Does not edit the live site.
