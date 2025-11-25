# Mosaic-Me Constitution

## Core Principles

### I. User Privacy First
No uploaded images are stored or persisted. All image processing happens in-memory only. User data is never shared with third parties beyond necessary analytics.

### II. Accurate Color Matching
LEGO color palettes must reflect real, purchasable LEGO pieces. Color matching algorithms must produce buildable results with available LEGO elements.

### III. Complete Build Workflow
Every generated mosaic must include: visual preview, building instructions with legend, and a shopping list exportable to LEGO Pick A Brick.

### IV. Simplicity
Keep the user interface minimal and focused. One clear path: upload image → configure → generate → download/purchase.

## Tech Stack

- **Framework**: Streamlit (Python web app)
- **Image Processing**: Pillow, NumPy
- **Analytics**: Google Sheets API via gspread
- **Deployment**: Streamlit Cloud

## Quality Standards

- All LEGO element IDs must be valid and current
- Color palettes must be maintained as LEGO inventory changes
- Mosaic output must be downloadable in standard formats (PNG, CSV)

## Governance

This constitution defines the minimum viable product requirements. Feature additions should not compromise the core workflow simplicity.

**Version**: 1.0.0 | **Ratified**: 2025-11-23 | **Last Amended**: 2025-11-23
