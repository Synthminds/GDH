# Export and delivery

Read this file at steps 18 and 19 of `motion-video`. It covers the master and platform versions, export defaults, safe areas, captions files, thumbnails, web embeds, result link lifetimes, AI-content disclosure and the delivery record.

Evidence. Every platform number here comes from vendor blogs found by search on 2026-11-23. The sources disagree, and no platform help page was read. Each value is a default to re-check on the platform's own page before delivery. Codec, frame-rate and loudness values are from memory. The web embed rule comes from the Vercel Web Interface Guidelines, read 2026-11-23. Link lifetimes come from the connector cards.

## 1. Master first, then versions

1. Export one master at the highest quality the route allows, at the master ratio.
2. Make each platform version from the master: reframe, resize, re-caption. Never re-generate a shot to change a ratio.
3. Reframe on purpose. A horizontal shot cropped to vertical must keep the subject. Plan a vertical framing in the storyboard when vertical matters.
4. Keep one constant frame rate through the whole pipeline: 24, 25, 30 or 60. Choose it once.

## 2. Export defaults

Default: re-check each value on the platform's own help page on the day of delivery. Record the page and the date in the closing report.

| Target | Ratio | Size | Container and codec | Notes |
| --- | --- | --- | --- | --- |
| Vertical short (TikTok, Reels, Shorts) | 9:16 | 1080 x 1920 | MP4, H.264 video, AAC audio | One master uploads to all three, per the guides |
| Horizontal (YouTube, web, LinkedIn desktop) | 16:9 | 1920 x 1080 | MP4, H.264, AAC | |
| Square feed | 1:1 | 1080 x 1080 | MP4, H.264, AAC | |
| Portrait feed | 4:5 | 1080 x 1350 | MP4, H.264, AAC | |
| Web hero loop | Layout ratio | Display size at 2x density, or less | MP4 (H.264) and WebM | Muted, short, small file |

Audio defaults, from memory: 48 kHz; about -14 LUFS integrated; true peak at or below -1 dBTP.

Length limits change often. Reported 2026 values: Shorts up to 3 minutes; TikTok up to 10 minutes; Reels 3 minutes when recorded in the app. Confirm before planning a long piece.

FFmpeg examples for versions, from memory of FFmpeg options. Run them on copies:

```
# master to a 9:16 H.264 file, constant 30 fps, AAC audio
ffmpeg -i master.mov -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -r 30 -c:v libx264 -pix_fmt yuv420p -crf 18 -c:a aac -b:a 192k -ar 48000 -movflags +faststart vertical.mp4

# web hero loop: no audio, small, plus a WebM
ffmpeg -i loop.mov -an -vf scale=1280:-2 -c:v libx264 -pix_fmt yuv420p -crf 26 -movflags +faststart hero.mp4
ffmpeg -i loop.mov -an -vf scale=1280:-2 -c:v libvpx-vp9 -b:v 0 -crf 36 hero.webm

# poster frame at 1 s
ffmpeg -ss 1 -i hero.mp4 -frames:v 1 hero-poster.jpg
```

## 3. Safe areas for vertical video

Keep text, faces and calls to action inside a central safe area. Platform buttons, captions and the profile line cover the edges.

Default: a central area of about 900 x 1400 px in a 1080 x 1920 frame. Guides list bottom margins near 300 to 320 px and a top margin near 210 px for one platform. The sources disagree. Confirm by placing a draft in the real app.

Rules:

1. Draw the overlay as a guide layer on the storyboard and the styleframes.
2. Before delivery, upload a private draft or use the app's preview and look at it on a phone.
3. The right edge holds the platform's buttons. Keep the call to action off it.

## 4. Captions

1. Deliver a sidecar file for every version that has speech: `.srt` for most platforms, `.vtt` for the web.
2. Burn captions into a version only when the platform shows no captions or the placement plays muted with no caption support.
3. Burned captions sit inside the safe area and meet the contrast floor, or sit on a solid backing.
4. Default: caption height about 4 to 5% of the frame height; one or two lines; about 32 to 42 characters a line. Rules of thumb.
5. Captions match the final audio word for word, including names and numbers.

A minimal WebVTT file:

```
WEBVTT

00:00:02.000 --> 00:00:05.800
Your weekly report still takes a day.

00:00:06.000 --> 00:00:10.500
Connect your sources once.
```

## 5. Thumbnail and first frame

1. The first frame works as a thumbnail: subject visible, text readable small.
2. Export a separate thumbnail where the platform takes one, at the platform's size.
3. For the web, export a poster image from a strong frame.

## 6. Web embeds

1. Use a `video` element, not a GIF. A muted, looping, inline video is far smaller.
2. Set `muted`, `loop`, `playsinline` and a `poster`. Autoplay only when muted.
3. Under reduced motion, show the poster and a play control instead of autoplay.
4. Pause the loop when it is off screen.
5. Serve the files from the project. Do not hotlink a tool's result URL.
6. Give the video a text alternative nearby when it carries content, and captions when it has speech.

```html
<video class="hero" autoplay muted loop playsinline preload="metadata" poster="/video/hero-poster.jpg">
  <source src="/video/hero.webm" type="video/webm">
  <source src="/video/hero.mp4" type="video/mp4">
</video>
<script>
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const v = document.querySelector('video.hero');
    v.removeAttribute('autoplay'); v.pause(); v.controls = true;
  }
</script>
```

## 7. Result links expire

| Source | Lifetime stated in the card |
| --- | --- |
| A hosted variable render link | Seven days |
| A motion import link into a hosted studio | 90 days after the last send |
| A design canvas send-to URL | About ten minutes |
| Generation and export links in several tools | Short-lived; not always stated |

Rules:

1. Download every result at once into `design/assets/video/<slug>/`.
2. Check the file: it plays, it has the expected length and size, it is not an error page saved under a video name.
3. Record it in the manifest with its sha256.

## 8. AI-content disclosure

1. Platforms ask creators to label realistic generated people, voices or scenes. One 2026 guide says the toggle is required at upload; others disagree.
2. Default: set the platform's AI-content label whenever the video contains a generated realistic person, a cloned or designed voice, or a generated realistic scene.
3. Confirm the rule on each platform's help page before upload.
4. Record what was disclosed and where in the delivery record.
5. GATE: the upload itself is exposure. Ask the user before any upload, post, share link or hosted project.

## 9. The delivery record

Add to the closing report and to `video/delivery.md`:

```
Version: vertical-9x16 | 1080x1920 | 30 fps | 00:30 | H.264/AAC | 18.2 MB | sha256 <hash>
Captions: vertical-9x16.srt (sidecar); burned: no
Spec re-checked: <platform help page>, <date>
Watched on: <phone model>, in the app draft view
AI label: set (generated hook footage)
```

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Spec from memory | Wrong safe area; text under buttons | Re-check the platform page; test a draft on a phone |
| Re-generate to reframe | A new clip generated for each ratio | Reframe from the master; plan vertical framing |
| Mixed frame rates | Judder at cuts | One constant rate through the pipeline |
| GIF on the web | A 12 MB animated GIF hero | A muted looping video with a poster |
| Dead links | Assets vanish after a week | Download at once; record with a hash |
| Missing label | A generated presenter posted unlabelled | Set the disclosure when it applies |
| Upload without asking | A draft posted to a public account | Ask before any upload |
