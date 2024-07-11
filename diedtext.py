import sys
import os
import requests
import zipfile
import io
from PIL import Image, ImageDraw, ImageFont, ImageFilter


def download_and_install_font(font_url, font_name):
    # Create a fonts directory if it doesn't exist
    fonts_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    os.makedirs(fonts_dir, exist_ok=True)

    # Download the font
    response = requests.get(font_url)
    if response.status_code == 200:
        # Extract the zip file
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(fonts_dir)

        # Find the .ttf or .otf file
        for file in os.listdir(fonts_dir):
            if file.lower().endswith(('.ttf', '.otf')):
                return os.path.join(fonts_dir, file)

    print(f"Failed to download or extract font {font_name}")
    return None


def create_echo_text(draw, text, font, position, color, iterations=3, offset=3):
    for i in range(iterations, 0, -1):
        alpha = int(50 / iterations * i)  # Reduced alpha for more fading
        echo_color = color + (alpha,)
        echo_pos = (position[0] - offset * i, position[1])  # Only horizontal offset
        draw.text(echo_pos, text, font=font, fill=echo_color)


def create_faded_background(img, text_height, y_position):
    background = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(background)

    mina, innera, edgeh = 0, 150, 20
    total_height = text_height + edgeh * 2  # Text height + 20px above and below
    y_start = int(y_position - edgeh)
    y_end = int(y_start + total_height)

    for y in range(y_start, y_end):
        if y < y_start + edgeh:
            alpha = int(0 + (y - y_start) * (innera / edgeh))  # Fade from 50 to 150
        elif y > y_end - edgeh:
            alpha = int(innera - (y - (y_end - edgeh)) * (innera / edgeh))  # Fade from 150 to 50
        else:
            alpha = innera
        draw.line([(0, y), (img.width, y)], fill=(0, 0, 0, alpha))

    return background


def overlay_text(image_path, text, font_name=None):
    with Image.open(image_path).convert('RGBA') as img:
        # Create a new RGBA image with the same size
        txt = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)

        # Load the font
        font_size = int(img.width / 10)
        if font_name:
            font_url = f"https://dl.dafont.com/dl/?f={font_name}"
            font_path = download_and_install_font(font_url, font_name)
            if font_path:
                font = ImageFont.truetype(font_path, font_size)
            else:
                print(f"Failed to load {font_name}, using default font.")
                font = ImageFont.truetype("OptimusPrinceps.ttf", font_size)
        else:
            font = ImageFont.truetype("OptimusPrinceps.ttf", font_size)

        # Get text size using textbbox
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

        # Calculate position (centered)
        position = ((img.width - text_width) / 2, (img.height - text_height) / 2)

        # Create faded background
        background = create_faded_background(img, text_height, position[1])

        # Create echo effect
        create_echo_text(draw, text, font, position, (255, 215, 0), iterations=5, offset=3)

        # Draw main text
        draw.text(position, text, font=font, fill=(255, 215, 0, 255))  # Golden color

        # Combine the original image, background, and text with echo
        result = Image.alpha_composite(img, background)
        result = Image.alpha_composite(result, txt)

        # Save the result as PNG
        output_path = os.path.splitext(image_path)[0] + "_output.png"
        result.save(output_path, format='PNG')
        print(f"Image saved as {output_path}")


def display_ascii_art():
    ascii_art = """


░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░       ░▒▓████████▓▒░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░ ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓██████▓▒░  ░▒▓██████▓▒░   ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░         ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░          ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░     
                                                                                                    
                                                                                                    


    """
    print(ascii_art)


def main():
    display_ascii_art()

    while True:
        image_path = input("Which image would you like to change? (or 'exit' to quit): ")
        if image_path.lower() == 'exit':
            print("Goodbye!")
            sys.exit(0)

        if not os.path.exists(image_path):
            print(f"Error: The file '{image_path}' does not exist. Please try again.")
            continue

        text = input("Enter the text to overlay: ")
        font_name = input("Enter the font name (press Enter for default): ").strip() or None

        try:
            overlay_text(image_path, text, font_name)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

        print("Do you want to process another image? (Type 'exit' to quit or press Enter to continue)")
        if input().lower() == 'exit':
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
