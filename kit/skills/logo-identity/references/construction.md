# Construction, optical correction and path hygiene

Read this file at step 9 of `logo-identity`. It covers how to redraw a chosen concept as a clean vector, the optical corrections, wordmark craft, small-size versions, SVG authoring rules, the path hygiene list and the failure patterns.

Evidence. The GDH research found no primary source on logo construction. It records only the outcome to reach: few anchor points, consistent stroke weights, optical corrections for curves and overshoot, closed paths, outlined strokes and text, no raster. Everything else in this file is drawing practice written from memory. Every number is a default. The eye decides, at the real sizes. A corrected mark is UNTESTED until you view it at 16px and at large size.

Terms. The master is the vector file that every export comes from. A unit is the base measure of the drawing, often the stroke width. Overshoot is the amount a round or pointed shape extends past a flat one. To outline is to convert a stroke or live text into a closed shape.

## 1. Set up the drawing

1. Draw in a square `viewBox` with round numbers, for example `0 0 96 96` for a mark.
2. Choose the unit. Default: the main stroke width is the unit. Sizes, gaps and radii are multiples or simple fractions of it.
3. Write the unit and the rules as a comment-free note in the direction file, not inside the SVG.
4. Decide the stroke system: one weight, or two weights with a fixed ratio.
5. Decide the corner system: sharp, one radius, or radii that grow with the shape.
6. Draw the skeleton first: center lines and key points. Then give it weight.
7. Keep coordinates on whole or half units. A value like 23.871 is a sign of drift.

## 2. Draw with few points

1. Use the fewest points that hold the shape.
2. Put curve points at the extremes: the top, bottom, left and right of a curve.
3. Keep curve handles horizontal or vertical at those extreme points.
4. A quarter circle needs two points. Its handle length is about 0.55 times the radius.
5. Use real circles and rectangles for circular and rectangular parts. Convert them to paths at the end.
6. Build complex shapes from simple ones: add, subtract, intersect. Then merge to one path for each color.
7. Mirror for symmetry. Draw one half, reflect it, and join. Do not draw both halves by eye.
8. Where a straight line meets a curve, the handle continues the line. No kink.

Test: delete any one point in your mind. If the shape would not change, the point should not exist.

## 3. Optical corrections

Geometry and perception disagree. Correct by eye, in small steps, and compare each step with the uncorrected version.

| Problem | What you see | Correction |
| --- | --- | --- |
| Overshoot | A circle or a point at the same height as a square looks smaller | Extend round and pointed shapes past the flat edges. Default: 1 to 3% of the height. |
| Optical center | A shape centered by numbers in a frame looks low | Move it up slightly. Default: 1 to 3% of the frame height. |
| Triangle in a circle | A centered play triangle looks pushed toward its flat side | Move it toward its point until the masses balance |
| Horizontal against vertical | A horizontal stroke looks thicker than a vertical of the same width | Thin the horizontals. Default: 3 to 8%. |
| Round against straight | A round stroke looks thinner than a straight one of the same width | Thicken the widest part of the curve slightly |
| Joins | Where strokes meet at an acute angle, a dark knot forms | Thin the strokes toward the join, or open a small notch |
| Diagonals | A diagonal looks heavier or lighter than the uprights | Adjust its width until the gray matches |
| Arc into line | A true arc joined to a straight edge looks like a bump | Start the curve earlier and flatten it into the line |
| Tight counters | Enclosed spaces fill in at small sizes | Open them. Enlarge the counter before you thin the stroke. |
| Reversed mark | White on black looks bolder than black on white | Default: reduce the weight of the reversed version by 2 to 5%, when the difference shows |
| Mark beside letters | A symbol of the same height as the capitals looks small or large | Size it by mass, not by height |

Rules:

1. Correct at the size where the problem shows. Then check every other size.
2. One correction at a time. Keep the previous version to compare.
3. A construction grid explains a mark. It does not prove it. When the grid and the eye disagree, the eye wins.
4. Record the corrections in the direction file. A later editor must not "fix" them back to geometry.

## 4. Wordmark craft

1. Start from a typeface whose license allows logo use, or draw the letters. `find-assets` reads the license.
2. Choose the face by the method of `typography`: from the subject and the brand words.
3. Make one or two purposeful changes that tie the letters to the idea. A wordmark with ten tricks has no idea.
4. Space the letters by area, not by distance. The white between each pair should look equal.
5. Work in threes. Look at three letters, balance the two gaps, move one letter along, repeat.
6. Typical order of gaps, widest to tightest: two straight sides, straight beside round, two round sides, diagonals and open letters.
7. Turn the word upside down or blur it. Uneven gaps show at once.
8. Capitals need more space than lowercase. Default: open the spacing of an all-caps wordmark.
9. Check problem pairs by eye: letters with overhangs, diagonals beside straights, open letters at the end.
10. Align the letters optically: round letters overshoot the baseline and the top line.
11. Convert the letters to outlines. The master holds no live text.
12. Keep an editable copy with the font name and the spacing values in `source/`.

A wordmark in a second script is drawn for that script. Do not type it in a fallback font. A reader of the script reviews it.

## 5. Mark and wordmark together

1. Derive the relation from the unit. The gap between mark and wordmark is a number of units.
2. Match the weights. The stroke of the mark and the stems of the letters look related.
3. Align by eye to the cap height, the x-height or the baseline. Say which in the rules.
4. Size the mark by mass. Default: a mark slightly taller than the capitals reads as equal.
5. Fix each lockup as one drawing. Nobody rearranges the parts later.

## 6. Small-size versions

One drawing rarely serves every size. Plan size versions like a type designer plans optical sizes.

| Version | Use | Changes |
| --- | --- | --- |
| Full | Large sizes | All detail |
| Standard | Most uses | The reference drawing |
| Small | Favicon, tiny avatar, small print | Fewer parts, heavier strokes, larger counters, wider gaps |

Rules:

1. The small version keeps the idea and drops detail. It is not a shrink of the full version.
2. For 16px and 32px, draw on that pixel grid. Put edges on whole pixels. A half-pixel edge renders as a blur.
3. State in the usage sheet at which size each version takes over.
4. Test each version at its own smallest size.

## 7. SVG authoring rules for the master

1. One `svg` element with a `viewBox`. No fixed width or height in the master.
2. Paths only in the final master. No `text`, no `image`, no `use` of outside files.
3. No stroke left as a stroke. Outline every stroke, so the weight scales with the mark.
4. No filter, mask, clip path or opacity. No gradient in the one-color master.
5. No transform. Apply transforms to the coordinates.
6. One path for each color region, merged. Counters are holes in the path, not white shapes on top.
7. Use `fill="currentColor"` in the one-color master. The mark then takes the text color where it is placed.
8. Round coordinates to two decimals at most. Fewer when the unit grid allows.
9. Check the fill rule. A counter that fills in means the inner path runs the wrong way for the rule in use.
10. Add a `title` when the SVG is placed inline as the only name of a link. Otherwise the page gives the name.
11. No editor metadata, no hidden layers, no unused definitions.
12. Keep the unoptimized working file in `source/`. Optimize a copy.

## 8. Path hygiene list

Run this on the master before the tests. Each line is a yes or a fix.

1. Every path is closed.
2. No stray point, no path with fewer than three points, no zero-size shape.
3. No two points sit on the same place.
4. No stroke remains. No live text remains.
5. No raster and no data string is embedded.
6. No shape lies outside the view box.
7. No white shape hides a black one.
8. Symmetric marks are exactly symmetric. Mirror and compare.
9. Curve points sit at the extremes. No kink where a line meets a curve.
10. The point count is as low as the shape allows. Compare with your first clean drawing.
11. The view box fits the mark with no accidental margin. Clear space is a rule, not empty canvas.
12. The file opens the same in two different renderers.

## 9. Checks after construction

1. View at 16px, 32px, 64px, 256px and 1024px. Compare neighbors.
2. View in black on white and white on black, side by side.
3. Blur the mark. The silhouette is still that mark.
4. Overlay the corrected version on the geometric version. The differences are small and all on purpose.
5. Put the mark back on the competitor sheet at 32px.
6. Then run the test suite.

## 10. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Pure geometry | Circles and squares at equal heights; the round parts look small | Add overshoot |
| Point soup | Hundreds of points from a trace | Redraw with points at the extremes |
| Live stroke | The mark gets thin when enlarged and fat when reduced | Outline every stroke |
| Live text | The wordmark changes on another machine | Outline the letters |
| Default spacing | The wordmark keeps the font's own spacing | Space by area, in threes |
| Typed logo | An unchanged typeface with no drawn decision, shown as the wordmark | One purposeful change, or call it what it is and ask |
| White patch | A white shape drawn over black to fake a hole | Make it a real hole |
| Grid worship | A visibly wrong shape kept because the grid says so | The eye wins |
| One size fits all | The full drawing shrunk to a favicon | Draw the small version |
| Blurry icon | A 16px icon with edges between pixels | Snap edges to the pixel grid |
| Drifted numbers | Coordinates with many decimals everywhere | Redraw on the unit grid |
