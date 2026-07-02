import bpy
import os
import re
from pathlib import Path

#-------------------------------path of One Click Editor-------------------------
print("=== Blender automation script started ===")
# Folder where this Python file is located
import sys

# Blender passes everything after "--" to the script
if "--" in sys.argv:
    folder = sys.argv[sys.argv.index("--") + 1]
else:
    raise Exception("No folder path received from transcribe1.py")

print("Media Folder:", folder)
scene = bpy.context.scene

if scene.sequence_editor is None:
    scene.sequence_editor_create()

seq = scene.sequence_editor

# Clear existing strips (optional)
for strip in list(seq.strips_all):
    seq.strips.remove(strip)

current_frame = 1
count = 0

image_exts = (".jpg", ".jpeg", ".png")
audio_exts = (".mp3", ".wav", ".m4a")

images = [f for f in os.listdir(folder)
          if f.lower().endswith(image_exts)]

# Sort Slide18, Slide19, Slide20...
images.sort(key=lambda x: int(re.findall(r'\d+', x)[0]))

for img in images:

    nums = re.findall(r'\d+', img)

    if not nums:
        continue

    slide_no = nums[0]

    audio_file = None

    for ext in audio_exts:
        candidate = slide_no + ext

        if os.path.exists(os.path.join(folder, candidate)):
            audio_file = candidate
            break

    if audio_file is None:
        continue

    image_path = os.path.join(folder, img)
    audio_path = os.path.join(folder, audio_file)

    try:
        # AUDIO
        sound = seq.strips.new_sound(
            name=f"Audio_{slide_no}",
            filepath=audio_path,
            channel=1,
            frame_start=current_frame
        )

        duration = sound.frame_final_duration

        # IMAGE
        image = seq.strips.new_image(
            name=f"Slide_{slide_no}",
            filepath=image_path,
            channel=2,
            frame_start=current_frame
        )

        image.frame_final_duration = duration
       
          # Match manual import behaviour
        image.transform.scale_x = 1.5
        image.transform.scale_y = 1.5
        current_frame += duration
        count += 1

    except Exception as e:
        print(e)

scene.frame_end = current_frame

bpy.context.window_manager.popup_menu(
    lambda self, context:
        self.layout.label(text=f"{count} slide/audio pairs imported"),
    title="Finished",
    icon='INFO'
)