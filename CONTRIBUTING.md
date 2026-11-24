# Contributing

Issues and pull requests are welcome, especially a page that still shows blue or a class that
Jellyfin has moved. The look follows HolyArrs, with square corners.

## Before you open a pull request

```sh
npm ci
npm run lint                              # stylelint, stylelint-config-standard
python3 tools/check.py <jellyfin-web-dir> # needs a copy of Jellyfin's web client
```

A copy of the web client is the `jellyfin-web` folder of the official image:

```sh
id=$(docker create jellyfin/jellyfin:latest)
docker cp "$id":/jellyfin/jellyfin-web web
docker rm "$id"
```

`tools/check.py` checks that the classes the theme styles still exist in that Jellyfin, that
Jellyfin has not gained more fixed blue than `tools/blue-baseline.json` records, that nothing is
rounded and that every variable is defined. Both checks run on every push and pull request, and
every Monday against the newest Jellyfin; a Monday run that finds drift opens an issue.

## After a new Jellyfin

When the weekly check finds drift, or after you update Jellyfin yourself:

1. Run the checks above against the new version and fix what they report.
2. Look at the pages by eye (the checks find what was renamed, not what looks wrong): home and a
   poster on hover, a library, a film page, a drop-down list, a dialog and a menu, the dashboard,
   a settings page and the sign-in page. Nothing should be blue and nothing rounded.
3. If you are happy with it, run `python3 tools/check.py <dir> --update-baseline`, commit the result,
   change the version table in the README and tag a new version (`git tag -a v0.1.1`).
