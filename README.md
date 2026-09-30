# kWhCompare

- `build.py` builds the whole site into `site/` (run by Netlify on every change).
- `content/queue.json` is the list of upcoming article topics. Add topics with `"status": "pending"`.
- `content/articles/` holds published articles written by the automation.
- `.github/workflows/publish.yml` writes a new article every Tuesday and Friday.
- Repository variable `PUBLISH_MODE`: `review` (default, opens a pull request to approve) or `auto` (publishes directly).
