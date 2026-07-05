# 🎬 One Click Editor

> **Automatically synchronize PowerPoint slides with narration and generate a fully arranged Blender Video Sequence Editor timeline in a single click.**

One Click Editor is an automation tool designed for content creators, educators, trainers, and YouTubers who create slide-based videos.

Instead of manually transcribing narration, cutting hundreds of audio clips, importing slides into Blender, matching each narration to its slide, and arranging everything on the timeline, One Click Editor performs the entire process automatically.

It can save **hours of repetitive editing work** and produce a perfectly synchronized Blender timeline within minutes.

---

# ✨ Features

* 🎤 Automatically transcribes narration using **OpenAI Whisper**
* 🔍 Detects the spoken word **"Slide"** during transcription
* ⏱ Extracts timestamps for every slide
* ✂ Automatically splits narration into individual audio files using **FFmpeg**
* 🖼 Automatically imports PowerPoint slide images into Blender Video Sequence Editor
* 🔊 Places each narration clip directly below its corresponding slide
* 📏 Automatically adjusts slide duration to match narration duration
* 🎬 Creates a fully arranged Blender timeline ready for rendering
* 📈 Saves hours of manual editing

---

# 📂 Required File Naming

## Narration Audio

Place all narration files inside your project folder using sequential names:

```text
part 01.wav
part 02.wav
part 03.wav
...
```

Any audio format supported by FFmpeg may be used.

---

## Slide Images

Export your PowerPoint presentation as images and name them:

```text
Slide1.png
Slide2.png
Slide3.png
Slide4.png
...
```

Supported formats:

* PNG
* JPG
* JPEG

---

# ⚙ Workflow

```text
Narration
      │
      ▼
OpenAI Whisper
      │
      ▼
Speech Transcription
      │
      ▼
Detect the word "Slide"
      │
      ▼
Extract timestamps
      │
      ▼
FFmpeg splits narration
      │
      ▼
1.wav
2.wav
3.wav
...
      │
      ▼
Blender imports

Slide1 + 1.wav
Slide2 + 2.wav
Slide3 + 3.wav
...
      │
      ▼
Automatically arranged Blender Timeline
```

---

# 📦 Software Requirements

Install the following software before using One Click Editor.

---

## 1️⃣ Blender

Download:

https://www.blender.org/download/

Blender is used to automatically generate the final video timeline.

---

## 2️⃣ Python (3.13 or later recommended)

Download:

https://www.python.org/downloads/

During installation, enable:

✅ **Add Python to PATH**

---

## 3️⃣ OpenAI Whisper

Install using:

```bash
python -m pip install openai-whisper
```

Verify installation:

```bash
python -m whisper --help
```

---

## 4️⃣ FFmpeg

Install using Winget:

```bash
winget install Gyan.FFmpeg
```

or download from:

https://ffmpeg.org/download.html

Verify installation:

```bash
ffmpeg -version
```

---

# 📁 Project Structure

```text
One_Click_Editor/

│
├── launcher.py
├── launcher.spec
├── transcribe1.py
├── helper.py
├── templet.blend
├── Blender video and audio auto sequencing.py
├── icon.ico
│
├── build/
├── dist/
│
├── settings.json
└── status.json
```

---

# 🚀 Running the Project (Python)

Navigate to the project folder:

```bash
cd /d "A:\Program\python\one_click_editor"
```

Launch the application:

```bash
python launcher.py
```

---

# 🔨 Building the Executable (PyInstaller)

Before building, delete the previous build folders:

```text
build
dist
```

Also delete (if present):

```text
settings.json
status.json
```

Navigate to the project folder:

```bash
cd /d "A:\Program\python\one_click_editor"
```

Build using the provided spec file:

```bash
python -m PyInstaller launcher.spec --clean
```

After a successful build, the executable will be created inside:

```text
dist/
```

Run:

```text
dist/
└── launcher.exe
```

---

# ▶ How to Use

1. Install all required software.
2. Export your PowerPoint slides as images.
3. Place narration audio files inside your project folder.
4. Ensure all files follow the required naming convention.
5. Launch **One Click Editor**.
6. Select:

   * Blender executable
   * One Click Editor folder
   * Working project folder
7. Click **START**.

The software will automatically:

* Transcribe narration
* Detect slide timestamps
* Split narration into individual audio clips
* Import slides into Blender
* Import narration clips
* Arrange the complete Blender timeline

---

# 📂 Example Project

```text
Project Folder

part 01.wav
part 02.wav

Slide1.png
Slide2.png
Slide3.png
Slide4.png
...
```

After processing:

```text
1.wav
2.wav
3.wav
4.wav
...
```

Blender timeline:

```text
Slide1 ─────────────────────────────
Audio1 ─────────────────────────────

Slide2 ─────────────────────────────
Audio2 ─────────────────────────────

Slide3 ─────────────────────────────
Audio3 ─────────────────────────────
```

---

# 🎯 Ideal For

* Educational videos
* YouTube creators
* Online courses
* Lecture recordings
* PowerPoint presentations
* Maritime training
* Corporate training
* Technical tutorials

---

# 💡 Benefits

* ✅ Eliminates manual transcription workflow
* ✅ Eliminates manual audio cutting
* ✅ Eliminates manual slide synchronization
* ✅ Eliminates manual Blender timeline editing
* ✅ Produces accurate, repeatable results
* ✅ Saves hours of repetitive work

---

# 🛠 Built With

* Python
* Blender
* OpenAI Whisper
* FFmpeg
* Tkinter
* PyInstaller

---

# 📜 License

This project is released under the **Anand License**.

You are free to use, modify, and improve this project.

---

# ⭐ Support

If this project saves you time, please consider giving it a ⭐ on GitHub.

Bug reports, feature requests, and pull requests are always welcome!
