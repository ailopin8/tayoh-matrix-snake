# GitHub Pages / Quest publication

The static build runs the existing Python simulation in a dedicated browser worker using self-hosted Pyodide 0.27.7. The worker is the sole authority for that tab. No Python-to-JavaScript algorithm rewrite or paid backend is required. Initial loading downloads roughly 14 MB of Python runtime files plus the app; wait for the world to appear before starting.

## Runtime distinction

- `python3 server.py`: one shared laptop-hosted world, using the server API as before.
- GitHub Pages: one independent Python world per browser tab/device. The headset does not mirror or synchronize the laptop session. Closing/reloading resets the session; export replay first to retain actions. Runtime and source versions should match for deterministic replay.

The Pages site uses HTTPS and can be opened directly in **Meta Quest Browser** on Quest 3S. Wait for initialization, then select Enter VR. Successful immersive entry starts playback. Meta Virtual Display is not needed for this path. Physical headset entry, tracking, controls and frame rate still need testing on hardware.

## Build and deploy

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_pages.py
python3 -m http.server 8766 --directory dist
```

The static folder contains the interface, Python source and pinned runtime. Its configuration selects `browser-python`; the source `web/runtime-config.json` keeps laptop-server mode. Paths are relative to support GitHub Pages project subdirectories.

The included `.github/workflows/pages.yml` tests the Python implementation, builds `dist`, uploads a Pages artifact and deploys on pushes to `main`. Set repository Settings → Pages → Source to **GitHub Actions**. The repository must exist under the intended owner; publication is not complete until GitHub confirms deployment and the site loads successfully.

## Exports and input

Replay/outcome links download JSON from the selected authority, so they work in either mode without nonexistent Pages API endpoints. The worker checks expected tick numbers and serializes inputs and steps. Native browser tab sessions are isolated. Exports contain experiment labels entered by the user; keep those labels appropriate for any subsequent sharing.

## Dependencies

Three.js 0.170.0 and Pyodide 0.27.7 are vendored with their licenses. `web/vendor/pyodide` contains the loader, WebAssembly Python interpreter, standard-library archive and package index. No external CDN is contacted during runtime initialization. This pin is a reproducibility choice, not a claim to use the latest release.

Primary references: [GitHub Pages limitations](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site), [Pyodide loading](https://pyodide.org/en/0.27.7/usage/quickstart.html).
