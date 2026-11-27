# Slice and send

Read this at steps 10 and 11. Slicing turns a checked 3MF into a job file a printer runs. Sending puts that job on a printer. The agent may slice. The user starts every print.

Evidence. The command flags come from each slicer's own documentation, read on 2026-11-27: DOCUMENTED. No slicer ran in a GDH session yet. Run `--help` on the installed version before the first job, because flags change between releases.

## 1. Which slicer

| Printer | First choice | Second choice | Job file |
| --- | --- | --- | --- |
| Bambu Lab P2S | Bambu Studio 2.3.0 or later | OrcaSlicer | `.gcode.3mf` |
| Flashforge Adventurer 5M, 5M Pro | OrcaSlicer, or the maker's Orca-Flashforge fork | FlashPrint 5 (no command line found) | `.gcode` |

Cards: [bambu-studio](../../../references/tools/bambu-studio.md), [orca-slicer](../../../references/tools/orca-slicer.md). Both are AGPL-3.0 desktop programs. Install nothing without the user's yes.

Find what is installed:

```
command -v bambu-studio orca-slicer orcaslicer OrcaSlicer
```

On macOS the binary sits inside the app bundle, for example `/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer`. A cloud session usually has neither; then hand the checked 3MF to the user to slice.

## 2. Settings come from profiles

A slicer needs three settings files: the machine, the process (layer height, walls, infill) and the filament. Take them from the slicer's own bundled profiles for the user's printer and nozzle, or from files the user exports from the slicer's interface. Never invent temperatures or speeds.

Keep the three files the user approves under `design/print/profiles/`, and name them in the print profile.

## 3. Commands

Bambu Studio, all plates, sliced 3MF out:

```
bambu-studio --orient --arrange 1 \
  --load-settings "design/print/profiles/machine.json;design/print/profiles/process.json" \
  --load-filaments "design/print/profiles/filament.json" \
  --slice 0 --export-3mf design/print/<part>/<part>.gcode.3mf \
  design/print/<part>/<part>.3mf
```

OrcaSlicer, the same job, with statistics:

```
orca-slicer --arrange 1 \
  --load-settings "design/print/profiles/process.json;design/print/profiles/machine.json" \
  --load-filaments "design/print/profiles/filament.json" \
  --slice 0 --export-3mf design/print/<part>/<part>.gcode.3mf \
  --outputdir design/print/<part>/ \
  design/print/<part>/<part>.3mf
```

For the Adventurer 5M, export G-code for the plate rather than a sliced 3MF. Read the installed version's help for the G-code export flag.

Rules:

- `--slice 0` slices every plate. A number slices one plate.
- Give every path inside the project. Never write into the slicer's own folders.
- Read the statistics or the slicer's log for print time, filament length and weight. Report them.
- Open the sliced preview, or a capture of it, before you call the job ready. Look at the first layer, supports and thin walls.

## 4. The send gate

Sending a job is a physical action. A printer heats to 300 degrees, moves at speed and can run for many hours unattended.

GATE: the agent never starts a print. The user starts it from the slicer, the printer's screen or the maker's app.

GATE: the agent sends a job to a printer only when the user asks for that one job, names the printer, and confirms the plate is clear and loaded. Each job needs its own yes.

Routes, from safest:

1. The user opens the sliced file in the slicer and prints. Default.
2. The user copies the job to a USB drive or SD card.
3. A tool opens the file in the user's slicer, such as a generation service's send-to-slicer command. It opens; it does not print.
4. The maker's third-party route: Bambu Connect takes a file handed over by another program, and the user confirms on screen.
5. Local network control: Bambu Developer Mode in LAN-only mode, or the community-documented Flashforge local API. The maker does not support Bambu Developer Mode, and the user takes on its network security. Use these only when the user has set them up and asks.

Never store a printer access code, a serial number or a cloud token in a tracked file or in chat. Those are the user's secrets.

## 5. Failure patterns

| Pattern | What goes wrong | Do this |
| --- | --- | --- |
| Invented settings | Made-up temperatures warp or clog the print | Use the slicer's bundled profile for the printer and filament |
| Wrong printer file | A Bambu job sent to the Flashforge, or the reverse | Slice per printer; name the printer in the file name |
| Unseen preview | The job slices but the first layer or a support fails | Look at the sliced preview before you hand it over |
| Silent send | The agent starts a print because the command exists | Follow the send gate; the user starts it |
| Version drift | A flag changed in a new slicer release | Run `--help` on the installed version first |
