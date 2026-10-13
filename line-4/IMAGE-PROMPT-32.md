# Round 32 image prompt

Tool: built-in `image_gen`. The input was record 31's hash-verified wall,
downloaded into `artifacts/line-4/wall.png`. The generated image bytes were
received through the tool, so no external local file needed to be read.

Exact prompt:

> Use case: precise-object-edit. Edit target: the supplied square prehistoric cave wall. Keep its exact square framing, rough warm brown stone, cracks, uneven torchlight, all existing cave paintings and every ancestor pigment mark absolutely unchanged. Keep the main recognizable Pepe frog with broad mouth and heavy-lidded eyes and both of his five-digit hands unchanged. Preserve the existing five-digit hand stencil. Add ONLY one small, humble pigment mark on the currently vacant rock LEFT of Pepe's face and ABOVE his raised hand: the rectangle from approximately x=255 to x=405, y=385 to y=475 on the 1254 by 1254 source. The new mark depicts one rough red-ochre notched pebble fitting precisely into a shallow charcoal outline, with a short faint chalk trace leading to a matching small ochre pebble beside it. Symbolic primitive stone-tool comparison, showing that matching shape matters. Handmade uneven charcoal, red/yellow ochre and faint chalk only, rubbed into the porous rock, worn and translucent with bare stone grain showing through. No new hands or frogs. No letters, numbers, caption, signature, logos, watermarks, borders or frames. Do not repaint, move, simplify, erase or redraw ANY existing mark. Do not change the background anywhere. Maintain original dimensions if possible. The only permitted saved project image output is artifacts/line-4/wall-v13.png; return the actual edited image bytes.

Preservation review restricted the generated result to two vacant-rock patches:
`[244,365,206,123]` and `[244,488,100,17]` (x, y, width, height).
The lower-right area was excluded to preserve the old raised hand/stone.
ffmpeg composited those patches with RGB output and made the 512-pixel JPEG.
No intermediate or discarded picture is retained in the workspace.
