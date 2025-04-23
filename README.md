# mosaic-me
## A LEGO Mosaic Creator

Transform your images into LEGO mosaic art with this Streamlit application. Upload any image and convert it into a detailed LEGO mosaic with building instructions and a shopping list.

## Features

- **Image Transformation**: Convert any image to a LEGO mosaic
- **Multiple Baseplate Sizes**: Choose from 16×16, 32×32, 48×48, or 64×64 studs
- **LEGO Piece Options**: Use Round 1×1 Plates, Square 1×1 Plates, or all LEGO colors
- **Building Instructions**: Get color-coded grid with numbered legend
- **Shopping List**: Export a detailed list of LEGO pieces needed

## Demo

Try the app with a demo image to see how it works before uploading your own images.

## Installation

### Local Development

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/lego-mosaic-creator.git
   cd lego-mosaic-creator
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run lego_mosaic_creator.py
   ```

## Project Structure

- `lego_mosaic_creator.py`: Main Streamlit application
- `utils.py`: Utility functions for creating and rendering mosaics
- `lego_colors.py`: Complete LEGO color palette
- `lego_colors_round.py`: Color palette for Round 1×1 Plates
- `lego_colors_square.py`: Color palette for Square 1×1 Plates
- `requirements.txt`: Required Python packages

## Deployment Notes

When deploying this application, ensure:

1. All color palette files (`lego_colors.py`, `lego_colors_round.py`, `lego_colors_square.py`) are included
2. The application has read/write access to handle uploaded images
3. All dependencies from `requirements.txt` are installed


## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue.

## Acknowledgments

- The LEGO® Group for inspiration (LEGO® is a trademark of the LEGO Group)

