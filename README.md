# US Allocation: OneGMS Reporting Explorer

A single-page site for information managers in the field to take a quick look
at indicator reporting for CBPF US Award (NSFT) projects. Pick a country, see
every project with its partner, budget, status and beneficiary figures, expand a
project to see each indicator's target and reach, or switch to the aggregated
view to see every indicator summed across the country's projects.

There is no backend and no build step. The page reads the public OneGMS API
directly from the browser, so figures are always what OneGMS publishes at the
moment the page loads. It is meant to be hosted on GitHub Pages.

## Files

| File | Purpose |
|---|---|
| `index.html` | The whole app: markup, styles and script in one file |
| `serve.py` | No-cache local preview server (`python3 serve.py`, then open http://127.0.0.1:8770/) |
| `.nojekyll` | Tells GitHub Pages to serve the files as they are |

## Data sources

All public, no credentials. Every endpoint returns `Access-Control-Allow-Origin: *`,
which is what makes the browser-only design possible.

| What | Endpoint | Notes |
|---|---|---|
| Indicator targets and achievements per project | `GlobalGenericDataExtract?SPCode=PF_GLB_INDIC&PoolfundCodeAbbrv=<fund>&AllocationYears=2026&...` | One row per project per global indicator; ids only, no names |
| Partner, title, status, budget, dates, targeted people | `ProjectSummaryV2?$filter=PFId eq <pfid> and substringof('NSFT',PrjCode)` | One row per approved project |
| Reached people and partner risk per project | `GlobalGenericDataExtract?SPCode=PF_PROJ_DETAIL&PoolfundCodeAbbrv=<fund>&AllocationYears=2026&FundTypeId=1` | Also carries titles, used as a fallback |
| Indicator names, codes, units, core flag | `GlobalGenericDataExtract?SPCode=GLB_INDIC_MST&GlobalIndicatorType=1` and `=2` | Fetched once per page load; type 1 is output, type 2 outcome |
| Sector names | `MstClusters` | Maps `GlbClstrId` to a global cluster name |
| Data freshness | `LastModified` | Shown in the footer |

Base URL: `https://cbpfapi.unocha.org/vo3/odata/`. The `cbpfapib` host serves
the same indicator extract scoped to US Award projects but also includes
projects still under approval, so this site uses `cbpfapi` and filters on the
`NSFT` token in the project code plus the fund's `PooledFundId` (Bangladesh
shares the `AP501` regional envelope with four other funds).

## Overview charts

Above the tables, an Overview section follows the current filters:

- **Progress by sector**: one bar per sector. Bar length is the sector's people
  targeted relative to the largest sector; the fill is the share reached. Only
  person-count indicators (units Individuals, People, Persons) are added up.
- **Core indicators**: one tile per US Award core indicator present in the
  country, with reached against targeted and how many projects are reporting.

## How figures are combined

- **By project**: each project's own targeted and reached people come from the
  project record. Indicator rows are shown as OneGMS publishes them.
- **By indicator**: rows are grouped by indicator and sector and summed across
  projects. Percentage indicators are averaged instead of summed. Reached
  totals only include projects that have reported. This is the same rule the
  AIT reporting pipeline uses.
- Indicator sums are not deduplicated beneficiary counts: a person counted under
  two indicators, or by two projects, is counted twice.
- A blank reached figure means the partner has not yet reported, not zero.
- Some funds (Sudan, Myanmar) do not publish partner names; the page says so and
  shows the organisation type instead.

## Adding or changing a country

Edit the `FUNDS` array at the top of the script in `index.html`. Each entry
needs the fund's `PooledFundId` (`pfid`) and `PoolfundCodeAbbrv` (`code`). Both
can be read from `https://cbpfapi.unocha.org/vo3/odata/Poolfund?$format=json`.

## Deploying

Push to GitHub, then in the repository settings enable Pages from the branch
root. Nothing else is required. The page also works from any static host.
