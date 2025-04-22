import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import io
import math
import base64
LEGO_COLORS_ROUND = [
    ["Black", "#05131D", 5, 19, 29],
    ["Blue", "#0055BF", 0, 85, 191],
    ["Green", "#237841", 35, 120, 65],
    ["Dark Turquoise", "#008F9B", 0, 143, 155],
    ["Red", "#C91A09", 201, 26, 9],
    ["Dark Pink", "#C870A0", 200, 112, 160],
    ["Brown", "#583927", 88, 57, 39],
    ["Light Gray", "#9BA19D", 155, 161, 157],
    ["Dark Gray", "#6D6E5C", 109, 110, 92],
    ["Bright Green", "#4B9F4A", 75, 159, 74],
    ["Yellow", "#F2CD37", 242, 205, 55],
    ["White", "#FFFFFF", 255, 255, 255],
    ["Tan", "#E4CD9E", 228, 205, 158],
    ["Orange", "#FE8A18", 254, 138, 24],
    ["Magenta", "#923978", 146, 57, 120],
    ["Lime", "#BBE90B", 187, 233, 11],
    ["Dark Tan", "#958A73", 149, 138, 115],
    ["Bright Pink", "#E4ADC8", 228, 173, 200],
    ["Medium Lavender", "#AC78BA", 172, 120, 186],
    ["Reddish Brown", "#582A12", 88, 42, 18],
    ["Light Bluish Gray", "#A0A5A9", 160, 165, 169],
    ["Dark Bluish Gray", "#6C6E68", 108, 110, 104],
    ["Medium Nougat", "#AA7D55", 170, 125, 85],
    ["Dark Purple", "#3F3691", 63, 54, 145],
    ["Nougat", "#D09168", 208, 145, 104],
    ["Yellowish Green", "#DFEEA5", 223, 238, 165],
    ["Bright Light Orange", "#F8BB3D", 248, 187, 61],
    ["Bright Light Yellow", "#FFF03A", 255, 240, 58],
    ["Dark Blue", "#0A3463", 10, 52, 99],
    ["Dark Brown", "#352100", 53, 33, 0],
    ["Dark Red", "#720E0F", 114, 14, 15],
    ["Medium Azure", "#36AEBF", 54, 174, 191],
    ["Light Aqua", "#ADC3C0", 173, 195, 192],
    ["Olive Green", "#9B9A5A", 155, 154, 90],
    ["Sand Green", "#A0BCAC", 160, 188, 172],
    ["Sand Blue", "#6074A1", 96, 116, 161],
    ["Dark Orange", "#A95500", 169, 85, 0],
]

LEGO_COLORS_SQUARE = [
    ["Black", "#05131D", 5, 19, 29],
    ["Blue", "#0055BF", 0, 85, 191],
    ["Green", "#237841", 35, 120, 65],
    ["Dark Turquoise", "#008F9B", 0, 143, 155],
    ["Red", "#C91A09", 201, 26, 9],
    ["Dark Pink", "#C870A0", 200, 112, 160],
    ["Brown", "#583927", 88, 57, 39],
    ["Light Gray", "#9BA19D", 155, 161, 157],
    ["Dark Gray", "#6D6E5C", 109, 110, 92],
    ["Bright Green", "#4B9F4A", 75, 159, 74],
    ["Pink", "#FC97AC", 252, 151, 172],
    ["Yellow", "#F2CD37", 242, 205, 55],
    ["White", "#FFFFFF", 255, 255, 255],
    ["Tan", "#E4CD9E", 228, 205, 158],
    ["Orange", "#FE8A18", 254, 138, 24],
    ["Magenta", "#923978", 146, 57, 120],
    ["Lime", "#BBE90B", 187, 233, 11],
    ["Dark Tan", "#958A73", 149, 138, 115],
    ["Bright Pink", "#E4ADC8", 228, 173, 200],
    ["Medium Lavender", "#AC78BA", 172, 120, 186],
    ["Lavender", "#E1D5ED", 225, 213, 237],
    ["Reddish Brown", "#582A12", 88, 42, 18],
    ["Light Bluish Gray", "#A0A5A9", 160, 165, 169],
    ["Dark Bluish Gray", "#6C6E68", 108, 110, 104],
    ["Medium Blue", "#5A93DB", 90, 147, 219],
    ["Light Nougat", "#F6D7B3", 246, 215, 179],
    ["Medium Nougat", "#AA7D55", 170, 125, 85],
    ["Dark Purple", "#3F3691", 63, 54, 145],
    ["Nougat", "#D09168", 208, 145, 104],
    ["Yellowish Green", "#DFEEA5", 223, 238, 165],
    ["Bright Light Orange", "#F8BB3D", 248, 187, 61],
    ["Bright Light Blue", "#9FC3E9", 159, 195, 233],
    ["Bright Light Yellow", "#FFF03A", 255, 240, 58],
    ["Dark Blue", "#0A3463", 10, 52, 99],
    ["Dark Green", "#184632", 24, 70, 50],
    ["Dark Brown", "#352100", 53, 33, 0],
    ["Dark Red", "#720E0F", 114, 14, 15],
    ["Dark Azure", "#078BC9", 7, 139, 201],
    ["Medium Azure", "#36AEBF", 54, 174, 191],
    ["Light Aqua", "#ADC3C0", 173, 195, 192],
    ["Olive Green", "#9B9A5A", 155, 154, 90],
    ["Sand Green", "#A0BCAC", 160, 188, 172],
    ["Sand Blue", "#6074A1", 96, 116, 161],
    ["Medium Orange", "#FFA70B", 255, 167, 11],
    ["Dark Orange", "#A95500", 169, 85, 0],
    ["Very Light Gray", "#E6E3DA", 230, 227, 218],
    ["Coral", "#FF698F", 255, 105, 143],
    ["Reddish Orange", "#CA4C0B", 202, 76, 11],
]

LEGO_COLORS_ALL = [
    ["[Unknown]", "#0033B2", 0, 51, 178],
    ["Black", "#05131D", 5, 19, 29],
    ["Blue", "#0055BF", 0, 85, 191],
    ["Green", "#237841", 35, 120, 65],
    ["Dark Turquoise", "#008F9B", 0, 143, 155],
    ["Red", "#C91A09", 201, 26, 9],
    ["Dark Pink", "#C870A0", 200, 112, 160],
    ["Brown", "#583927", 88, 57, 39],
    ["Light Gray", "#9BA19D", 155, 161, 157],
    ["Dark Gray", "#6D6E5C", 109, 110, 92],
    ["Light Blue", "#B4D2E3", 180, 210, 227],
    ["Bright Green", "#4B9F4A", 75, 159, 74],
    ["Light Turquoise", "#55A5AF", 85, 165, 175],
    ["Salmon", "#F2705E", 242, 112, 94],
    ["Pink", "#FC97AC", 252, 151, 172],
    ["Yellow", "#F2CD37", 242, 205, 55],
    ["White", "#FFFFFF", 255, 255, 255],
    ["Light Green", "#C2DAB8", 194, 218, 184],
    ["Light Yellow", "#FBE696", 251, 230, 150],
    ["Tan", "#E4CD9E", 228, 205, 158],
    ["Light Violet", "#C9CAE2", 201, 202, 226],
    ["Glow In Dark Opaque", "#D4D5C9", 212, 213, 201],
    ["Purple", "#81007B", 129, 0, 123],
    ["Dark Blue-Violet", "#2032B0", 32, 50, 176],
    ["Orange", "#FE8A18", 254, 138, 24],
    ["Magenta", "#923978", 146, 57, 120],
    ["Lime", "#BBE90B", 187, 233, 11],
    ["Dark Tan", "#958A73", 149, 138, 115],
    ["Bright Pink", "#E4ADC8", 228, 173, 200],
    ["Medium Lavender", "#AC78BA", 172, 120, 186],
    ["Lavender", "#E1D5ED", 225, 213, 237],
    ["Chrome Antique Brass", "#645A4C", 100, 90, 76],
    ["Chrome Blue", "#6C96BF", 108, 150, 191],
    ["Chrome Green", "#3CB371", 60, 179, 113],
    ["Chrome Pink", "#AA4D8E", 170, 77, 142],
    ["Chrome Black", "#1B2A34", 27, 42, 52],
    ["Very Light Orange", "#F3CF9B", 243, 207, 155],
    ["Light Purple", "#CD6298", 205, 98, 152],
    ["Reddish Brown", "#582A12", 88, 42, 18],
    ["Light Bluish Gray", "#A0A5A9", 160, 165, 169],
    ["Dark Bluish Gray", "#6C6E68", 108, 110, 104],
    ["Medium Blue", "#5A93DB", 90, 147, 219],
    ["Medium Green", "#73DCA1", 115, 220, 161],
    ["Speckle Black-Copper", "#05131D", 5, 19, 29],
    ["Speckle DBGray-Silver", "#6C6E68", 108, 110, 104],
    ["Light Pink", "#FECCCF", 254, 204, 207],
    ["Light Nougat", "#F6D7B3", 246, 215, 179],
    ["Milky White", "#FFFFFF", 255, 255, 255],
    ["Metallic Silver", "#A5A9B4", 165, 169, 180],
    ["Metallic Green", "#899B5F", 137, 155, 95],
    ["Metallic Gold", "#DBAC34", 219, 172, 52],
    ["Medium Nougat", "#AA7D55", 170, 125, 85],
    ["Dark Purple", "#3F3691", 63, 54, 145],
    ["Light Brown", "#7C503A", 124, 80, 58],
    ["Royal Blue", "#4C61DB", 76, 97, 219],
    ["Nougat", "#D09168", 208, 145, 104],
    ["Light Salmon", "#FEBABD", 254, 186, 189],
    ["Violet", "#4354A3", 67, 84, 163],
    ["Medium Bluish Violet", "#6874CA", 104, 116, 202],
    ["Medium Lime", "#C7D23C", 199, 210, 60],
    ["Aqua", "#B3D7D1", 179, 215, 209],
    ["Light Lime", "#D9E4A7", 217, 228, 167],
    ["Light Orange", "#F9BA61", 249, 186, 97],
    ["Speckle Black-Silver", "#05131D", 5, 19, 29],
    ["Speckle Black-Gold", "#05131D", 5, 19, 29],
    ["Copper", "#AE7A59", 174, 122, 89],
    ["Pearl Light Gray", "#9CA3A8", 156, 163, 168],
    ["Pearl Sand Blue", "#7988A1", 121, 136, 161],
    ["Pearl Light Gold", "#DCBC81", 220, 188, 129],
    ["Pearl Dark Gray", "#575857", 87, 88, 87],
    ["Pearl Very Light Gray", "#ABADAC", 171, 173, 172],
    ["Very Light Bluish Gray", "#E6E3E0", 230, 227, 224],
    ["Yellowish Green", "#DFEEA5", 223, 238, 165],
    ["Flat Dark Gold", "#B48455", 180, 132, 85],
    ["Flat Silver", "#898788", 137, 135, 136],
    ["Pearl White", "#F2F3F2", 242, 243, 242],
    ["Bright Light Orange", "#F8BB3D", 248, 187, 61],
    ["Bright Light Blue", "#9FC3E9", 159, 195, 233],
    ["Rust", "#B31004", 179, 16, 4],
    ["Bright Light Yellow", "#FFF03A", 255, 240, 58],
    ["Sky Blue", "#7DBFDD", 125, 191, 221],
    ["Dark Blue", "#0A3463", 10, 52, 99],
    ["Dark Green", "#184632", 24, 70, 50],
    ["Pearl Gold", "#AA7F2E", 170, 127, 46],
    ["Dark Brown", "#352100", 53, 33, 0],
    ["Maersk Blue", "#3592C3", 53, 146, 195],
    ["Dark Red", "#720E0F", 114, 14, 15],
    ["Dark Azure", "#078BC9", 7, 139, 201],
    ["Medium Azure", "#36AEBF", 54, 174, 191],
    ["Light Aqua", "#ADC3C0", 173, 195, 192],
    ["Olive Green", "#9B9A5A", 155, 154, 90],
    ["Chrome Gold", "#BBA53D", 187, 165, 61],
    ["Sand Red", "#D67572", 214, 117, 114],
    ["Medium Dark Pink", "#F785B1", 247, 133, 177],
    ["Earth Orange", "#FA9C1C", 250, 156, 28],
    ["Sand Purple", "#845E84", 132, 94, 132],
    ["Sand Green", "#A0BCAC", 160, 188, 172],
    ["Sand Blue", "#6074A1", 96, 116, 161],
    ["Chrome Silver", "#E0E0E0", 224, 224, 224],
    ["Fabuland Brown", "#B67B50", 182, 123, 80],
    ["Medium Orange", "#FFA70B", 255, 167, 11],
    ["Dark Orange", "#A95500", 169, 85, 0],
    ["Very Light Gray", "#E6E3DA", 230, 227, 218],
    ["Glow in Dark White", "#D9D9D9", 217, 217, 217],
    ["Medium Violet", "#9391E4", 147, 145, 228],
    ["Reddish Lilac", "#8E5597", 142, 85, 151],
    ["Vintage Blue", "#039CBD", 3, 156, 189],
    ["Vintage Green", "#1E601E", 30, 96, 30],
    ["Vintage Red", "#CA1F08", 202, 31, 8],
    ["Vintage Yellow", "#F3C305", 243, 195, 5],
    ["Fabuland Orange", "#EF9121", 239, 145, 33],
    ["Modulex White", "#F4F4F4", 244, 244, 244],
    ["Modulex Light Bluish Gray", "#AfB5C7", 175, 181, 199],
    ["Modulex Light Gray", "#9C9C9C", 156, 156, 156],
    ["Modulex Charcoal Gray", "#595D60", 89, 93, 96],
    ["Modulex Tile Gray", "#6B5A5A", 107, 90, 90],
    ["Modulex Black", "#4D4C52", 77, 76, 82],
    ["Modulex Tile Brown", "#330000", 51, 0, 0],
    ["Modulex Terracotta", "#5C5030", 92, 80, 48],
    ["Modulex Brown", "#907450", 144, 116, 80],
    ["Modulex Buff", "#DEC69C", 222, 198, 156],
    ["Modulex Red", "#B52C20", 181, 44, 32],
    ["Modulex Pink Red", "#F45C40", 244, 92, 64],
    ["Modulex Orange", "#F47B30", 244, 123, 48],
    ["Modulex Light Orange", "#F7AD63", 247, 173, 99],
    ["Modulex Light Yellow", "#FFE371", 255, 227, 113],
    ["Modulex Ochre Yellow", "#FED557", 254, 213, 87],
    ["Modulex Lemon", "#BDC618", 189, 198, 24],
    ["Modulex Pastel Green", "#7DB538", 125, 181, 56],
    ["Modulex Olive Green", "#7C9051", 124, 144, 81],
    ["Modulex Aqua Green", "#27867E", 39, 134, 126],
    ["Modulex Teal Blue", "#467083", 70, 112, 131],
    ["Modulex Tile Blue", "#0057A6", 0, 87, 166],
    ["Modulex Medium Blue", "#61AFFF", 97, 175, 255],
    ["Modulex Pastel Blue", "#68AECE", 104, 174, 206],
    ["Modulex Violet", "#BD7D85", 189, 125, 133],
    ["Modulex Pink", "#F785B1", 247, 133, 177],
    ["Modulex Clear", "#FFFFFF", 255, 255, 255],
    ["Modulex Foil Dark Gray", "#595D60", 89, 93, 96],
    ["Modulex Foil Light Gray", "#9C9C9C", 156, 156, 156],
    ["Modulex Foil Dark Green", "#006400", 0, 100, 0],
    ["Modulex Foil Light Green", "#7DB538", 125, 181, 56],
    ["Modulex Foil Dark Blue", "#0057A6", 0, 87, 166],
    ["Modulex Foil Light Blue", "#68AECE", 104, 174, 206],
    ["Modulex Foil Violet", "#4B0082", 75, 0, 130],
    ["Modulex Foil Red", "#8B0000", 139, 0, 0],
    ["Modulex Foil Yellow", "#FED557", 254, 213, 87],
    ["Modulex Foil Orange", "#F7AD63", 247, 173, 99],
    ["Coral", "#FF698F", 255, 105, 143],
    ["Pastel Blue", "#5AC4DA", 90, 196, 218],
    ["Vibrant Yellow", "#EBD800", 235, 216, 0],
    ["Pearl Copper", "#B46A00", 180, 106, 0],
    ["Fabuland Red", "#FF8014", 255, 128, 20],
    ["Reddish Gold", "#AC8247", 172, 130, 71],
    ["Curry", "#DD982E", 221, 152, 46],
    ["Dark Nougat", "#AD6140", 173, 97, 64],
    ["Bright Reddish Orange", "#EE5434", 238, 84, 52],
    ["Pearl Red", "#D60026", 214, 0, 38],
    ["Pearl Blue", "#0059A3", 0, 89, 163],
    ["Pearl Green", "#008E3C", 0, 142, 60],
    ["Pearl Brown", "#57392C", 87, 57, 44],
    ["Pearl Black", "#0A1327", 10, 19, 39],
    ["Duplo Blue", "#009ECE", 0, 158, 206],
    ["Duplo Medium Blue", "#3E95B6", 62, 149, 182],
    ["Duplo Lime", "#FFF230", 255, 242, 48],
    ["Fabuland Lime", "#78FC78", 120, 252, 120],
    ["Duplo Medium Green", "#468A5F", 70, 138, 95],
    ["Duplo Light Green", "#60BA76", 96, 186, 118],
    ["Light Tan", "#F3C988", 243, 201, 136],
    ["Rust Orange", "#872B17", 135, 43, 23],
    ["Clikits Pink", "#FE78B0", 254, 120, 176],
    ["Two-tone Copper", "#945148", 148, 81, 72],
    ["Two-tone Gold", "#AB673A", 171, 103, 58],
    ["Two-tone Silver", "#737271", 115, 114, 113],
    ["Pearl Lime", "#6A7944", 106, 121, 68],
    ["Duplo Pink", "#FF879C", 255, 135, 156],
    ["Medium Brown", "#755945", 117, 89, 69],
    ["Warm Tan", "#CCA373", 204, 163, 115],
    ["Duplo Turquoise", "#3FB69E", 63, 182, 158],
    ["Warm Yellowish Orange", "#FFCB78", 255, 203, 120],
    ["Metallic Copper", "#764D3B", 118, 77, 59],
    ["Light Lilac", "#9195CA", 145, 149, 202],
    ["Trans-Medium Purple", "#8D73B3", 141, 115, 179],
    ["Clikits Yellow", "#FFCF0B", 255, 207, 11],
    ["Duplo Dark Purple", "#5F27AA", 95, 39, 170],
    ["Pearl Titanium", "#3E3C39", 62, 60, 57],
    ["HO Aqua", "#B3D7D1", 179, 215, 209],
    ["HO Azure", "#1591cb", 21, 145, 203],
    ["HO Blue-gray", "#354e5a", 53, 78, 90],
    ["HO Cyan", "#5b98b3", 91, 152, 179],
    ["HO Dark Aqua", "#a7dccf", 167, 220, 207],
    ["HO Dark Blue", "#0A3463", 10, 52, 99],
    ["HO Dark Gray", "#6D6E5C", 109, 110, 92],
    ["HO Dark Green", "#184632", 24, 70, 50],
    ["HO Dark Lime", "#b2b955", 178, 185, 85],
    ["HO Dark Red", "#631314", 99, 19, 20],
    ["HO Dark Sand Green", "#627a62", 98, 122, 98],
    ["HO Dark Turquoise", "#10929d", 16, 146, 157],
    ["HO Earth Orange", "#bb771b", 187, 119, 27],
    ["HO Gold", "#b4a774", 180, 167, 116],
    ["HO Light Aqua", "#a3d1c0", 163, 209, 192],
    ["HO Light Brown", "#965336", 150, 83, 54],
    ["HO Light Gold", "#cdc298", 205, 194, 152],
    ["HO Light Tan", "#f9f1c7", 249, 241, 199],
    ["HO Light Yellow", "#f5fab7", 245, 250, 183],
    ["HO Medium Blue", "#7396c8", 115, 150, 200],
    ["HO Medium Red", "#c01111", 192, 17, 17],
    ["HO Metallic Blue", "#0d4763", 13, 71, 99],
    ["HO Metallic Dark Gray", "#5e5e5e", 94, 94, 94],
    ["HO Metallic Green", "#879867", 135, 152, 103],
    ["HO Metallic Sand Blue", "#5f7d8c", 95, 125, 140],
    ["HO Olive Green", "#9B9A5A", 155, 154, 90],
    ["HO Rose", "#d06262", 208, 98, 98],
    ["HO Sand Blue", "#6e8aa6", 110, 138, 166],
    ["HO Sand Green", "#A0BCAC", 160, 188, 172],
    ["HO Tan", "#E4CD9E", 228, 205, 158],
    ["HO Titanium", "#616161", 97, 97, 97],
    ["Metal", "#A5ADB4", 165, 173, 180],
    ["Reddish Orange", "#CA4C0B", 202, 76, 11],
    ["Sienna Brown", "#915C3C", 145, 92, 60],
    ["Umber Brown", "#5E3F33", 94, 63, 51],
    ["Neon Orange", "#EC4612", 236, 70, 18],
    ["Neon Green", "#D2FC43", 210, 252, 67],
    ["Dark Olive Green", "#5d5c36", 93, 92, 54],
    ["Glitter Milky White", "#FFFFFF", 255, 255, 255],
    ["Chrome Red", "#CE3021", 206, 48, 33],
    ["[No Color/Any Color]", "#05131D", 5, 19, 29],
]


# Set page configuration
st.set_page_config(
    page_title="LEGO Mosaic Creator",
    page_icon="🧱",
    layout="wide"
)

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
    try:
        img_resized = image.resize((mosaic_size, mosaic_size), Image.Resampling.LANCZOS)
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
    except Exception as e:
        st.error(f"Error creating mosaic: {e}")
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
    st.title("🧱 LEGO Mosaic Creator")
    st.write("Transform your images into LEGO mosaic art")
    
    # Initialize session state variables
    if 'selected_lego_colors' not in st.session_state:
        st.session_state.selected_lego_colors = LEGO_COLORS_SQUARE
    if 'demo_mode' not in st.session_state:
        st.session_state.demo_mode = False
    if 'mosaic_created' not in st.session_state:
        st.session_state.mosaic_created = False
    
    col1, col2 = st.columns([3, 1])
    
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
    if not st.session_state.demo_mode and 'uploaded_file' in locals() and uploaded_file is not None:
        try:
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
                                st.success("Mosaic created successfully!")
                        except Exception as e:
                            st.error(f"Error creating mosaic: {str(e)}")
        except Exception as e:
            st.error(f"Error loading image: {str(e)}")
    
    # Demo mode section
    elif st.session_state.demo_mode:
        try:
            # Try to load the demo image file
            demo_path = "demo_image.jpeg"
            try:
                demo_img = Image.open(demo_path)
                st.success(f"Successfully loaded demo image from {demo_path}")
            except (FileNotFoundError, IOError):
                # If file not found or can't be opened, create a simple gradient image
                st.warning(f"Demo image file '{demo_path}' not found or couldn't be opened. Creating a simple gradient image instead.")
                demo_img = Image.new('RGB', (300, 300), color='white')
                draw = ImageDraw.Draw(demo_img)
                
                # Draw a simple pattern
                for y in range(300):
                    for x in range(300):
                        r = int(255 * x / 300)
                        g = int(255 * y / 300)
                        b = int(255 * (1 - (x + y) / 600))
                        draw.point((x, y), fill=(r, g, b))
            
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
                                st.success("Demo mosaic created successfully!")
                        except Exception as e:
                            st.error(f"Error creating demo mosaic: {str(e)}")
        except Exception as e:
            st.error(f"Error with demo image: {str(e)}")
    
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
                
                # Color legend
                st.write("### Color Legend:")
                legend_cols = st.columns(4)
                lego_colors_used = st.session_state.get("selected_lego_colors", LEGO_COLORS_ALL)

                for i, (color_name, count) in enumerate(color_counts.items()):
                    color_info = next((c for c in lego_colors_used if c[0] == color_name), None)
                    if color_info:
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