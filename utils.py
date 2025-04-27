import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
import io
import math
import base64
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def find_closest_lego_color(r, g, b, lego_colors):
    """Find the closest LEGO color to the given RGB values with error handling."""
    if lego_colors is None or len(lego_colors) == 0:
        # Fallback to a default color if no colors are available
        return ["Black", "#05131D", 5, 19, 29]
        
    # Ensure inputs are numeric
    try:
        r, g, b = float(r), float(g), float(b)
    except (ValueError, TypeError):
        # If conversion fails, use default values
        r, g, b = 0, 0, 0
        
    min_distance = float('inf')
    closest_color = lego_colors[0]  # Default to first color
    
    for color in lego_colors:
        try:
            name, hex_color, cr, cg, cb = color
            # Ensure color values are numeric
            cr, cg, cb = float(cr), float(cg), float(cb)
            distance = math.sqrt((r - cr) ** 2 + (g - cg) ** 2 + (b - cb) ** 2)
            
            if distance < min_distance:
                min_distance = distance
                closest_color = color
        except (ValueError, TypeError, IndexError):
            # Skip this color if there's an error
            continue
            
    return closest_color

def create_mosaic(image, mosaic_size, lego_colors):
    """Create a LEGO mosaic from an image with robust error handling."""
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
        
        # Validate lego_colors is properly loaded
        if lego_colors is None or len(lego_colors) == 0:
            st.error("LEGO colors not loaded properly")
            # Use a fallback color palette if needed
            lego_colors = [
                ["Black", "#05131D", 5, 19, 29],
                ["White", "#FFFFFF", 255, 255, 255],
                ["Red", "#C91A09", 201, 26, 9],
                ["Blue", "#0055BF", 0, 85, 191],
                ["Green", "#237841", 35, 120, 65]
            ]
            
        # Create the mosaic
        mosaic_data = []
        color_counts = {}
        
        # Verify pixel_data dimensions
        if pixel_data.shape[0] != mosaic_size or pixel_data.shape[1] != mosaic_size:
            st.warning(f"Resized image dimensions don't match requested size: {pixel_data.shape}")
            # Resize again or handle the issue
        
        # Process each row and column with bounds checking
        for y in range(min(mosaic_size, pixel_data.shape[0])):
            row = []
            for x in range(min(mosaic_size, pixel_data.shape[1])):
                # Get pixel color with bounds checking
                try:
                    r, g, b = pixel_data[y, x]
                except (IndexError, ValueError):
                    r, g, b = 0, 0, 0  # Default to black if error
                    
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
            draw.rectangle([(x1, y1), (x2, y2)], fill=(r, g, b))
    
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



def save_feedback_to_google_sheets(rating, comment):
    # Path to your service account key JSON file
    creds_path = "your-service-account-credentials.json"
    
    # Connect to Google Sheets
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    
    # Open the sheet (by name or by URL)
    sheet = client.open("lego_feedback").sheet1  # Assuming first sheet
    
    # Prepare feedback data
    timestamp = datetime.now().isoformat()
    rating = rating if rating else ""
    comment = comment if comment else ""
    
    # Append the feedback as a new row
    sheet.append_row([timestamp, rating, comment])
