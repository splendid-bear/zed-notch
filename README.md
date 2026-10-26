# Zen Notch

An experimental `userChrome.css` mod for Zen's **Single Toolbar** layout. It styles the real address bar as a top-center notch with rounded lower corners. Clicking it or pressing Ctrl+L (Cmd+L on macOS) keeps it at the same top-center position and enlarges the field slightly, with native suggestions beneath it.

The notch is hidden until the pointer enters a **28px top-edge strip** over the content region (using the same sidebar compensation and side margins as its positioning). It fades in and remains visible while hovered, keyboard-focused, showing suggestions, or reporting an open URL-bar popup. Ctrl+L/Cmd+L reveals it directly. Moving away after finishing interaction fades it out. Adjust `--zen-notch-reveal-distance` in `zen-notch.css` to change the threshold.

The invisible hover strip intercepts pointer events in that narrow area; outside it, the hidden notch lets clicks reach the webpage. The threshold is measured from the window top and may need adjustment with extra title bars/toolbars.

## Status and limitations

This is a prototype, not a visually verified or published Zen Mods package. Toolbar selectors were checked against Zen's upstream development source; your installed release may differ.

- On Zen versions supporting CSS anchor positioning, horizontal placement uses the actual rendered sidebar edge and the opposite window gutter to center over the content region. The same rule applies to hover and Ctrl+L, including right-side sidebars. Older versions fall back to `--zen-sidebar-width` or the configurable `--zen-notch-sidebar-width` (250px by default); that fallback may need manual adjustment. Confirm alignment after sidebar resizing in your installed release.
- The notch overlays the page rather than reserving space. The top offset may need adjustment for your title bar, bookmarks toolbar, or window controls.
- Compact mode, fullscreen, popup windows, and toolbar customization retain the native layout. This initial version does not implement an always-visible notch in compact mode.
- Split view uses the combined content region, not the active pane. An additional web/AI sidebar is not compensated for.
- The original address-bar slot has zero reserved height while the notch is active. The input remains in the document for keyboard focus; any remaining navigation buttons retain their own row height. Native spacing returns in modes where the notch is disabled.
- The notch and its inverse corners use `#131313` in dark mode and `#ebebed` in light mode, following Zen's UI color scheme. The corner radius follows Zen's theme; a dedicated two-layer shadow separates the notch from the webpage, including in no-padding mode. Custom frame colors may differ from these fixed background colors.
- Exact centering and appearance need testing in your Zen version before treating this as finished browser integration.

## Install

Requires GNU Make and Python 3.8+; no Python packages or JavaScript loader are needed.

1. In Zen, open `about:profiles` and find the **Root Directory** of the profile in use (not Local Directory).
2. Open `about:config` and set `toolkit.legacyUserProfileCustomizations.stylesheets` to `true`.
3. Close Zen, then run from this repository, replacing the example path:

   ```sh
   make install PROFILE="/absolute/path/to/your/zen/profile"
   ```

4. Restart Zen with **Single Toolbar** selected.

The installer adds a managed import at the start of `chrome/userChrome.css` (after an existing charset declaration) and copies the stylesheet to `chrome/zen-notch/zen-notch.css`. Existing CSS is preserved; repeat installation updates the mod without duplicating the import. It refuses unmanaged destination directories and symlinked targets. It does not edit `prefs.js` or `user.js`.

## Uninstall

Close Zen and run:

```sh
make uninstall PROFILE="/absolute/path/to/your/zen/profile"
```

Restart Zen. Only the managed import and installed mod files are removed; other CSS and extra files are retained. The stylesheet preference is intentionally left unchanged because other mods may need it. An empty `userChrome.css` may remain after uninstall.

## Customize

Edit the variables at the top of `zen-notch.css`, then run `make install` again and restart Zen:

| Variable | Default | Purpose |
| --- | --- | --- |
| `--zen-notch-width` | `840px` | Maximum notch width |
| `--zen-notch-height` | `68px` | Idle field height |
| `--zen-notch-focused-width` | `1000px` | Maximum focused notch width |
| `--zen-notch-focused-height` | `80px` | Focused field height |
| `--zen-notch-padding-inline` | `24px` | Input content padding on each side, idle and focused |
| `--zen-notch-radius` | Zen content-container radius, or `14px` | Bottom corner radius |
| `--zen-notch-shoulder-radius` | `18px` | Inverse top-corner radius |
| `--zen-notch-top` | Zen element separation, or `8px` | Offset from window top |
| `--zen-notch-sidebar-width` | Zen sidebar width, or `250px` | Sidebar compensation; override if misaligned |
| `--zen-notch-background` | `light-dark(#ebebed, #131313)` | Light/dark notch and inverse-corner background |
| `--zen-notch-shadow` | Two-layer shadow, stronger in dark mode | Visible side/bottom shadow; use `none` to disable |
| `--zen-notch-animation-duration` | `220ms` | Expand/collapse duration |
| `--zen-notch-animation-easing` | `cubic-bezier(0.2, 0.8, 0.2, 1)` | Expand/collapse easing |

The notch animates its width and input height while staying centered. The suggestions list retains native content-driven height (it does not animate to/from `auto`). Reduced-motion preferences disable the transition. Rounded lower corners and concave top shoulders are retained in focused/open states. The shoulders use the same light/dark background as the notch.

## Validation

```sh
make test
```

Tests cover installer round trips, repeat installs/uninstalls, existing stylesheet preservation (including CRLF and BOM), unmanaged directories, symlinks, invalid profiles, and files added after installation. They do not validate browser rendering.

Manual browser checks still required: page-relative alignment, sidebar resizing and right-side layout, clicking the field, Ctrl+L, Escape, suggestions, site permissions, narrow windows, fullscreen video, and compact mode.
