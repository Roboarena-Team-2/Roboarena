import os
from PIL import Image

angles = range(0, 360, 10)  # 0, 10, ..., 350


def generate(prefix, input_folder, output_file):
    first_frame = os.path.join(input_folder, f"{prefix}_000.png")
    first_image = Image.open(first_frame)
    frame_width, frame_height = first_image.size

    spritesheet = Image.new("RGBA", (frame_width, frame_height * len(angles)))

    for i, angle in enumerate(angles):
        filename = f"{prefix}_{angle:03d}.png"
        filepath = os.path.join(input_folder, filename)
        x = 0
        y = i * frame_height
        print("Paste:", filepath)
        spritesheet.paste(Image.open(filepath), (x, y))

    spritesheet.save(output_file)
    print(f"✅ Gespeichert: {output_file}")


# === BODY ===
generate(
    prefix="body", input_folder=r"tank_frames/body", output_file=r"body_spritesheet.png"
)

# === HEAD ===
generate(
    prefix="head", input_folder=r"tank_frames/head", output_file=r"head_spritesheet.png"
)
