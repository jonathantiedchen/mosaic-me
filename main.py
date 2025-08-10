import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from lego_colors import LEGO_COLORS_ALL
from lego_colors_round import LEGO_COLORS_ROUND
from lego_colors_square import LEGO_COLORS_SQUARE
from lego_colors_square_available import LEGO_COLORS_SQUARE_AVAILABLE
from lego_colors_round_available import LEGO_COLORS_ROUND_AVAILABLE
from utils import *

shape_index = st.session_state.get('shape_index', 0)  # default to 0 (square)
selected_lego_colors = st.session_state.get('selected_lego_colors', LEGO_COLORS_ALL)

# Standard baseplate sizes
BASEPLATE_SIZES = [
    {"name": "32×32 (standard)", "size": 32},
    {"name": "48×48 (standard)", "size": 48},
    {"name": "64×64", "size": 64},
    {"name": "96×96", "size": 96},
    {"name": "128×128", "size": 128},
]

def main():
    st.set_page_config(
        page_title="LEGO Mosaic Creator",
        page_icon="🧱",
        layout="wide"
    )
    
    st.title("🧱 LEGO Mosaic Creator")
    st.write("""
    Hello there! 👋 With this small application you can transform your images into LEGO-style mosaic art.

    Here’s what the app does for you:
    - 📷 Import an image from your device (square format works best)
    - 🧱 Choose the LEGO brick type (round, square, or all colors) and mosaic size
    - 👀 Get a real-time preview of your mosaic
    - 🏗️ Download easy-to-follow building instructions
    - 🛒 Get a shopping list with the exact LEGO pieces you need
    - 🔒 No data is saved — just image in, image out. 100% privacy!

    Awesome, right?!  
    Enjoy the app my friend — and happy building! 🚀
    """)
    st.write("## ")
    st.write("## Create Your Mosaic Here")
    st.write("Please note that you should upload a square image.")

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
                shape_options = ["Square 1x1 Plates (LEGO Colors)", "Round 1x1 Plates (LEGO Colors)"]
                shape_index = st.selectbox(
                    "Select Piece Shape:",
                    range(len(shape_options)),
                    format_func=lambda i: shape_options[i],
                    key="user_shape_selector"
                )
                st.session_state['shape_index'] = int(shape_index)
                
                if shape_index == 0:
                    selected_lego_colors = LEGO_COLORS_SQUARE_AVAILABLE
                elif shape_index == 1:
                    selected_lego_colors = LEGO_COLORS_ROUND_AVAILABLE
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
                                st.success("Mosaic created successfully!")
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
                shape_options = ["Square 1x1 Plates (LEGO Colors)", "Round 1x1 Plates (LEGO Colors)"]
                shape_index = st.selectbox(
                    "Select Piece Shape:",
                    range(len(shape_options)),
                    format_func=lambda i: shape_options[i],
                    key="demo_shape_selector"
                )
                st.session_state['shape_index'] = int(shape_index)
                
                if shape_index == 0:
                    selected_lego_colors = LEGO_COLORS_SQUARE_AVAILABLE
                elif shape_index == 1:
                    selected_lego_colors = LEGO_COLORS_ROUND_AVAILABLE
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
                    with st.spinner("Creating demo mosaic...(that might take some seconds)"):
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
        st.write("### ")
        st.write("### Results")
        try:
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["Mosaic Preview", "Building Instructions", "Shopping List"])
            
            # Tab 1: Mosaic Preview
            with tab1:
                st.write("#### Mosaic Preview")
                pixel_size = st.slider("Zoom Level:", min_value=5, max_value=20, value=10)

                if shape_index == 0:
                    mosaic_img = draw_mosaic(mosaic_data, pixel_size)
                elif shape_index == 1: 
                    mosaic_img = draw_mosaic_with_dots(mosaic_data, pixel_size)
                else: 
                    mosaic_img = draw_mosaic(mosaic_data, pixel_size)

                if mosaic_img:
                    st.image(mosaic_img)

                    # Add mosaic download tracking
                    if st.download_button(
                        label="Download Mosaic Image",
                        data=instructions_img_to_bytes(mosaic_img),
                        file_name="lego_mosaic.png",
                        mime="image/png",
                    ):
                        try:
                            save_mosaic_download_to_google_sheets()
                        except Exception as e:
                            st.warning(f"Error logging mosaic image download: {str(e)}")

            
            # Tab 2: Building Instructions
            with tab2:
                st.write("#### Building Instructions")
                st.write("Follow the color-coded grid below to build your mosaic:")

                # Draw instructions with color legend
                lego_colors_used = st.session_state.get("selected_lego_colors", LEGO_COLORS_ALL)
                instructions_img = draw_instructions(mosaic_data, color_counts=color_counts, lego_colors_used=lego_colors_used)
                
                if instructions_img:
                    st.image(instructions_img)

                    # Track the instruction download event
                    if st.download_button(
                        label="Download Instructions with Color Legend",
                        data=instructions_img_to_bytes(instructions_img),
                        file_name="lego_instructions.png",
                        mime="image/png",
                    ):
                        try:
                            save_instruction_download_to_google_sheets()
                        except Exception as e:
                            st.warning(f"Error logging instruction download: {str(e)}")

            # Tab 3: Shopping List
            with tab3:
                st.write("#### Shopping List")
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

                st.write(f"**Total Pieces:** {sum(color_counts.values())}")

                # Export and track CSV download
                csv = shopping_df[["Color Name", "Quantity"]].to_csv(index=False)
                if st.download_button(
                    label="Download Shopping List (CSV)",
                    data=csv,
                    file_name="lego_shopping_list.csv",
                    mime="text/csv",
                ):
                    try:
                        save_shopping_list_download_to_google_sheets()
                    except Exception as e:
                        st.warning(f"Error logging shopping list download: {str(e)}")
                
        except Exception as e:
            st.error(f"Error rendering mosaic: {str(e)}")

    
    #### EXAMPLES
    st.divider()
    # Display example images side-by-side
    example1 = Image.open("example1.png")  # or .jpg, depending on your file
    example2 = Image.open("example2.png")

    st.write("### Example Mosaics")
    
    spacer1, col1, spacer2, col2, spacer3 = st.columns([1, 3, 0.5, 3, 1])
    
    with col1:
        st.image(example1, caption="Example 1", use_container_width=True)

    with col2:
        st.image(example2, caption="Example 2", use_container_width=True)


    ### FEEDBACK
    st.divider()
    st.write("Did you enjoy using the LEGO Mosaic Creator? 🎨🧱")
    feedback = st.feedback(
        "thumbs",
        key="lego_mosaic_feedback"
    )
    comment = st.text_area(
        label="Tell me what you built, or any feedback you have! 🧱🎨",
        placeholder="I built a mosaic of my dog!",
        key="lego_mosaic_comment"
    )

    if feedback:
        try:
            rating = "thumbs_up" if feedback == 1 else "thumbs_down"
            save_feedback_to_google_sheets(rating, comment)            
            st.success("Thank you for your feedback! 🙏 (It has been saved)")
        except Exception as e:
            st.error(f"An error occurred while saving your feedback: {str(e)}")

if __name__ == "__main__":
    main()