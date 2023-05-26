"""
This module generates the Electric Dark themes for both Firefox and Chrome.
It loads common manifest data from a JSON file, generates a specific manifest
for each browser, and updates color placeholders using a predefined color scheme.
"""

import os
import zipfile
import json
import copy

manifest_data = {
    "manifest_version": 3,
    "version": "5.5",
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
    "Cerbero": "{5d266402-4868-4f0c-b650-fd2d17c3a762}",
}


colors = {
    "Purple": {
        "accent_color": "#BD00FF",
        "accent_color_trans": "#BD00FF20",
        "accent_color_semitrans": "#BD00FF30",
        "accent_color_chrome": "#C72EFF",
        "frame_color": "#0C0E14",
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
        "theme_frame": "images/twitch-[browser].png",
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
        "theme_frame": "images/discord-[browser].png",
    },
    "Cyberpunk": {
        "accent_color": "#BD00FF",
        "accent_color_trans": "#BD00FF20",
        "accent_color_semitrans": "#BD00FF30",
        "accent_color_chrome": "#C72EFF",
        "frame_color": "#0C0E14",
        "text_color": "#f2e900",
        "text_color_popup": "#002b32",
        "text_muted_color": "#02d7f2",
        "toolbar_color": "#0D1315",
        "theme_frame": "images/cyberpunk.svg"
    },
    "Cerbero": {
        "accent_color": "#fffe94",
        "accent_color_trans": "#fffe9420",
        "accent_color_semitrans": "#fffe9430",
        "accent_color_chrome": "#fffe94",
        "frame_color": "#0d0d0080",
        "text_color": "#fffe94",
        "text_color_popup": "#0C0E14",
        "text_muted_color": "#cccb76",
        "toolbar_color": "#0d0d0050",
        "theme_ntp_bg": "images/cerbero-ntpb.png",
        "theme_frame": "images/cerbero.png"
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
            extension_file = f"{manifest['name'].replace(' ', '')}_{browser}_{manifest['version']}{EXT}"
            with zipfile.ZipFile(extension_file, "w", zipfile.ZIP_DEFLATED) as package:
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
