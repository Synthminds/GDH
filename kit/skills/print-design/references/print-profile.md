# Print profile template

Read this before you start. Copy the block below to `design/print-profile.md` in the project and fill it from `printers.json` and the user's answers. Keep the owner's own printers, materials and settings in the project or in a private brand vault, never in this public kit.

```
# Print profile

Status: draft | confirmed YYYY-MM-DD by <who>

## Printers

| Id | Model | Nozzle mm | Material system | Slicer | Reaches the printer by |
| --- | --- | --- | --- | --- | --- |
| <id from printers.json> | <model> | 0.4 | <none | system and slots> | <slicer> | <SD card | USB | LAN | cloud> |

## Materials on hand

| Material | Brand and color | Printers | Notes |
| --- | --- | --- | --- |
| PLA | <brand, color> | <ids> | <dry box, hardened nozzle, and so on> |

## Measured fits

Record coupon results here. A measured number replaces the default in design-for-print.md.

| Fit | Printer, nozzle, material | Clearance that worked mm | Date |
| --- | --- | --- | --- |
| Press fit on a 10 mm pin | <id, 0.4, PLA> | <value> | <date> |

## Rules

- Who starts prints: the user. The agent prepares job files only.
- Default printer for new parts: <id>.
```

Rules for the agent:

- A measured fit in the profile beats every default.
- A printer not in `printers.json` needs its build volume, nozzle and enclosure from the user or the maker's page. Label it DOCUMENTED with the source.
- The profile names how a job reaches each printer. That line tells `slice-and-send.md` which gate applies.
