import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import io
import math
import base64
from lego_colors_round import LEGO_COLORS_ROUND
from lego_colors import LEGO_COLORS_ALL
from lego_colors_square import LEGO_COLORS_SQUARE


# Set page configuration
st.set_page_config(
    page_title="LEGO Mosaic Creator",
    page_icon="🧱",
    layout="wide"
)

# LEGO colors - based on commonly available colors
# Format: [name, hex, R, G, B]

# Standard baseplate sizes
BASEPLATE_SIZES = [
    {"name": "16×16", "size": 16},
    {"name": "32×32", "size": 32},
    {"name": "48×48", "size": 48},
    {"name": "64×64", "size": 64}
]

def find_closest_lego_color(r, g, b, lego_colors):
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
    img_resized = image.resize((mosaic_size, mosaic_size), Image.LANCZOS)
    if img_resized.mode != 'RGB':
        img_resized = img_resized.convert('RGB')
    pixel_data = np.array(img_resized)
    mosaic_data = []
    color_counts = {}
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


def draw_mosaic(mosaic_data, pixel_size=20):
    """Draw the mosaic and return as an image."""
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

def draw_instructions(mosaic_data, pixel_size=24):
    """Draw the building instructions and return as an image."""
    mosaic_size = len(mosaic_data)
    
    # Create a new image with white background
    img_width = mosaic_size * pixel_size
    img_height = mosaic_size * pixel_size
    image = Image.new('RGB', (img_width, img_height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Draw the mosaic with coordinate labels
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
            draw.rectangle([(x1, y1), (x2, y2)], fill=(r, g, b), outline=(0, 0, 0))
            
            # Add coordinate text (adjust text color for visibility)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            text_color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
            
            # Only add coordinates for smaller mosaics to avoid clutter
            if mosaic_size <= 32:
                coord_text = f"{y},{x}"
                # Get text size and center it in the cell
                text_width = 6 * len(coord_text)  # Approximation
                text_height = 10  # Approximation
                text_x = x1 + (pixel_size - text_width) // 2
                text_y = y1 + (pixel_size - text_height) // 2
                draw.text((text_x, text_y), coord_text, fill=text_color)
    
    return image

def get_image_download_link(img, filename, text):
    """Generate a download link for an image."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:image/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def main():
    st.title("🧱 LEGO Mosaic Creator")
    st.write("Transform your images into LEGO mosaic art")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload an image (square format works best)", type=["jpg", "jpeg", "png"])
    
    col1, col2 = st.columns([3, 1])
    
    # Variables to store mosaic data
    mosaic_data = None
    color_counts = None
    
    # If an image is uploaded
    if uploaded_file is not None:
        # Load the image
        image = Image.open(uploaded_file)
        
        # Display original image
        with col2:
            st.write("Original Image")
            st.image(image, width=150)
        
        # Mosaic settings
        with col1:
            st.write("### Mosaic Settings")
            
            # Select piece shape
            shape_options = ["Round 1x1 Plates", "Square 1x1 Plates"]
            shape_index = st.selectbox(
                "Select Piece Shape:",
                range(2),
                format_func=lambda i: shape_options[i]
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
                format_func=lambda i: size_options[i]
            )
            mosaic_size = BASEPLATE_SIZES[size_index]["size"]
            

            # Generate button
            if st.button("Generate LEGO Mosaic"):
                with st.spinner("Creating mosaic..."):
                    mosaic_data, color_counts = create_mosaic(image, mosaic_size, selected_lego_colors)
                    st.session_state.mosaic_data = mosaic_data
                    st.session_state.color_counts = color_counts
                    st.success("Mosaic created successfully!")
    else:
        # Demo image option
        if st.button("Load Demo Image"):
            # Create a simple demo image (a gradient)
            demo_img = Image.new('RGB', (300, 300), color='white')
            draw = ImageDraw.Draw(demo_img)
            
            # Draw a simple pattern
            for y in range(300):
                for x in range(300):
                    r = int(255 * x / 300)
                    g = int(255 * y / 300)
                    b = int(255 * (1 - (x + y) / 600))
                    draw.point((x, y), fill=(r, g, b))
            
            # Store in session state
            st.session_state.demo_img = demo_img
            
            # Display the demo image
            with col2:
                st.write("Demo Image")
                st.image(demo_img, width=150)
            
            # Mosaic settings for demo
            with col1:
                st.write("### Mosaic Settings")
                
                # Select mosaic size
                size_options = [s["name"] + f" ({s['size']}×{s['size']} studs)" for s in BASEPLATE_SIZES]
                size_index = st.selectbox(
                    "Select Mosaic Size:",
                    range(len(BASEPLATE_SIZES)),
                    format_func=lambda i: size_options[i]
                )
                mosaic_size = BASEPLATE_SIZES[size_index]["size"]
                
                # Generate button for demo
                if st.button("Generate Demo LEGO Mosaic"):
                    with st.spinner("Creating demo mosaic..."):
                        mosaic_data, color_counts = create_mosaic(st.session_state.demo_img, mosaic_size, selected_lego_colors)
                        st.session_state.mosaic_data = mosaic_data
                        st.session_state.color_counts = color_counts
                        st.success("Demo mosaic created successfully!")
    
    # Check if mosaic data exists in session state
    if hasattr(st.session_state, 'mosaic_data') and st.session_state.mosaic_data is not None:
        mosaic_data = st.session_state.mosaic_data
        color_counts = st.session_state.color_counts
    
    # If mosaic data is available
    if mosaic_data:
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Mosaic Preview", "Building Instructions", "Shopping List"])
        
        # Tab 1: Mosaic Preview
        with tab1:
            st.write("### Mosaic Preview")
            pixel_size = st.slider("Zoom Level:", min_value=5, max_value=20, value=10)
            
            # Draw mosaic preview
            mosaic_img = draw_mosaic(mosaic_data, pixel_size)
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
            
            # Draw instructions
            instructions_img = draw_instructions(mosaic_data)
            st.image(instructions_img)
            
            # Download link
            st.markdown(
                get_image_download_link(instructions_img, "lego_instructions.png", "Download Instructions"),
                unsafe_allow_html=True
            )
            
            # Color legend
            st.write("### Color Legend:")
            legend_cols = st.columns(4)
            lego_colors_used = st.session_state.get("selected_lego_colors", LEGO_COLORS_ALL)

            for i, (color_name, count) in enumerate(color_counts.items()):
                color_info = next((c for c in lego_colors_used if c[0] == color_name), None)
                with legend_cols[i % 4]:
                    st.markdown(
                        f'<div style="display: flex; align-items: center; margin-bottom: 10px;">'
                        f'<div style="width: 20px; height: 20px; background-color: {color_info[1]}; margin-right: 10px; border: 1px solid black;"></div>'
                        f'<span>{color_name}</span>'
                        f'</div>',
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

if __name__ == "__main__":
    main()