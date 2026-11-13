# Maivoc visual identity — M4 / v1

**Canonical concept:** the connected-M, not the alternative portal/lock concept. This is a fresh Maivoc symbol consisting of two violet/mint M wings, a **three-node connected path**, and an open transition that represents several AI models in one workspace.

## Brand promise and copy
- Name: **Maivoc** (capitalize M; use lowercase only in domain/URL).
- Primary tagline: **Every model. One workspace.**
- Secondary proposition: **Switch. Compare. Connect.**
- Voice: calm, precise, capable, accessible. Don't claim that free cloud inference is confidential or unlimited.
- UX order: **Connect → Converse → Switch → Compare → Search**.

## Color tokens
| Token | Hex | Usage |
|---|---|---|
| Charcoal | `#0B0F17` | Primary dark canvas / PWA tile |
| Violet | `#5B3FF6` | Connected-M wing, active selection |
| Indigo | `#5135F5` | Gradient start |
| Mint | `#7FE4C3` | Connected-M accent / success |
| Deep teal | `#164D86` | Wing fold / subtle depth |
| White | `#FFFFFF` | Dark-theme primary text / connector |
| Warm neutral | `#F8FAFC` | Light-theme app background |

Treat token values as intended UI palette; the logo SVG gradients use additional intermediate stops. Meet WCAG AA contrast for all functional text, particularly mint on white.

## Typography
**Inter** for product UI and wordmark. Recommended headings: semibold/bold, body: regular/medium. Prefer an accessible readable fallback. The SVG lockup includes a DejaVu Sans fallback; PNG is the reproducible display asset.

## Mark construction
- The `M` must retain both wings, three white circular nodes, connecting arc and open internal pathway.
- Keep clear space of at least **12% of the mark's width** all around.
- Minimum size: 24 px for standalone app/favicon mark. At 16 px use the provided raster instead of redrawing details.
- For the horizontal lockup, use the provided transparent PNG or SVG; do not separately rebuild letter spacing.

## Variant guidance
- Transparent `maivoc-mark.png` or SVG for editorial, hero, iconography and light/dark layouts.
- Transparent `maivoc-lockup.png` or SVG for README, sponsorship, presentation titles.
- Dark square icons with centered mark for browser install, mobile and system menus.
- Maskable icon adds extra padding so operating systems can crop safely.

## Don't
- Don't substitute a padlock/cloud/portal emblem.
- Don't recolor or modify the node positions.
- Don't apply drop shadows or clipping that cut off nodes.
- Don't put free cloud models in the **Local · Private** category.
- Don't represent Maivoc as an official LibreChat product or imply endorsement.

## Attribution
Maivoc visual artwork was created for this project, independently of LibreChat's upstream marks. The separate application engine is based on **LibreChat (MIT)**, and its source and required notices remain in `docs/UPSTREAM.md` and `third_party/LibreChat-LICENSE`. Brand/trademark rights are not established by this guide; obtain project-owner approval for unrelated commercial use.

See [MEDIA_GUIDE.md](MEDIA_GUIDE.md) for exact files, placement and build steps.
