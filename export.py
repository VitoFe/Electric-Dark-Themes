"""
This module generates the Electric Dark themes for both Firefox and Chrome.
It loads common manifest data from a JSON file, generates a specific manifest
for each browser, and updates color placeholders using a predefined color scheme.
"""

import copy
import json
import os
import zipfile

# Edit the Nyan Cat frames using ffmpeg to add a transparent padding at the bottom and make the colors more neutral, then convert them to PNG format for better compatibility with Chrome
# ffmpeg -f apng -i nyan-0.png -vf "crop=iw-38:ih:0:0,colorchannelmixer=aa=0.95,format=rgba,geq=r='p(X,Y)':g='p(X,Y)':b='p(X,Y)':a='p(X,Y)*(1-(X/W))',pad=iw:ih+2:0:2:color=0x00000000" -f apng -plays 0 nyan_cat.png
# ffmpeg -f apng -i nyan-1.png -vf "colorchannelmixer=aa=0.5" -f apng -plays 0 nyan_sparkles.png                          

manifest_data = {
    "manifest_version": 3,
    "version": "5.8.5",
    "name": "Electric [color] Dark",
    "author": "Vito Ferri",
    "developer": {"name": "Vito Ferri", "url": "https://github.com/VitoFe"},
    "browser_specific_settings": {"gecko": {"id": "[id]"}},
}


addon_ids = {
    "Purple": "{5d266402-4868-4f0c-b650-fd2d17c3a752}",
    "Orange": "{5d266402-4868-4f0c-b650-fd2d17c3a753}",
    "Green": "{5d266402-4868-4f0c-b650-fd2d17c3a754}",
    "Azure": "{5d266402-4868-4f0c-b650-fd2d17c3a765}",
    "Pink": "{5d266402-4868-4f0c-b650-fd2d17c3a756}",
    "Red": "{5d266402-4868-4f0c-b650-fd2d17c3a757}",
    "Yellow": "{5d266402-4868-4f0c-b650-fd2d17c3a758}",
    "Twitch": "{5d266402-4868-4f0c-b650-fd2d17c3a759}",
    "Discord": "{5d266402-4868-4f0c-b650-fd2d17c3a760}",
    "Cyberpunk": "{5d266402-4868-4f0c-b650-fd2d17c3a761}",
    "Nyan": "{5d266402-4868-4f0c-b650-fd2d17c3a962}",
    "Vaporwave": "{5d266402-4868-4f0c-b650-fd2d17c3a763}",
}


colors = {
    "Purple": {
        "accent_color": "#BD00FF",
        "accent_color_trans": "#BD00FF20",
        "accent_color_semitrans": "#BD00FF30",
        "accent_color_chrome": "#C72EFF",
        "frame_color": "#0C0E14EE",
        "text_color": "#FFFFFF",
        "text_color_popup": "#FFFFFF",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#121521",
    },
    "Orange": {
        "accent_color": "#ff3503",
        "accent_color_trans": "#ff350320",
        "accent_color_semitrans": "#ff350330",
        "accent_color_chrome": "#ff3503",
        "frame_color": "#0C0E14",
        "text_color": "#FFFFFF",
        "text_color_popup": "#0C0E14",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#150e0d",
    },
    "Green": {
        "accent_color": "#00FF00",
        "accent_color_trans": "#00FF0020",
        "accent_color_semitrans": "#00FF0030",
        "accent_color_chrome": "#00FF00",
        "frame_color": "#0C0E14",
        "text_color": "#FFFFFF",
        "text_color_popup": "#0C0E14",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#0D150E",
    },
    "Azure": {
        "accent_color": "#00BFFF",
        "accent_color_trans": "#00BFFF20",
        "accent_color_semitrans": "#00BFFF30",
        "accent_color_chrome": "#00BFFF",
        "frame_color": "#0C0E14",
        "text_color": "#FFFFFF",
        "text_color_popup": "#FFFFFF",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#0D1315",
    },
    "Red": {
        "accent_color": "#FF0000",
        "accent_color_trans": "#FF000020",
        "accent_color_semitrans": "#FF000030",
        "accent_color_chrome": "#FF0000",
        "frame_color": "#0C0E14",
        "text_color": "#FFFFFF",
        "text_color_popup": "#FFFFFF",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#150D0D",
    },
    "Yellow": {
        "accent_color": "#FFFF00",
        "accent_color_trans": "#FFFF0020",
        "accent_color_semitrans": "#FFFF0030",
        "accent_color_chrome": "#FFFF00",
        "frame_color": "#0C0E14",
        "text_color": "#FFFFFF",
        "text_color_popup": "#0C0E14",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#15150D",
    },
    "Pink": {
        "accent_color": "#FF00FF",
        "accent_color_trans": "#FF00FF20",
        "accent_color_semitrans": "#FF00FF30",
        "accent_color_chrome": "#FF00FF",
        "frame_color": "#0C0E14",
        "text_color": "#FFFFFF",
        "text_color_popup": "#FFFFFF",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#150D15",
    },
    "Twitch": {
        "accent_color": "#9146FF",
        "accent_color_trans": "#9146FF20",
        "accent_color_semitrans": "#9146FF30",
        "accent_color_chrome": "#AA60FF",
        "frame_color": "#0C0E14",
        "text_color": "#FFFFFF",
        "text_color_popup": "#FFFFFF",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#1A0F2B",
    },
    "Discord": {
        "accent_color": "#7289DA",
        "accent_color_trans": "#7289DA20",
        "accent_color_semitrans": "#7289DA30",
        "accent_color_chrome": "#7289DA",
        "frame_color": "#23272A",
        "text_color": "#FFFFFF",
        "text_color_popup": "#FFFFFF",
        "text_muted_color": "#99AAB5",
        "toolbar_color": "#2C2F33",
    },
    "Cyberpunk": {
        "accent_color": "#BD00FF",
        "accent_color_trans": "#BD00FF20",
        "accent_color_semitrans": "#BD00FF30",
        "accent_color_chrome": "#C72EFF",
        "frame_color": "#0C0E14DD",
        "text_color": "#f2e900",
        "text_color_popup": "#002b32",
        "text_muted_color": "#02d7f2",
        "toolbar_color": "#0D131560",
        "theme_frame": "images/cyberpunk.png"
    },
    "Nyan": {
        "accent_color": "#BD00FF",
        "accent_color_trans": "#BD00FF20",
        "accent_color_semitrans": "#BD00FF30",
        "accent_color_chrome": "#C72EFF",
        "frame_color": "#0C0E14EE",
        "text_color": "#FFFFFF",
        "text_color_popup": "#FFFFFF",
        "text_muted_color": "#CCCCCC",
        "toolbar_color": "#12152130",
        "additional_backgrounds": ["images/nyan_cat.png", "images/nyan_sparkles.png"],
        "additional_backgrounds_alignment": ["right top", "right top"],
        "additional_backgrounds_tiling": ["no-repeat", "repeat"],
    },
    "Vaporwave": {
        "accent_color": "#f62e97",
        "accent_color_trans": "#f62e9720",
        "accent_color_semitrans": "#f62e9730",
        "accent_color_chrome": "#f62e97",
        "frame_color": "#1A0F2BDD",
        "text_color": "#f9d653",
        "text_color_popup": "#0C0E14",
        "text_muted_color": "#f9ba53",
        "toolbar_color": "#1A0F2B50",
        "theme_frame": "images/vaporwave.png"
    },
}

def invert_hex(hex_color):
  hex_color = hex_color.lstrip('#')
  r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
  r = 255 - r
  g = 255 - g
  b = 255 - b
  inverted_hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
  return inverted_hex

def extract_number(filename):
  name = filename.split(".")[0]
  for i in range(len(name)):
    if name[i].isdigit():
      number = name[i:]
      return int(number)
  return None

# Convert color theme from dark-mode to light-mode
def convert_theme(theme):
  new_theme = {}
  for key, value in theme.items():
    if value.startswith('#'):
      new_value = invert_hex(value)
    else:
      new_value = value
    new_theme[key] = new_value
  return new_theme


# Load common manifest data
with open(os.path.join("templates", "common.json"), "r", encoding="utf-8") as f:
    manifest_data.update(json.load(f))

# Delete the previously generated packages
if os.path.exists("out"):
    for file in os.listdir("out"):
        if file.endswith(".xpi") or file.endswith(".zip"):
            os.remove(os.path.join("out", file))

# Generate extension package for each browser
for browser in ["firefox", "chrome"]:
    with open(os.path.join("templates", f"{browser}.json"), "r", encoding="utf-8") as f:
        manifest_spec = json.load(f)
        # Parse color placeholders
        for accent, colormap in colors.items():
            manifest = copy.deepcopy(manifest_data)
            manifest["theme"]["colors"].update(manifest_spec["colors"])
            manifest["name"] = manifest_data["name"].replace("[color]", accent)
            manifest.update(
                {"browser_specific_settings": {"gecko": {"id": addon_ids[accent]}}}
            )
            if "theme_frame" in colormap.keys():
                theme_frame = colormap["theme_frame"].replace("[browser]", browser)
                if theme_frame.endswith(".svg") and browser != "firefox":
                    theme_frame = theme_frame.replace(".svg", ".png")
                manifest["theme"]["images"]["theme_frame"] = theme_frame
            if "theme_ntp_bg" in colormap.keys():
                manifest["theme"]["images"]["theme_ntp_background"] = colormap["theme_ntp_bg"]
            if "additional_backgrounds" in colormap:
                manifest["theme"]["images"]["additional_backgrounds"] = colormap["additional_backgrounds"]
            if "additional_backgrounds_alignment" in colormap:
                manifest["theme"]["properties"]["additional_backgrounds_alignment"] = colormap["additional_backgrounds_alignment"]
            if "additional_backgrounds_tiling" in colormap:
                manifest["theme"]["properties"]["additional_backgrounds_tiling"] = colormap["additional_backgrounds_tiling"]
            context = colormap.copy()
            manifest["theme"]["colors"] = {
                key: context[value] if value in context else value
                for key, value in manifest["theme"]["colors"].items()
            }
            if browser == "chrome":  # RGB array instead of HEX
                manifest["theme"]["colors"] = {
                    element[0]: [int(element[1][i : i + 2], 16) for i in (1, 3, 5)]
                    if element[1].startswith("#")
                    else element[1]
                    for element in manifest["theme"]["colors"].items()
                }
            # Create extension package
            EXT = ".xpi" if browser == "firefox" else ".zip"
            theme_file = f"{manifest['name'].replace(' ', '')}_{browser}_{manifest['version']}{EXT}"
            if not os.path.exists("out"):
                os.makedirs("out")
            with zipfile.ZipFile(os.path.join("out", theme_file), "w", zipfile.ZIP_DEFLATED) as package:
                for include_dir in [ "icons", "images"]:
                    for root, dirs, files in os.walk(include_dir):
                        for file in files:
                            if include_dir == "icons":
                                if file.startswith(accent.lower()):
                                    resolution = str(extract_number(file))
                                    manifest["icons"][resolution] = f"{include_dir}/{file}"
                                    package.write(os.path.join(root, file))
                                elif file.startswith("icon"):
                                    package.write(os.path.join(root, file))
                            else:
                                package.write(os.path.join(root, file))
                package.write("LICENSE")
                package.writestr("manifest.json", json.dumps(manifest))
