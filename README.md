# Holyfin

A dark theme for [Jellyfin](https://jellyfin.org), unofficial and inspired by the look of
[HolyArrs](https://github.com/HolyArrs/HolyArrs): near-black greys, one red accent, Geist, and one
set of calm motion. The corners are square.

It is one stylesheet, written from scratch (no other theme sits under it), that only styles what
Jellyfin's web client and the apps built on it show. Nothing is installed on the server.

> Holyfin is not made by, or affiliated with, HolyArrs. It borrows ideas and colour values from how
> HolyArrs looks, no code.

## Use it

In Jellyfin, open **Dashboard, General, Custom CSS** and add:

```css
@import url("https://cdn.jsdelivr.net/gh/<user>/holyfin@v0.1.0/theme.css");
```

Name a version (`@v0.1.0`), not `@main`: a version never changes under you, and the CDN keeps it.

With [Ansible](https://www.ansible.com) or another tool that sets Jellyfin's branding, put that
one line in the Custom CSS setting.

## Change it

Everything below the first section reads from the tokens at the top of `theme.css`: the greys, the
accent, the type scale, the motion and the corner radius (`--radius`, square by default). To make
your own version, copy the file, change the tokens and import your copy instead.

## What it works with

| Holyfin | Jellyfin |
| ------- | -------- |
| 0.1.0   | 12.4     |

Jellyfin styles are built from class names that can change between versions. A check runs every
week against the newest Jellyfin and opens an issue when something has drifted (see below).

## Checks

| Check | What it does | When |
| ----- | ------------ | ---- |
| `npm run lint` | stylelint with `stylelint-config-standard` | every push and pull request |
| `python3 tools/check.py <jellyfin-web-dir>` | classes the theme styles still exist in that Jellyfin; no new fixed blue; no rounded corners; every variable is defined | every push and pull request, and every Monday against the newest Jellyfin |

The second check needs no running Jellyfin. The workflow takes the web client from the official
image and compares text. It can also be run locally against any copy of the `jellyfin-web` folder.

`tools/blue-baseline.json` holds how much fixed blue the Jellyfin it was made against has. When you
have looked at a new Jellyfin and are happy with the theme on it, run
`python3 tools/check.py <dir> --update-baseline` and commit the result.

## After a Jellyfin update: look at it

The checks find what has been renamed. What a page looks like, you check by eye, on these:

- [ ] Home: the rows, a poster, hovering a poster (red block behind it, light edge)
- [ ] A library: the grid, the A-Z strip, the tabs in the top bar
- [ ] A film page: the logo, the band with the title and buttons, the panel with video and audio
- [ ] A drop-down list (subtitles): glass list, red tick, opens below the field
- [ ] A dialog and a menu (the three dots)
- [ ] The dashboard and a settings page: no blue left, square corners
- [ ] The sign-in page

Then change the table above, and tag a new version.

## Credits

- Look: [HolyArrs](https://github.com/HolyArrs/HolyArrs) (colours and ideas, no code).
- Font: [Geist](https://github.com/vercel/geist-font) by Vercel, under the SIL Open Font License. It is delivered with
  the theme in `fonts/` (with its licence, `fonts/OFL.txt`), so nothing is loaded from Google.

## Licence

[MIT](LICENSE).
