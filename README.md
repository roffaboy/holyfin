# Holyfin

[![Check](https://github.com/roffaboy/holyfin/actions/workflows/check.yml/badge.svg)](https://github.com/roffaboy/holyfin/actions/workflows/check.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-informational.svg)](LICENSE)
![Jellyfin 12.4](https://img.shields.io/badge/Jellyfin-12.4-00a4dc?logoColor=white)

A calm, dark theme for [Jellyfin](https://jellyfin.org). Near-black greys, one red accent, square
corners and [Geist](https://github.com/vercel/geist-font), after the look of
[HolyArrs](https://github.com/HolyArrs/HolyArrs).

It is one stylesheet, written from scratch: no other theme sits under it. Nothing is installed on
the server, and it works in the web client and in the apps built on it.

> Holyfin is unofficial. It is not made by, or affiliated with, HolyArrs. It borrows ideas and
> colour values from how HolyArrs looks, no code.

<!--
Screenshots (add them in docs/screenshots/, then remove this comment):

![Home](docs/screenshots/home.png)
![A film page](docs/screenshots/film.png)
![Hovering a poster](docs/screenshots/hover.png)
![The dashboard](docs/screenshots/dashboard.png)
-->

## What you get

- **One accent.** Jellyfin's blue is gone everywhere: focus, links, switches, sliders, loading
  circles, the dashboard. It is the same red throughout.
- **Posters that react.** Hovering a poster lifts it 2 px, draws a light edge and puts a solid red block
  behind it. Watched titles get a green tick, counts are red, progress is red.
- **A film page with room.** A taller band for the title and buttons, the logo above it, the video
  and audio details in a quiet panel with small capitals as labels.
- **Glass where things open.** The top bar, menus and drop-down lists are blurred glass with a fine
  line, and the chosen item is a soft grey step with a red tick.
- **Geist, delivered with the theme.** Nothing is loaded from Google.
- **Calm motion** in one set of durations and curves, and none at all for anyone who asked their
  system for less motion.
- **Square corners.** One setting (`--radius`) if you would rather have them round.

## Install

In Jellyfin, open **Dashboard, General, Custom CSS** and add:

```css
@import url("https://cdn.jsdelivr.net/gh/roffaboy/holyfin@v0.1.0/theme.css");
```

Name a version (`@v0.1.0`), not `@main`. A version never changes under you, and the CDN keeps it.
Reload the page with Ctrl+Shift+R.

With a tool that sets Jellyfin's branding for you (for example Ansible), put that one line in the
Custom CSS setting.

To take it away again, empty the Custom CSS box.

### Pair it with the Jellyfin Enhanced plugin (optional)

[Jellyfin Enhanced](https://github.com/n00bcodr/Jellyfin-Enhanced) can put quality and rating tags on
every poster. In its settings, the **summary** layout shows one quiet pill ("1080p · 7.4") instead of
tags in all four corners, which suits the theme.

## Change it

Everything below the first section of `theme.css` reads from the tokens at the top.

| Token | What it is | Default |
| ----- | ---------- | ------- |
| `--bg`, `--surface`, `--surface-2`, `--surface-3` | page and panel greys | `#0b0b0c` to `#2a2a2e` |
| `--accent`, `--accent-fill` | the red, for text and icons, and for fills | `#ff453a`, `#d42d24` |
| `--text`, `--muted`, `--faint` | text colours | `#f5f5f7`, `#a1a1a6`, `#7c7c80` |
| `--radius` | corner radius of buttons, panels and fields | `0px` |
| `--font` | the typeface | Geist |
| `--dur-fast`, `--dur`, `--dur-slow` | how long motion takes | 150, 240, 360 ms |

To make your own version, copy `theme.css` (and the `fonts/` folder, or point `--font` at another
face), change the tokens and import your copy.

## Works with

| Holyfin | Jellyfin |
| ------- | -------- |
| 0.1.0   | 12.4     |

**Browsers.** The styled drop-down lists need Chrome or Edge 135 or newer. Elsewhere the browser's
own list is shown, which is fully usable. Everything else works in current Chrome, Edge, Firefox and
Safari.

Jellyfin's styles are built from class names that can change between versions, so the table above is
the version the theme was last looked at on. A check runs every week against the newest Jellyfin and
opens an issue when something has drifted.

## How it is kept working

| Check | What it does | When |
| ----- | ------------ | ---- |
| `npm run lint` | stylelint with `stylelint-config-standard` | every push and pull request |
| `python3 tools/check.py <jellyfin-web-dir>` | the classes the theme styles still exist in that Jellyfin; no new fixed blue; no rounded corners; every variable is defined | every push and pull request, and every Monday against the newest Jellyfin |

The second check needs no running Jellyfin. The workflow takes the web client from the official image
and compares text. It can also be run on your machine against any copy of the `jellyfin-web` folder.

`tools/blue-baseline.json` holds how much fixed blue the Jellyfin it was made against has. When you
have looked at a new Jellyfin and are happy with the theme on it, run
`python3 tools/check.py <dir> --update-baseline` and commit the result.

### After a Jellyfin update, look at it

The checks find what has been renamed. What a page looks like, you check by eye:

- [ ] Home: the rows, a poster, hovering a poster (red block behind it, light edge)
- [ ] A library: the grid, the A-Z strip, the tabs in the top bar
- [ ] A film page: the logo, the band with the title and buttons, the panel with video and audio
- [ ] A drop-down list (subtitles): glass list, red tick, opens below the field
- [ ] A dialog and a menu (the three dots)
- [ ] The dashboard and a settings page: no blue left, square corners
- [ ] The sign-in page

Then change the table above and tag a new version.

## Contributing

Issues and pull requests are welcome, especially a page that still shows blue or a class that moved.
Please run `npm ci && npm run lint` and `python3 tools/check.py <jellyfin-web-dir>` first. The look
follows HolyArrs, with square corners; changes that round things off are out of scope.

## Credits

- Look: [HolyArrs](https://github.com/HolyArrs/HolyArrs) (colours and ideas, no code).
- Font: [Geist](https://github.com/vercel/geist-font) by Vercel, under the SIL Open Font License. It is
  delivered with the theme in `fonts/` (with its licence, `fonts/OFL.txt`).

## Licence

[MIT](LICENSE).
