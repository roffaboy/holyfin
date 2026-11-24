# workflows

What runs on GitHub. None of it is needed to use the theme.

| Workflow | When | Does |
|---|---|---|
| [`check.yml`](check.yml) | Every PR, pushes to `main`, and every Monday | stylelint on `theme.css`; and a check that the classes it styles still exist in the newest Jellyfin and that Jellyfin has not gained more fixed blue ([`tools/check.py`](../../tools/check.py)). A Monday run that finds drift opens an issue |
| [`release.yml`](release.yml) | By hand: Actions → Release | Tags `main` with the next version (from the PR titles: `feat:`, `fix:`, `feat!:`) and writes the release notes |

Renovate ([`renovate.json`](../../renovate.json)) opens a PR every week with new versions of the
actions and of stylelint; patch updates merge by themselves once the checks pass.
