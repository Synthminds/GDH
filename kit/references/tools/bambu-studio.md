# Bambu Studio

Catalog entry: [bambu-studio.json](../../catalogs/tools/bambu-studio.json). Source: https://github.com/bambulab/BambuStudio/wiki/Command-Line-Usage

Terms in this card. A sliced 3MF is a 3MF package that holds the G-code for each plate beside the model. AMS is Bambu Lab's material system that feeds several filaments to one printer.

## What it makes

- A sliced 3MF (`.gcode.3mf`) for Bambu printers, the P2S included from version 2.3.0.
- Multi-color jobs that map bodies to material system slots.
- Automatic orientation and arrangement.
- It does not repair or model geometry.

## Connection and auth

- A desktop program on the user's machine. Slicing from the command line needs no account.
- The interface can send jobs to a printer through the maker's cloud or the LAN. That path needs the user's account or the printer's access code. The agent does not use it.
- Third-party programs reach Bambu printers through Bambu Connect, where the user confirms each job. Developer Mode in LAN-only mode opens the printer's local channels; the maker does not support it.
- Install nothing without the user's yes.

## Cost model

Free and open source (AGPL-3.0, based on PrusaSlicer). The command-line slice makes no network call. Cloud sending is outside GDH.

## Call order

1. Confirm the binary and its version with `--help`.
2. Load the P2S machine profile for the nozzle, a process profile and the filament profiles.
3. Slice all plates to a sliced 3MF inside the project.
4. Open or capture the preview. Check the first layer and supports.
5. Hand the file to the user. The user prints from Bambu Studio, Bambu Handy or the printer.

## Key tools

```
bambu-studio --orient --arrange 1 \
  --load-settings "machine.json;process.json" \
  --load-filaments "filament.json" \
  --slice 0 --export-3mf out.gcode.3mf \
  design/print/<part>/<part>.3mf
```

`--slice 0` slices all plates. `--outputdir` sets the folder. Full steps: `print-design` reference `slice-and-send.md`.

## Inputs

- A checked 3MF in millimetres. A 3MF keeps color bodies; STL does not.
- Machine, process and filament settings for the P2S and nozzle.

## Outputs and how to bring them into a project

- `design/print/<part>/<part>.gcode.3mf`. The G-code for each plate sits inside it.
- Keep the settings files under `design/print/profiles/`.

## Handoffs

- From `print-design` after the mesh check.
- To the user, who opens the job and starts the print.
- A generation service's send-to-slicer command can open a model in Bambu Studio for the user.

## Limits and failure modes

- Flags change between releases. Read `--help` first.
- It slices for Bambu printers. Use OrcaSlicer for the Flashforge printers.
- Mandatory authorization control for third-party printer commands arrived in 2025. Do not script printer control around it.

## Best for

- The default slicer for Bambu printers: the maker's own, with its newest printer and firmware support first.
- Multi-color jobs with the material system, and jobs the user will open in the same app.

## Wrong for

- Non-Bambu printers.
- Unattended sending. The send gate holds.

## Evidence

DOCUMENTED. On 2026-11-27 the command-line wiki page, the 2.3.0 release notes that add the P2S, and the repository README were read. The latest release seen was 2.09.02.62. No slice ran in a GDH session.
