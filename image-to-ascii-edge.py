import sys
import numpy as np
from PIL import Image, ImageFilter
import math

def image_to_ascii_with_edges(image_path, max_chars=1000):
    """
    Convert an image to ASCII art with edge detection for better shape preservation.
    
    Args:
        image_path (str): Path to the input image
        max_chars (int): Maximum total characters to use in the ASCII art
        
    Returns:
        str: ASCII art representation
    """
    # ASCII characters from high edge intensity to low
    # We use characters with different visual weights to represent edges
    ascii_chars = ' .:-=+*#%@'
    
    try:
        # Open image
        img = Image.open(image_path).convert('L')  # Convert to grayscale
        
        # Calculate appropriate width and height based on image aspect ratio
        orig_width, orig_height = img.size
        aspect_ratio = orig_width / orig_height
        
        # Terminal characters are typically taller than wide
        # We need to make the ASCII art wider to compensate for this
        char_height_to_width_ratio = 2.5
        
        # Calculate dimensions that preserve the aspect ratio
        target_aspect = aspect_ratio * char_height_to_width_ratio
        
        # Calculate width and height to fit within max_chars
        # Use a different approach to determine dimensions
        height = int(math.sqrt(max_chars / target_aspect))
        width = int(height * target_aspect)
        
        # Ensure dimensions don't exceed max_chars
        while width * height > max_chars:
            height -= 1
            width = int(height * target_aspect)
            if height <= 0 or width <= 0:
                height = 1
                width = min(max_chars, int(target_aspect))
                break
        
        # Ensure minimum dimensions
        width = max(1, width)
        height = max(1, height)
        
        # Resize image to calculated dimensions
        img = img.resize((width, height))
        
        # Apply edge detection filter
        edge_img = img.filter(ImageFilter.FIND_EDGES)
        
        # Get edge data and original brightness data
        edge_data = np.array(list(edge_img.getdata()))
        brightness_data = np.array(list(img.getdata()))
        
        # Calculate edge strength scaling factor
        # Replace the percentile-based mask with continuous edge strength scaling
        edge_strength = edge_data / np.max(edge_data) if np.max(edge_data) > 0 else 0
        combined_data = np.clip(brightness_data - (edge_data * edge_strength)*0.4, 0, 255)
        
        # Convert to ASCII
        ascii_art = ''
        for i in range(height):
            for j in range(width):
                idx = i * width + j
                # Map combined value to ASCII character
                pixel_value = combined_data[idx]  # Use combined_data directly
                char_index = min(int(pixel_value * (len(ascii_chars) - 1) / 255), len(ascii_chars) - 1)
                ascii_art += ascii_chars[char_index]
            ascii_art += '\n'
            
        return ascii_art
    
    except Exception as e:
        return f"Error processing image: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ascii_art.py <image_path> [max_chars]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    max_chars = int(input("Enter the maximum number of characters: "))
    
    if len(sys.argv) > 2:
        try:
            max_chars = int(sys.argv[2])
        except ValueError:
            print("Error: max_chars must be an integer")
            sys.exit(1)
    
    ascii_result = image_to_ascii_with_edges(image_path, max_chars)
    print(ascii_result)
