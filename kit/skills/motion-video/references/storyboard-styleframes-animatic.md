# Storyboard, styleframes and animatic

Read this file at steps 4 to 7 and 10 of `motion-video`. It covers the storyboard format, the look-kit board, styleframes as the direction step, the animatic, and the approval rounds.

Evidence. The sequence storyboard, styleframe, animatic is motion design practice recalled from process articles, not re-read in this build. The look-kit pattern (one kit artboard followed by one artboard per shot, each titled with its time range) was seen in a real owner storyboard canvas on 2026-11-23. The number of directions follows the GDH resolution of conflict 13. The stage rule follows conflict 14.

## 1. Why the cheap forms come first

| Form | Fixes | Cost to change |
| --- | --- | --- |
| Script | Message and words | Minutes |
| Storyboard | Order, shots, on-screen text | Minutes to an hour |
| Styleframes | The look: type, color, texture, composition | Hours |
| Animatic | Pacing against real sound | Hours |
| Animation | Motion detail | Days |
| Paid render | The final file | Credits and waiting |

A change found in the animatic costs an hour. The same change found after a paid render costs the render again. Approve each form before the next.

## 2. The storyboard

One frame per beat. Each frame holds:

1. Beat number and time range: `03 (0:06 to 0:11)`.
2. A sketch or a rough frame of the shot: composition, the focal point, where text sits.
3. Action: what moves and how, in one line.
4. On-screen text, exact.
5. Sound: the line of voice, the music cue, an effect.
6. Transition in and out: cut, match cut, push, mask reveal, cross-fade.

Format choices:

| Where | When |
| --- | --- |
| A Claude Design canvas through the `claude-design` skill | The user works in Claude Design, or the board will feed a send-to video route |
| A local HTML board, one fixed-size frame per beat | Default with no canvas tool |
| A Markdown table plus rough PNG frames | The quickest review |

The look-kit layout for a canvas:

1. One wide kit artboard first: palette swatches, type specimen at video sizes, logo lockups, texture and overlay samples, one example of each motion pattern named in words.
2. Then one artboard per shot, at the video's aspect ratio, in reading order. Title each with its number and time range.
3. Keep equal gaps between frames and rows. One note above the kit and one above the shots.

Rules:

1. Draw at the real aspect ratio. A 16:9 board for a 9:16 video hides every composition problem.
2. Put the platform's interface overlay on the vertical frames as a guide layer: the caption area, the side buttons, the bottom bar. Keep text and faces out of it.
3. Use real copy. Placeholder text hides length problems.
4. ASK after the board: "Keep, change or remove, for each beat?" Change only the beats named.

## 3. Styleframes: the direction step

A styleframe is a finished still of one beat. It fixes type, color, texture, composition and the treatment of footage or illustration.

1. Pick one representative beat, usually the hook or the key proof beat.
2. Make two to four styleframes of that same beat. Default: three. Two when brand rules are strict. Four at most.
3. In this explore stage, the frames differ in idea, not in color. Name the idea of each in one sentence that does not name a color.
4. Each frame uses the same copy and the same content.
5. Add one motion note per frame: how things move in this direction (snappy and graphic, slow and filmic, typographic and rhythmic).
6. Run the tell scan on choices the design system leaves open: default fonts, purple-to-blue gradients, glow on dark, the same entrance on every element.
7. ASK: show the frames side by side. Ask for keep, change and remove per part. Get one choice.
8. Record the choice and the rejected frames with reasons.

After the choice, any further comparison is a refine-stage comparison: two frames that differ in one named attribute (for example type size or grain amount).

Example directions for one hook frame:

| Direction | Idea in one sentence | Motion note |
| --- | --- | --- |
| A. Paper trail | The report is a stack of real-looking pages that sort themselves | Paper physics: slides, settles, soft shadows |
| B. Signal | Data as clean lines that converge into one number | Precise, linear draws, one hard accent |
| C. Big type | The words carry the video; product shots are small and framed | Kinetic type, hard cuts on the beat |

## 4. Making styleframes

| Route | Use when |
| --- | --- |
| Hand-built HTML frames from tokens | Default. Brand-exact, free, and the same code can become the video |
| A design canvas | The user reviews in Claude Design |
| Generated stills through `generate-media` | The direction needs imagery that does not exist. Spend gate applies. |

Rules:

1. Logos, type and colors come from the brand files and tokens. A generated frame never supplies the logo or the text.
2. A generated still is a candidate background or footage reference. Text and logo go on top in the design.
3. A styleframe built in HTML at the video's pixel size can become scene one of a code-owned video.

## 5. The animatic

The animatic is the storyboard (or styleframes) cut to the timed voice or music.

1. Lay the frames on a timeline at the beat times from the script.
2. Use the recorded guide read or a draft voice. Use the chosen music bed, or a temporary track with the same tempo.
3. Add only cuts and the rough position of each motion. No polish.
4. Watch it at full length, then muted.
5. Fix pacing here: a beat too long, a line that cannot be read, a cut that lands off the beat.
6. ASK: approve pacing before animation starts.

Ways to build it:

| Route | How |
| --- | --- |
| HTML | One page that shows each frame for its duration, with the audio element in sync. Free. |
| A local HTML video composer | The frames as scenes with hard cuts; preview locally before any render |
| A scene engine with free export | Frames as scenes, check a contact sheet, export a low-resolution file |
| A video editor the user owns | Frames and audio on a timeline |

A minimal HTML animatic, timed by the audio clock:

```html
<!doctype html>
<meta charset="utf-8">
<title>Animatic</title>
<audio id="vo" src="guide-read.mp3" controls></audio>
<img id="frame" alt="" width="540" height="960">
<script>
  const beats = [[0, 'f01.png'], [2, 'f02.png'], [6, 'f03.png'], [11, 'f04.png']];
  const vo = document.getElementById('vo'), img = document.getElementById('frame');
  vo.addEventListener('timeupdate', () => {
    const t = vo.currentTime;
    img.src = beats.filter(([s]) => s <= t).pop()[1];
  });
</script>
```

## 6. Approval rounds

| Round | Shown | Feedback asked | Stage |
| --- | --- | --- | --- |
| 1 | Script and storyboard | Keep, change, remove per beat | explore |
| 2 | Styleframes | One direction; keep, change, remove per part | explore |
| 3 | Animatic | Pacing per beat; muted read | refine |
| 4 | Low-cost preview of the animation | Motion per beat | refine |
| 5 | Final render | Last fixes only | finalize |

Each round writes one entry in `design/decisions.md` with what was shown, the question, the answers per part, the decision and the rejected options.

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Animate first | Motion work starts before a styleframe is chosen | No animation before the yes on a styleframe |
| One idea, three colors | Three styleframes that differ only in palette | Name each idea in one sentence without a color |
| Wrong ratio board | Frames drawn at 16:9 for a vertical video | Draw at the delivery ratio with the overlay guide |
| Pacing found late | Text unreadable in the final render | Fix pacing in the animatic, muted and with sound |
| Generated logo | A styleframe with a generated wordmark | Place the supplied logo file |
| Board with no sound | The storyboard has no sound column | Every frame states its sound |
