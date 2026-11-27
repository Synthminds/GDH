# OrcaSlicer

Catalog entry: [orca-slicer.json](../../catalogs/tools/orca-slicer.json). Source: https://www.orcaslicer.com/wiki/cli/cli_mode

Terms in this card. Slicing turns a 3D model into the moves a printer runs. A profile is a saved settings file: machine, process or filament. A plate is one print bed's worth of parts.

## What it makes

- A sliced 3MF (`.gcode.3mf`) or G-code for one or all plates, from a 3MF or STL.
- Print statistics: time, filament length and weight, from version 2.5.0.
- Automatic orientation and arrangement on the plate.
- It does not model or repair geometry. `print-design` checks the mesh first.

## Connection and auth

- A desktop program on the user's machine. No account for slicing.
- Bundled profiles cover the Bambu Lab P2S at 0.2 to 0.8 mm nozzles and the Flashforge Adventurer 5M and 5M Pro at 0.25 to 0.8 mm.
- The Flashforge fork Orca-Flashforge adds the maker's cloud and LAN sending. Its command line is not documented; treat it as the same as OrcaSlicer only after `--help` confirms it.
- Install nothing without the user's yes.

## Cost model

Free and open source (AGPL-3.0). Slicing makes no network call.

## Call order

1. Confirm the binary and its version with `--help`.
2. Choose the machine, process and filament profiles for the printer and nozzle. Use bundled profiles or files the user exported. Never invent temperatures or speeds.
3. Slice to a path inside the project.
4. Read the statistics. Open or capture the preview.
5. Hand the job file to the user. The user starts the print.

## Key tools

```
orca-slicer --arrange 1 \
  --load-settings "process.json;machine.json" \
  --load-filaments "filament.json" \
  --slice 0 --export-3mf out.gcode.3mf \
  --outputdir design/print/<part>/ \
  design/print/<part>/<part>.3mf
```

`--slice 0` slices all plates. `--export-statistics` writes the time and material figures. `--min-save` writes a smaller 3MF. Full steps: `print-design` reference `slice-and-send.md`.

## Inputs

- A checked 3MF or STL in millimetres.
- Three settings files for the printer, the process and the filament.

## Outputs and how to bring them into a project

- `design/print/<part>/<part>.gcode.3mf`, or G-code for the Flashforge printers.
- The statistics file beside it. Keep the three settings files under `design/print/profiles/`.

## Handoffs

- From `print-design` after the mesh check passes.
- To the user, who opens the job in the slicer, copies it to a drive, or prints from the app.

## Limits and failure modes

- Flags change between releases. Read `--help` first.
- A desktop session may lack a display. The command line runs without one on Linux; confirm on the user's machine.
- A cloud session usually lacks the program. Hand the checked 3MF to the user instead.

## Best for

- One slicer for both a Bambu and a Flashforge printer.
- Repeatable job files from the command line.

## Wrong for

- Sending a job unattended. The send gate in `print-design` holds.
- Mesh repair or modeling.

## Evidence

DOCUMENTED. On 2026-11-27 the command-line wiki pages (mode, actions, miscellaneous) and the bundled Bambu Lab and Flashforge machine profile folders on the main branch were read. The latest release seen was 2.5.2. No slice ran in a GDH session.
