"""
This module generates the Electric Purple Dark theme for both Firefox and Chrome.
It loads common manifest data from a JSON file, generates a specific manifest
for each browser, and updates color placeholders using a predefined color scheme.
"""

import os
import zipfile
import json
import copy

manifest_data = {
    "manifest_version": 3,
    "version": "5.2",
    "name": "Electric Purple Dark",
}


colors = {
    "accent_color": "#BD00FF",
    "accent_color_semitrans": "#BD00FF30",
    "accent_color_chrome": "#C72EFF",
    "frame_color": "#0C0E14",
    "text_color": "#FFFFFF",
    "text_muted_color": "#CCCCCC",
    "toolbar_color": "#131622",
}

# Load common manifest data
with open(os.path.join("templates", "common.json"), "r", encoding="utf-8") as f:
    manifest_data.update(json.load(f))

# Generate extension package for each browser
for browser in ["firefox", "chrome"]:
    with open(os.path.join("templates", f"{browser}.json"), "r", encoding="utf-8") as f:
        manifest_spec = json.load(f)
        manifest = copy.deepcopy(manifest_data)
        manifest["theme"]["colors"].update(manifest_spec["colors"])
        # Parse color placeholders
        context = colors.copy()
        if browser == "chrome":  # RGB array instead of HEX
            context = {
                key: [int(value[i : i + 2], 16) for i in (1, 3, 5)]
                if value.startswith("#")
                else value
                for key, value in context.items()
            }
        manifest["theme"]["colors"] = {
            key: context[value] if value in context else value
            for key, value in manifest["theme"]["colors"].items()
        }
        # Create extension package
        EXT = ".xpi" if browser == "firefox" else ".zip"
        extension_file = f"{manifest_data['name'].replace(' ', '')}_{browser}_{manifest_data['version']}{EXT}"
        with zipfile.ZipFile(extension_file, "w", zipfile.ZIP_DEFLATED) as package:
            for root, dirs, files in os.walk("icons"):
                for file in files:
                    package.write(os.path.join(root, file))
            package.write("LICENSE")
            package.writestr("manifest.json", json.dumps(manifest))
