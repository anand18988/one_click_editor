import subprocess
import re
from pathlib import Path
import shutil
import sys
import traceback

from helper import reset, log, set_status, update_progress

def main(blender_exe, one_click_editor_path, video_folder):

    try:
        # ALL your existing code here
        blender_exe = Path(blender_exe)
        one_click_editor_path = Path(one_click_editor_path)
        folder_path = Path(video_folder)

        # Rest of your code...
        # Put ALL your existing processing code here
    
        

        reset()

        log("Program Started")
        set_status("Starting...")
        update_progress(0)

        


        #-------------------------------------------Transcribe----------------------------------------------------


    

    
        print(f"Blender: {blender_exe}")
        print(f"Editor : {one_click_editor_path}")
        print(f"Video  : {folder_path}")

        blender_exe_path = blender_exe
        audio_folder = folder_path

        audio_extensions = {".wav", ".mp3", ".flac", ".aac", ".m4a", ".ogg"}

        # Get all audio files

        set_status("Scanning audio files...")
        update_progress(5)
        log("Scanning audio files...")

        audio_files = [
            file for file in audio_folder.iterdir()
            if file.is_file() and file.suffix.lower() in audio_extensions
        ]

        for i, audio_file in enumerate(audio_files, start=1):
            print(f"File name : {audio_file.name}")
            print(f"Full path : {audio_file}")

            
            output_dir = audio_folder

            # Run Whisper
            set_status("Running Whisper...")
            update_progress(20)
            log("Running Whisper...")
            subprocess.run([
                "python",
                "-m",
                "whisper",
                str(audio_file),
                "--language", "English",
                "--model", "tiny",
                "--output_dir", str(output_dir)
            ], check=True)

            # Keep only VTT
            base_name = Path(audio_file).stem

            for ext in [".txt", ".srt", ".tsv", ".json"]:
                file_to_delete = output_dir / f"{base_name}{ext}"
                if file_to_delete.exists():
                    file_to_delete.unlink()

            print("Done. Only VTT file retained.")

        # ----------------------------------------------Time Stamp only--------------------------------------
        vtt_extensions = {".vtt"}


        # Get all audio files
        vtt_files = [
            file for file in audio_folder.iterdir()
            if file.is_file() and file.suffix.lower() in vtt_extensions
        ]

        for i, vtt_file in enumerate(vtt_files, start=1):
            print(f"File name : {vtt_file.name}")
            print(f"Full path : {vtt_file}")

        # Input file
            input_file = vtt_file

            # Output file
            set_status("Extracting timestamps...")
            update_progress(40)
            log("Extracting timestamps...")
            output_file = vtt_file.parent / f"timestamonly{vtt_file.stem}.vtt"
            
            if output_file.exists():
                print(f"✓ Found {output_file.name}")
            else:
                # Match:
                # 00:00.000 --> 00:07.000
                timestamp_pattern = re.compile(
                    r'(\d{2}:\d{2}\.\d{3})\s*-->\s*\d{2}:\d{2}\.\d{3}'
                )

                slide_pattern = re.compile(r'^Slide\s+\d+', re.IGNORECASE)

                slide_timestamps = []

                with open(input_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                for i in range(len(lines) - 1):

                    timestamp_match = timestamp_pattern.search(lines[i])

                    if timestamp_match and slide_pattern.search(lines[i + 1].strip()):
                        slide_timestamps.append(timestamp_match.group(1))

                with open(output_file, "w", encoding="utf-8") as f:
                    for ts in slide_timestamps:
                        f.write(ts + "\n")

                print(f"Done. Output saved to {output_file}")
            
            #-------------------------------------Split Audio---------------------------------------------

        k=0
        # Get all WAV files in alphabetical order
        set_status("Splitting audio...")
        update_progress(50)
        log("Splitting audio...")
        audio_files = sorted(audio_folder.glob("*.wav"))

        print(f"Found {len(audio_files)} audio files.\n")

        for i, audio_file in enumerate(audio_files, start=1):

            # Build the matching VTT filename
            vtt_file = audio_folder / f"timestamonly{audio_file.stem}.vtt"

            # Check that the VTT exists
            if not vtt_file.exists():
                print(f"Missing VTT for {audio_file.name}")
                continue
            
            print(f"Audio : {audio_file.name}")
            print(f"VTT   : {vtt_file.name}")

        


            # Input audio file
        # audio_file = r"A:\youtube channel\video\satyam\part 03.wav"

            # Timestamp file
            timestamp_file = vtt_file
            # Output folder
            output_folder = audio_folder/f"audio"
            output_folder.mkdir(exist_ok=True)

            # Read timestamps
            with open(timestamp_file, "r", encoding="utf-8") as f:
                timestamps = [line.strip() for line in f if line.strip()]

            # Create audio segments
            for j in range(len(timestamps)):

                start = timestamps[j]
                output_file = output_folder / f"{k+1}.wav"
                k+=1

                if j < len(timestamps) - 1:
                    end = timestamps[j + 1]

                    cmd = [
                        "ffmpeg",
                        "-y",
                        "-i", audio_file,
                        "-ss", start,
                        "-to", end,
                        str(output_file)
                    ]
                else:
                    # Last segment goes until end of file
                    cmd = [
                        "ffmpeg",
                        "-y",
                        "-i", audio_file,
                        "-ss", start,
                        str(output_file)
                    ]

                subprocess.run(cmd, check=True)

            print(f"Done. Audio files saved in: {output_folder}")

        print("\nFinished.")
        # --------------------------------cut paste all image to Audio folder------------------------------

        set_status("Shifting all the slides to audio folder...")
        update_progress(60)
        log("Shifting all the slides to audio folder...")

        # Source folder
        source_folder = audio_folder

        # Destination folder
        destination_folder = output_folder

        # Create destination folder if it doesn't exist
        destination_folder.mkdir(parents=True, exist_ok=True)

        # Image extensions
        image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tif", ".tiff"}

        # Move all images
        for image_file in source_folder.iterdir():
            if image_file.is_file() and image_file.suffix.lower() in image_extensions:
                shutil.move(str(image_file), str(destination_folder / image_file.name))
                print(f"Moved: {image_file.name}")

        print("All images moved successfully.")

        #-------------------changing path in bat file moduel---------------------


        

        # Debug information
        
        #----------------calling batch file------------------
        set_status("Launching Blender...")
        update_progress(70)
        log("Launching Blender...")


        blender = blender_exe_path
        print("Using Blender executable:", blender)
        
        
        

        blend_file = one_click_editor_path / "templet.blend"
        python_script = one_click_editor_path / "Blender video and audio auto sequencing.py"

        cmd = [
            str(blender),
            str(blend_file),
            "--python",
            str(python_script),
            "--",
            str(output_folder)
        ]

        print(cmd)

        result = subprocess.run(cmd, text=True)

        

        print("Return code:", result.returncode)
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)

        print("Blender finished.")
        set_status("Completed")
        update_progress(100)
        log("Completed successfully")



        if __name__ == "__main__":
        

            main(
                sys.argv[1],
                sys.argv[2],
                sys.argv[3]
            )

    except Exception as e:
       

        log(str(e))
        log(traceback.format_exc())

        set_status("ERROR")

    finally:
        update_progress(100)

    