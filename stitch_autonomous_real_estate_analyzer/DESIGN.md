---
name: Autonomous Real Estate Investment Analyzer
colors:
  surface: '#0c1322'
  surface-dim: '#0c1322'
  surface-bright: '#323949'
  surface-container-lowest: '#070e1d'
  surface-container-low: '#141b2b'
  surface-container: '#191f2f'
  surface-container-high: '#232a3a'
  surface-container-highest: '#2e3545'
  on-surface: '#dce2f7'
  on-surface-variant: '#bec9c0'
  inverse-surface: '#dce2f7'
  inverse-on-surface: '#293040'
  outline: '#89938b'
  outline-variant: '#3f4942'
  surface-tint: '#86d7ac'
  primary: '#86d7ac'
  on-primary: '#003823'
  primary-container: '#63b38a'
  on-primary-container: '#00432a'
  inverse-primary: '#126c48'
  secondary: '#9dcaff'
  on-secondary: '#003257'
  secondary-container: '#056eb5'
  on-secondary-container: '#e1edff'
  tertiary: '#ffb950'
  on-tertiary: '#452b00'
  tertiary-container: '#dd9406'
  on-tertiary-container: '#513300'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#a2f4c7'
  primary-fixed-dim: '#86d7ac'
  on-primary-fixed: '#002113'
  on-primary-fixed-variant: '#005234'
  secondary-fixed: '#d1e4ff'
  secondary-fixed-dim: '#9dcaff'
  on-secondary-fixed: '#001d35'
  on-secondary-fixed-variant: '#00497c'
  tertiary-fixed: '#ffddb3'
  tertiary-fixed-dim: '#ffb950'
  on-tertiary-fixed: '#291800'
  on-tertiary-fixed-variant: '#624000'
  background: '#0c1322'
  on-background: '#dce2f7'
  surface-variant: '#2e3545'
typography:
  display-lg:
    fontFamily: DM Serif Display
    fontSize: 48px
    fontWeight: '400'
    lineHeight: '1.1'
  headline-lg:
    fontFamily: DM Serif Display
    fontSize: 32px
    fontWeight: '400'
    lineHeight: '1.2'
  headline-md:
    fontFamily: DM Serif Display
    fontSize: 24px
    fontWeight: '400'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Outfit
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Outfit
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  body-sm:
    fontFamily: Outfit
    fontSize: 14px
    fontWeight: '300'
    lineHeight: '1.5'
  label-md:
    fontFamily: DM Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  label-sm:
    fontFamily: DM Mono
    fontSize: 10px
    fontWeight: '400'
    lineHeight: '1.2'
    letterSpacing: 0.1em
  headline-lg-mobile:
    fontFamily: DM Serif Display
    fontSize: 28px
    fontWeight: '400'
    lineHeight: '1.2'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 20px
  margin: 24px
  container-max: 1440px
---

## Brand & Style
The design system is engineered for the high-stakes world of autonomous real estate investment. The brand personality is **authoritative, analytical, and sophisticated**, designed to instill confidence in algorithmic decision-making. 

The aesthetic leverages **Dark-Mode Modernism** with a **Glassmorphic** twist. It emphasizes high data density without visual clutter, using a "Command Center" philosophy. Subtle glowing borders and deep navy surfaces create a sense of infinite depth, while the mint-green primary accent provides a "synthetic organic" feel—bridging the gap between cold data and the physical reality of real estate assets.

## Colors
The palette is rooted in a deep navy foundation to reduce eye strain during prolonged analysis. 
- **Primary (Sage Mint):** Used for growth indicators, primary CTAs, and active states. It signifies "Go" and financial health.
- **Secondary/Info (Cerulean):** Reserved for technical data points, tooltips, and neutral system notifications.
- **Surface Tiers:** Use `#111827` for standard backgrounds and `#1A2235` for elevated interactive elements or nested cards to create a clear structural hierarchy.
- **Borders:** A signature 1px stroke using `rgba(99,179,138,0.15)` creates a "radar screen" effect, subtly highlighting the perimeter of data containers.

## Typography
This design system utilizes a high-contrast typographic pairing:
- **DM Serif Display (Italic):** Used for primary headings and hero numbers to provide a sophisticated, "editorial" feel to financial reports. 
- **Outfit:** The workhorse for the UI. Use weight 300 for body copy to maintain a light, modern feel on dark backgrounds, and weight 600 for sub-headers and button text.
- **DM Mono:** Essential for all quantitative data, status badges, and technical metadata. This ensures that columns of numbers align perfectly and look "computed."

## Layout & Spacing
The system employs a **12-column fluid grid** for the main dashboard content. 
- **Desktop:** 24px margins and 20px gutters. 
- **Tablet:** 16px margins and 16px gutters.
- **Mobile:** 12px margins; cards typically stack into a single column.

Spacing follows a strict 4px baseline grid. Data-heavy sections (like property tables) should use `sm` (8px) padding to maximize information density, while editorial or overview sections use `md` or `lg` to allow the design to "breathe."

## Elevation & Depth
Depth is created through **Tonal Layering** rather than traditional shadows. 
1. **Base:** `#0A0E1A` (The background).
2. **Surface:** `#111827` (Main cards and containers).
3. **Overlay:** `#1A2235` (Active items, modals, and dropdowns).

To enhance the "analyzer" feel, use **backplate blurs** (backdrop-filter: blur(10px)) on navigation bars and modals. Interactive elements should feature a subtle "outer glow" rather than a drop shadow—achieved by using a 0px blur, 1px spread shadow with the Primary Accent color at 10% opacity.

## Shapes
The design system uses a **Rounded (Level 2)** shape language to soften the technical edge of the data. 
- **Standard Cards:** 16px (rounded-lg).
- **Secondary Buttons & Inputs:** 8px (rounded-md).
- **Chips & Status Badges:** Pill-shaped (999px) to distinguish them from structural elements.

## Components
- **Cards:** Background `#111827`, Border 1px `rgba(99,179,138,0.15)`. Padding should be consistent at 24px.
- **Status Badges:** 
    - *Done:* Sage Mint text on 10% opacity Sage Mint background.
    - *Running:* Cerulean text with a 2px pulse animation.
    - *Waiting:* Amber text, monospaced.
- **Circular Gauges:** Use a stroke width of 4px. The background track should be `text_muted` at 20% opacity; the active track uses the Primary Sage Mint or specific status color.
- **Inputs:** Dark background (`#0A0E1A`) with a 1px border that brightens to 40% opacity Sage Mint on focus. Use Outfit 400 for input text.
- **Data Chips:** Small, pill-shaped markers using DM Mono for attribute tagging (e.g., "CAP RATE", "ROI").
- **CTA Buttons:** Solid Sage Mint background with `#0A0E1A` text for maximum legibility and "clickability."