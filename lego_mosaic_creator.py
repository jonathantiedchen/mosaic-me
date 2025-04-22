import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import io
import math
import base64
import os
from lego_colors import LEGO_COLORS_ALL
from lego_colors_round import LEGO_COLORS_ROUND
from lego_colors_square import LEGO_COLORS_SQUARE

# Standard baseplate sizes
BASEPLATE_SIZES = [
    {"name": "16×16", "size": 16},
    {"name": "32×32", "size": 32},
    {"name": "48×48", "size": 48},
    {"name": "64×64", "size": 64}
]

# ------------------------------ CORE FUNCTIONS ------------------------------

def find_closest_lego_color(r, g, b, lego_colors):
    """Find the closest LEGO color to the given RGB values."""
    min_distance = float('inf')
    closest_color = None
    for color in lego_colors:
        name, hex_color, cr, cg, cb = color
        distance = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_color = color
    return closest_color

def create_mosaic(image, mosaic_size, lego_colors):
    """Create a LEGO mosaic from an image."""
    try:
        # Make a copy to avoid modifying the original
        img_copy = image.copy()
        
        # Ensure we're working with RGB mode
        if img_copy.mode != 'RGB':
            img_copy = img_copy.convert('RGB')
            
        # Try different resize methods if one fails
        try:
            img_resized = img_copy.resize((mosaic_size, mosaic_size), Image.Resampling.LANCZOS)
        except (AttributeError, Exception):
            try:
                img_resized = img_copy.resize((mosaic_size, mosaic_size), Image.LANCZOS)
            except (AttributeError, Exception):
                img_resized = img_copy.resize((mosaic_size, mosaic_size), Image.NEAREST)
                
        # Convert to numpy array for efficient processing
        pixel_data = np.array(img_resized)
        
        # Create the mosaic
        mosaic_data = []
        color_counts = {}
        
        # Process each row and column
        for y in range(mosaic_size):
            row = []
            for x in range(mosaic_size):
                r, g, b = pixel_data[y, x]
                lego_color = find_closest_lego_color(r, g, b, lego_colors)
                row.append(lego_color)
                
                color_name = lego_color[0]
                color_counts[color_name] = color_counts.get(color_name, 0) + 1
            
            mosaic_data.append(row)
            
        return mosaic_data, color_counts
        
    except Exception as e:
        st.error(f"Error creating mosaic: {str(e)}")
        return None, None

def draw_mosaic(mosaic_data, pixel_size=20):
    """Draw the mosaic and return as an image."""
    if not mosaic_data:
        return None
        
    mosaic_size = len(mosaic_data)
    
    # Create a new image with white background
    img_width = mosaic_size * pixel_size
    img_height = mosaic_size * pixel_size
    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw the mosaic
    for y in range(mosaic_size):
        for x in range(mosaic_size):
            color = mosaic_data[y][x]
            hex_color = color[1]  # Use hex color
            
            # Convert hex to RGB
            r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
            
            # Draw filled rectangle
            x1 = x * pixel_size
            y1 = y * pixel_size
            x2 = x1 + pixel_size - 1
            y2 = y1 + pixel_size - 1
            draw.rectangle([(x1, y1), (x2, y2)], fill=(r, g, b), outline=(128, 128, 128))
    
    return image

def draw_instructions(mosaic_data, pixel_size=24, color_counts=None, lego_colors_used=None):
    """Draw the building instructions and return as an image."""
    if not mosaic_data:
        return None
        
    mosaic_size = len(mosaic_data)
    
    # Calculate the main grid height and the legend height
    grid_height = mosaic_size * pixel_size
    legend_height = 0
    
    # Add space for color legend if provided
    if color_counts and lego_colors_used:
        # Calculate how many rows we need for the legend (4 colors per row)
        num_colors = len(color_counts)
        legend_rows = (num_colors + 3) // 4  # Ceiling division to get number of rows
        legend_height = legend_rows * 25 + 40  # 25px per row + 40px padding/header
    
    # Create a new image with white background including space for the legend
    img_width = mosaic_size * pixel_size
    img_height = grid_height + legend_height
    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Create a mapping of colors to numbers
    color_to_number = {}
    if color_counts:
        for i, color_name in enumerate(color_counts.keys()):
            color_to_number[color_name] = i + 1  # Start numbering from 1
    
    # Draw the mosaic with color numbers
    for y in range(mosaic_size):
        for x in range(mosaic_size):
            color = mosaic_data[y][x]
            color_name = color[0]
            hex_color = color[1]  # Use hex color
            
            # Convert hex to RGB
            r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
            
            # Draw filled rectangle
            x1 = x * pixel_size
            y1 = y * pixel_size
            x2 = x1 + pixel_size - 1
            y2 = y1 + pixel_size - 1
            draw.rectangle([(x1, y1), (x2, y2)], fill=(r, g, b), outline=(0, 0, 0))
            
            # Add color number text (adjust text color for visibility)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
            
            # Get the number for this color
            color_number = color_to_number.get(color_name, 0)
            
            # Draw color number
            number_text = str(color_number)
            text_width = 6 * len(number_text)  # Approximation
            text_height = 10  # Approximation
            text_x = x1 + (pixel_size - text_width) // 2
            text_y = y1 + (pixel_size - text_height) // 2  # Center in the cell
            draw.text((text_x, text_y), number_text, fill=text_color)
    
    # Add color legend if provided
    if color_counts and lego_colors_used:
        # Draw legend header
        draw.text((10, grid_height + 10), "Color Legend:", fill=(0, 0, 0))
        
        # Draw color swatches with names and numbers
        col_width = img_width // 4
        row_height = 25
        
        i = 0
        for color_name, count in color_counts.items():
            color_info = next((c for c in lego_colors_used if c[0] == color_name), None)
            if color_info:
                col = i % 4
                row = i // 4
                
                # Calculate position
                x_pos = col * col_width + 10
                y_pos = grid_height + 35 + (row * row_height)
                
                # Draw color square
                hex_color = color_info[1]
                r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
                draw.rectangle([(x_pos, y_pos), (x_pos + 15, y_pos + 15)], fill=(r, g, b), outline=(0, 0, 0))
                
                # Draw color number inside square
                color_number = color_to_number.get(color_name, 0)
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                number_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
                draw.text((x_pos + 4, y_pos + 2), str(color_number), fill=number_color)
                
                # Draw color name and count
                draw.text((x_pos + 20, y_pos + 2), f"{color_name} ({count})", fill=(0, 0, 0))
                
                i += 1
    
    return image

def get_image_download_link(img, filename, text):
    """Generate a download link for an image."""
    if img is None:
        return ""
        
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def main():
    st.set_page_config(
        page_title="LEGO Mosaic Creator",
        page_icon="🧱",
        layout="wide"
    )
    
    st.title("🧱 LEGO Mosaic Creator")
    st.write("Transform your images into LEGO mosaic art")
    
    # Initialize session state variables
    if 'selected_lego_colors' not in st.session_state:
        st.session_state.selected_lego_colors = LEGO_COLORS_SQUARE
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False
    if 'mosaic_created' not in st.session_state:
        st.session_state.mosaic_created = False
    if 'image_processed' not in st.session_state:
        st.session_state.image_processed = False
    
    col1, col2 = st.columns([3, 1])
    
    # Check if we should show the 'Start Over' button instead of the uploader
    if st.session_state.image_processed:
        if st.button("Start Over with New Image"):
            st.session_state.image_processed = False
            st.session_state.mosaic_created = False
            st.session_state.demo_mode = False
            if 'mosaic_data' in st.session_state:
                del st.session_state.mosaic_data
            if 'color_counts' in st.session_state:
                del st.session_state.color_counts
            if 'current_image' in st.session_state:
                del st.session_state.current_image
            st.rerun()
    
    # Only show the file uploader if no image is being processed
    if not st.session_state.image_processed:
        # File uploader - only show when not in demo mode
        if not st.session_state.demo_mode:
            uploaded_file = st.file_uploader("Upload an image (square format works best)", type=["jpg", "jpeg", "png"])
            
            # Demo mode button
            if st.button("Or Use Demo Image Instead"):
                st.session_state.demo_mode = True
                st.rerun()  # Rerun the app to update the UI
        else:
            # Exit demo mode button
            if st.button("Exit Demo Mode"):
                st.session_state.demo_mode = False
                st.session_state.mosaic_created = False
                if 'mosaic_data' in st.session_state:
                    del st.session_state.mosaic_data
                if 'color_counts' in st.session_state:
                    del st.session_state.color_counts
                st.rerun()  # Rerun the app to update the UI
    
    # Variables to store mosaic data
    mosaic_data = None
    color_counts = None
    
    # If an image is uploaded (when not in demo mode)
    if not st.session_state.demo_mode and not st.session_state.image_processed and 'uploaded_file' in locals() and uploaded_file is not None:
        try:
            # Load the image
            image = Image.open(uploaded_file)
            st.session_state.current_image = image
            
            # Display original image
            with col2:
                st.write("Original Image")
                st.image(image, width=150)
            
            # Mosaic settings
            with col1:
                st.write("### Mosaic Settings")
                
                # Select piece shape
                shape_options = ["Round 1x1 Plates", "Square 1x1 Plates", "All LEGO Colors"]
                shape_index = st.selectbox(
                    "Select Piece Shape:",
                    range(len(shape_options)),
                    format_func=lambda i: shape_options[i],
                    key="user_shape_selector"
                )
                if shape_index == 0:
                    selected_lego_colors = LEGO_COLORS_ROUND
                elif shape_index == 1:
                    selected_lego_colors = LEGO_COLORS_SQUARE
                else:
                    selected_lego_colors = LEGO_COLORS_ALL
                st.session_state.selected_lego_colors = selected_lego_colors

                # Select mosaic size
                size_options = [s["name"] + f" ({s['size']}×{s['size']} studs)" for s in BASEPLATE_SIZES]
                size_index = st.selectbox(
                    "Select Mosaic Size:",
                    range(len(BASEPLATE_SIZES)),
                    format_func=lambda i: size_options[i],
                    key="user_size_selector"
                )
                mosaic_size = BASEPLATE_SIZES[size_index]["size"]
                
                # Generate button
                if st.button("Generate LEGO Mosaic", key="user_generate_button"):
                    with st.spinner("Creating mosaic..."):
                        try:
                            mosaic_data, color_counts = create_mosaic(image, mosaic_size, selected_lego_colors)
                            if mosaic_data:
                                st.session_state.mosaic_data = mosaic_data
                                st.session_state.color_counts = color_counts
                                st.session_state.mosaic_created = True
                                st.session_state.image_processed = True
                                st.success("Mosaic created successfully!")
                                st.rerun()  # Force UI update
                        except Exception as e:
                            st.error(f"Error creating mosaic: {str(e)}")
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
    
    # Demo mode section
    elif st.session_state.demo_mode and not st.session_state.image_processed:
        try:
            # Try to load the demo image file
            demo_path = "demo_image.jpeg"
            try:
                demo_img = Image.open(demo_path)
                st.success(f"Successfully loaded demo image")
            except (FileNotFoundError, IOError):
                # If file not found or can't be opened, create a simple gradient image
                st.warning(f"Demo image file not found. Creating a simple gradient image instead.")
                demo_img = Image.new('RGB', (300, 300), color='white')
                draw = ImageDraw.Draw(demo_img)
                
                # Draw a simple pattern
                for y in range(300):
                    for x in range(300):
                        r = int(255 * x / 300)
                        g = int(255 * y / 300)
                        b = int(255 * (1 - (x + y) / 600))
                        draw.point((x, y), fill=(r, g, b))
            
            st.session_state.current_image = demo_img
                
            # Display the demo image
            with col2:
                st.write("Demo Image")
                st.image(demo_img, width=150)
            
            # Mosaic settings for demo
            with col1:
                st.write("### Demo Mosaic Settings")
                
                # Select piece shape
                shape_options = ["Round 1x1 Plates", "Square 1x1 Plates", "All LEGO Colors"]
                shape_index = st.selectbox(
                    "Select Piece Shape:",
                    range(len(shape_options)),
                    format_func=lambda i: shape_options[i],
                    key="demo_shape_selector"
                )
                
                if shape_index == 0:
                    selected_lego_colors = LEGO_COLORS_ROUND
                elif shape_index == 1:
                    selected_lego_colors = LEGO_COLORS_SQUARE
                else:
                    selected_lego_colors = LEGO_COLORS_ALL
                st.session_state.selected_lego_colors = selected_lego_colors
                
                # Select mosaic size
                size_options = [s["name"] + f" ({s['size']}×{s['size']} studs)" for s in BASEPLATE_SIZES]
                size_index = st.selectbox(
                    "Select Mosaic Size:",
                    range(len(BASEPLATE_SIZES)),
                    format_func=lambda i: size_options[i],
                    key="demo_size_selector"
                )
                mosaic_size = BASEPLATE_SIZES[size_index]["size"]
                
                # Generate button for demo
                if st.button("Generate Demo LEGO Mosaic", key="demo_generate_button"):
                    with st.spinner("Creating demo mosaic..."):
                        try:
                            # Create the mosaic
                            mosaic_data, color_counts = create_mosaic(demo_img, mosaic_size, selected_lego_colors)
                            if mosaic_data:
                                st.session_state.mosaic_data = mosaic_data
                                st.session_state.color_counts = color_counts
                                st.session_state.mosaic_created = True
                                st.session_state.image_processed = True
                                st.success("Demo mosaic created successfully!")
                                st.rerun()  # Force UI update
                        except Exception as e:
                            st.error(f"Error creating demo mosaic: {str(e)}")
        except Exception as e:
            st.error(f"Error with demo image: {str(e)}")
    
    # Handle case when reloading page with processed image
    if st.session_state.image_processed and 'current_image' in st.session_state:
        with col2:
            st.write("Original Image")
            st.image(st.session_state.current_image, width=150)
    
    # Check if mosaic data exists in session state
    if 'mosaic_data' in st.session_state and st.session_state.mosaic_data is not None:
        mosaic_data = st.session_state.mosaic_data
        color_counts = st.session_state.color_counts
    
    # If mosaic data is available
    if mosaic_data:
        try:
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["Mosaic Preview", "Building Instructions", "Shopping List"])
            
            # Tab 1: Mosaic Preview
            with tab1:
                st.write("### Mosaic Preview")
                pixel_size = st.slider("Zoom Level:", min_value=5, max_value=20, value=10)
                
                # Draw mosaic preview
                mosaic_img = draw_mosaic(mosaic_data, pixel_size)
                if mosaic_img:
                    st.image(mosaic_img)
                    
                    # Download link
                    st.markdown(
                        get_image_download_link(mosaic_img, "lego_mosaic.png", "Download Mosaic Image"),
                        unsafe_allow_html=True
                    )
            
            # Tab 2: Building Instructions
            with tab2:
                st.write("### Building Instructions")
                st.write("Follow the color-coded grid below to build your mosaic:")
                
                # Draw instructions with color legend
                lego_colors_used = st.session_state.get("selected_lego_colors", LEGO_COLORS_ALL)
                instructions_img = draw_instructions(mosaic_data, color_counts=color_counts, lego_colors_used=lego_colors_used)
                if instructions_img:
                    st.image(instructions_img)
                    
                    # Download link
                    st.markdown(
                        get_image_download_link(instructions_img, "lego_instructions.png", "Download Instructions with Color Legend"),
                        unsafe_allow_html=True
                    )
            
            # Tab 3: Shopping List
            with tab3:
                st.write("### Shopping List")
                st.write("Here are the LEGO 1×1 plates you need to buy:")
                lego_colors_used = st.session_state.get("selected_lego_colors", LEGO_COLORS_ALL)

                # Create shopping list dataframe
                shopping_data = []
                for color_name, count in color_counts.items():
                    color_info = next((c for c in lego_colors_used if c[0] == color_name), None)
                    if color_info:
                        shopping_data.append({
                            "Color Name": color_name,
                            "Quantity": count,
                            "Color Preview": color_info[1]
                        })
                
                # Sort by quantity (descending)
                shopping_df = pd.DataFrame(shopping_data).sort_values(by="Quantity", ascending=False)
                
                # Display shopping list
                for i, row in shopping_df.iterrows():
                    st.markdown(
                        f'<div style="display: flex; align-items: center; margin-bottom: 10px;">'
                        f'<div style="width: 20px; height: 20px; background-color: {row["Color Preview"]}; margin-right: 10px; border: 1px solid black;"></div>'
                        f'<span style="width: 150px;">{row["Color Name"]}</span>'
                        f'<span><b>{row["Quantity"]}</b> pieces</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                
                # Total count
                st.write(f"**Total Pieces:** {sum(color_counts.values())}")
                
                # Export shopping list as CSV
                csv = shopping_df[["Color Name", "Quantity"]].to_csv(index=False)
                st.download_button(
                    label="Download Shopping List (CSV)",
                    data=csv,
                    file_name="lego_shopping_list.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"Error rendering mosaic: {str(e)}")

if __name__ == "__main__":
    main()