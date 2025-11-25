# LEGO Mosaic Creator - Next Features to Implement

## Selected Features for Next Development Phase

### 1. Limited Palette Mode
**Feature:** Add a "Limited Palette" mode where users can specify exactly which colors they have available

**Implementation Details:**
- Allow users to select from a checklist of available LEGO colors
- Save user's color preferences for future sessions
- Generate mosaics using only the selected colors
- Show preview of how limiting colors affects the final result

---

### 2. Cost Estimation
**Feature:** Show cost estimation based on current LEGO Pick A Brick prices

**Implementation Details:**
- Integrate LEGO Pick A Brick pricing data (API or manual updates)
- Display total cost estimate before generation
- Break down cost by color in shopping list
- Show price per piece
- Update pricing periodically to maintain accuracy
- Display currency options (USD, EUR, etc.)

---

### 3. Interactive Image Cropping and Rotation
**Feature:** Built-in image cropping and rotation before mosaic generation - it should be interactive so the user can zoom and rotate the image inside of the frame

**Implementation Details:**
- Add interactive image editor before mosaic generation
- Allow users to:
  - Zoom in/out on the image
  - Rotate the image
  - Pan/move the image within the frame
  - Crop to specific aspect ratios or baseplate sizes
- Real-time preview of selected area
- Reset to original option
- Maintain image quality during transformations

**UI Considerations:**
- Overlay frame showing the mosaic boundaries
- Slider or pinch-to-zoom controls
- Rotation wheel or degree input
- "Fit to frame" quick action button
- Visual guides (grid lines, center markers)

---

### 4. Dithering Algorithms
**Feature:** Dithering algorithms for better gradient representation

**Implementation Details:**
- Implement multiple dithering algorithms:
  - Floyd-Steinberg dithering
  - Ordered dithering
  - Atkinson dithering
- Allow users to select dithering style or "None"
- Preview different dithering options before final generation
- Particularly useful for images with smooth gradients
- Explain what dithering does (tooltip/help text)

---

### 5. Edge Detection Mode
**Feature:** Edge detection mode for outline-focused designs

**Implementation Details:**
- Apply edge detection algorithms (Canny, Sobel, etc.)
- Create line art / outline style mosaics
- Adjustable edge sensitivity
- Option to combine with normal mosaic or pure outline
- Useful for:
  - Portraits
  - Logos
  - Graphic designs
  - Coloring-book style mosaics
- Preview edge detection results before mosaic generation

---

### 6. QR Code Generator
**Feature:** QR code generator that creates scannable LEGO QR codes

**Implementation Details:**
- Input field for URL or text to encode
- Generate QR code that works with LEGO brick constraints
- Ensure adequate size for scannability (minimum 32×32 recommended)
- Test/verify QR code is scannable after generation
- Use high error correction level to account for brick limitations
- Two-color mode (typically black and white) for best results
- Provide scanning instructions with the output

**Technical Notes:**
- QR codes require specific size constraints
- Error correction is critical for physical builds
- May need larger baseplate sizes (48×48 or 64×64)

---

### 7. Text-to-Mosaic Converter
**Feature:** Text-to-mosaic converter for custom messages - user should also be able to choose font color and background color

**Implementation Details:**
- Text input field for custom messages
- Font selection (readable LEGO-friendly fonts)
- Font size adjustment
- Color picker for text color
- Color picker for background color
- Multi-line text support
- Text alignment options (left, center, right)
- Preview before generation
- Automatic size recommendation based on text length
- Consider readability with LEGO resolution constraints

**UI Considerations:**
- Live preview as user types
- Warning if text is too long for selected baseplate
- Suggestion to use contrasting colors for readability
- Example texts to show possibilities

---

### 8. Rotatable 3D Preview (All Features)
**Feature:** Interactive 3D view of the completed mosaic showing brick depth and texture

**Implementation Details:**
- **3D Rendering:**
  - Use Three.js for WebGL-based 3D rendering
  - Model individual 1×1 LEGO plates with studs
  - Accurate brick dimensions and proportions
  - Realistic brick spacing and connections

- **Interactivity:**
  - Mouse drag to rotate view
  - Scroll/pinch to zoom
  - Click and drag to pan
  - Reset camera button
  - Preset viewing angles (front, top, 45° perspective)

- **Visual Features:**
  - Toggle between flat 2D view and 3D brick representation
  - Lighting effects to simulate real LEGO piece appearance
  - Show studs and brick connections for realistic preview
  - Optional: Show baseplate underneath
  - Optional: Cast shadows for depth perception

- **Performance:**
  - Level of Detail (LOD) for large mosaics
  - Efficient rendering for 64×64 and larger mosaics
  - Loading indicator for 3D model generation
  - Option to disable for low-performance devices

**Technical Requirements:**
- Three.js library integration
- GLTF/GLB model format for LEGO pieces
- WebGL support detection
- Mobile-friendly touch controls

---

### 9. Direct LEGO Pick A Brick Cart Integration
**Feature:** Direct LEGO Pick A Brick link generation with pre-filled cart

**Implementation Details:**
- Generate properly formatted CSV for LEGO Pick A Brick upload
- Direct link to Pick A Brick page with instructions
- One-click "Open in Pick A Brick" button
- Automatic formatting of elementId and quantity
- Regional URL detection (US, UK, EU, etc.)
- Instructions overlay showing upload process:
  1. Download CSV
  2. Go to Pick A Brick
  3. Upload file
  4. Review cart
  5. Checkout

**Technical Notes:**
- LEGO Pick A Brick CSV format: elementId, quantity
- Include baseplate in the export
- Verify all element IDs are valid
- Handle out-of-stock items gracefully

---

## Implementation Notes

### Maintaining Simplicity
While adding features, maintain the core principle: **upload image → configure → generate → download/purchase**

Consider:
- Collapsible "Advanced Options" sections for power users
- Default settings that work well for 90% of users
- Progressive disclosure - show advanced features only when relevant
- Tabbed interface to organize features without cluttering main flow
- Optional features that don't interrupt the basic workflow

### Technical Considerations
- **3D preview** may require Three.js or similar WebGL library
- **Cost estimation** needs API integration or regular price updates
- **Save/load features** require backend storage or local browser storage
- **Community features** require user authentication and content moderation
- **Export to specialized formats** (LDD, LDraw) requires format documentation
- **Interactive image editing** can use libraries like Cropper.js or React-Cropper
- **Dithering and edge detection** can use image processing libraries or custom algorithms
- **QR code generation** can use libraries like qrcode or qrcode.react

### User Experience Guidelines
- Every new feature should have a clear "skip" or "use default" option
- Advanced features should be clearly labeled as optional
- The basic flow should remain unchanged: quick and easy
- Help tooltips for complex features
- Examples/demos for new visualization features
- Progressive enhancement - basic features work without advanced options
- Clear visual feedback for all interactions
- Loading states for compute-intensive operations (3D rendering, edge detection)

### Development Priorities

**Phase 1: Image Processing Improvements**
1. Interactive image cropping and rotation
2. Edge detection mode
3. Dithering algorithms

**Phase 2: Visualization & Preview**
4. Rotatable 3D preview
5. Text-to-mosaic converter
6. QR code generator

**Phase 3: Shopping & Economics**
7. Cost estimation
8. Direct LEGO Pick A Brick cart integration
9. Limited palette mode

### Testing Considerations
- Test 3D preview on various devices and browsers
- Verify QR codes are scannable after physical build
- Test cost estimation accuracy with real LEGO prices
- Ensure image transformations maintain quality
- Performance testing with maximum baseplate sizes (128×128)
- Mobile responsiveness for all new features
- Accessibility for interactive controls
