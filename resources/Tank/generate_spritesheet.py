import os
from PIL import Image

# Config
input_folder = "tank_frames"
output_file = "tank_spritesheet.png"
frame_count = 36  # 000.png to 035.png
columns = 1
rows = 36

# Get frame size from first image
first_frame = os.path.join(input_folder, "panzer_000.png")
first_image = Image.open(first_frame)
frame_width, frame_height = first_image.size

# Create empty spritesheet
spritesheet = Image.new("RGBA", (columns * frame_width, rows * frame_height))

# Add all frames
for i in range(frame_count):
    filename = f"panzer_{i:03d}.png"
    filepath = os.path.join(input_folder, filename)
    x = 0
    y = i * frame_height
    spritesheet.paste(Image.open(filepath), (x, y))

# Save
spritesheet.save(output_file)