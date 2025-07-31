import os
from PIL import Image

# Config
input_folder = "spider_frames"
output_file = "spider_spritesheet.png"
angle_step = 10
frames_per_angle = 4
rows = 360 // angle_step
columns = frames_per_angle

# Get frame size from first image
file = os.path.join(input_folder, "000_1.png")
sample_image = Image.open(file)
frame_width, frame_height = sample_image.size

# Create empty spritesheet
spritesheet = Image.new("RGBA", (columns * frame_width, rows * frame_height))

# Add all frames
for angle in range(0, 360, angle_step):
    i = angle // angle_step  # row
    for j in range(1, frames_per_angle + 1):
        filename = f"{angle:03d}_{j}.png"
        filepath = os.path.join(input_folder, filename)
        x = (j - 1) * frame_width
        y = i * frame_height
        spritesheet.paste(Image.open(filepath), (x, y))

# Save
spritesheet.save(output_file)
