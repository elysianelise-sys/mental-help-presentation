# Mental Help · Project presentation

The UI/UX project presentation for **Mental Help** by Elise, as an animated web slideshow (29 slides).

- **Live:** https://mental-help-presentation-chi.vercel.app
- **The app it presents:** https://mental-help-alpha.vercel.app

## Using the slideshow

- Arrow keys, Space or a click move between slides; swipe on a phone. **F** = full screen.
- Each slide animates in when you arrive. The last slide plays the ending video with music (volume control bottom-left).
- On a phone held upright, the slides become a scrollable list; tap one to open it, turn sideways to present.
- **Jump to a slide:** tap the "1 / 29" counter (or press **G**) to open a menu of slide previews, then click one to go there. Esc closes it.
- `#12` at the end of the link opens slide 12.

## What is in this repo

```
index.html        the whole slideshow (29 slides, navigation, animations, phone layout)
assets/           images, icons, photos and the ending video (ending-v18.mp4)
thumbs/           light pictures of each slide, used for the phone list view
vercel.json       static deploy settings
exports/          PDF of the deck, the ending video (MP4), the QR code PNG, the 15s showreel
source/           how it was made (reference, not needed to deploy)
  slides/         the 29 slide files and deck.json from the original Claude Slides deck
  site_build.py   builds index.html from source/slides + site_tpl.html (paths inside are from the original workspace)
  site_tpl.html   the slideshow shell: navigation, animations, phone view, music volume
  make_pdf_thumbs.py  renders thumbs/ and the PDF with Playwright
  map.json        asset id to file mapping used by site_build.py
  video/          ending video scenes (partA.html opener, partC.html end card), rend.py frame renderer,
                  music2.py (generates the bubbly 150 BPM track), ending-music2.wav, and their images
  qr/render.py    the themed QR code renderer (rose dots, orb centre)
```

Everything is static. There is no install or build step.

## Slides

1 Cover · 2–3 Problem and solution · 4–5 Audience and persona · 6 Scope (390px, one hand) · 7 User flow · 8–13 Design system (colour, type, mascot direction, rationale, emotion system) · 14 HTML prototype · 15–16 References · 17 Figma screens · 18 Live app · 19 New screens (Profile, Calendar, Settings) · 20–21 Bonus challenges · 22–26 Reflection (skills, hurdles, fixes after testing, concept to final) · 27 Final app in hand · 28 What's next · 29 Thank you (video with music and QR code).

The cover has a "Project links" row: Progressive assessment (Google Slides), Figma, Dribbble reference.

## Links used in the deck

- Live app: https://mental-help-alpha.vercel.app
- Figma screens: https://www.figma.com/design/AUItTBis7M5o89P9dCcskv
- User flow (Figma): https://www.figma.com/design/AUItTBis7M5o89P9dCcskv/Assignment-2-Deliverables?node-id=460-2
- Prototype (Figma): https://www.figma.com/design/AUItTBis7M5o89P9dCcskv/Assignment-2-Deliverables?node-id=456-59
- Dribbble reference: https://dribbble.com/shots/27716037-Mental-Health-Mobile-App
- Original Claude Slides deck: https://claude.ai/artifact/VNuk7dUBtVHGg7JgJ56QkR

## Deploy

Vercel project: **mental-help-presentation** in team **UIUX** (`uiux22`). Domain: `mental-help-presentation-chi.vercel.app`.

Connect this repo to that project (Vercel → mental-help-presentation → Settings → Git → Connect Git Repository). `vercel.json` makes Vercel serve the files as they are. Every push to `main` redeploys.

## Style

Fonts: Bricolage Grotesque (headings), Plus Jakarta Sans (body), JetBrains Mono (labels). Colours: ink `#2B1D25`, body `#6E5462`, eyebrow `#9B5C78`, wine `#713043`, pinks `#F29BB0` `#E98AA8` `#F9D5DE`, lilac `#D6CBF2` `#A99FE0`, peach `#FFD3B0` `#F49C8A`.
