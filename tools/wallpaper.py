import os
import re
import sys
import ctypes
import struct
import subprocess
import urllib.parse


def get_env():
    # Get Current Desktop Environment
    def get(name): return os.environ.get(
        name) if os.environ.get(name) else None
    support = ["XDG_CURRENT_DESKTOP", "DESKTOP_SESSION", "GNOME_DESKTOP_SESSION_ID",
               "MATE_DESKTOP_SESSION_ID", "SWAYSOCK", "DESKTOP_STARTUP_ID"]
    for env in support:
        out = get(env)
        if out:
            if "GNOME" in env:
                return "GNOME"
            elif "MATE" in env:
                return "MATE"
            elif "SWAY" in env:
                return "SWAY"
            elif "awesome" in out:
                return "AWESOME"
            else:
                return out
    return None


def is_64bit_windows():
    """Check if 64 bit Windows OS"""
    return struct.calcsize('P') * 8 == 64


def setwallpaper(image_path, relative_path=True):
    host = sys.platform
    desktop = get_env()
    if relative_path:
        image_path = os.path.join(os.getcwd(), image_path)
    if "linux" in host:
        desktop = str(desktop).lower()

        def disown(cmd): return subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if desktop in ["xfce", "xubuntu"]:
            xfconf_re = re.compile(
                r"^/backdrop/screen\d/monitor(?:0|\w*)/"
                r"(?:(?:image-path|last-image)|workspace\d/last-image)$",
                flags=re.M
            )
            xfconf_data = subprocess.check_output(
                ["xfconf-query", "--channel", "xfce4-desktop", "--list"],
                stderr=subprocess.DEVNULL
            ).decode('utf8')
            paths = xfconf_re.findall(xfconf_data)
            for path in paths:
                disown(["xfconf-query", "--channel", "xfce4-desktop",
                        "--property", path, "--set", image_path])
        elif desktop in ["muffin", "cinnamon"]:
            disown(["gsettings", "set", "org.cinnamon.desktop.background",
                    "picture-uri", "file://" + urllib.parse.quote(image_path)])
        elif desktop in ["gnome", "unity"]:
            disown(["gsettings", "set", "org.gnome.desktop.background",
                    "picture-uri", "file://" + urllib.parse.quote(image_path)])
        elif "mate" in desktop:
            disown(["gsettings", "set", "org.mate.background",
                    "picture-filename", image_path])
        elif "sway" in desktop:
            disown(["swaymsg", "output", "*", "bg", image_path, "fill"])
        elif "awesome" in desktop:
            disown(
                ["awesome-client", "require('gears').wallpaper.maximized('"+image_path+"')"])
        else:
            if desktop:
                return f"Sorry, {desktop} is currently not supported.", False
            else:
                return f"Sorry, Desktop Environment could not be detected", False
    elif "darwin" in host:
        db_file = "Library/Application Support/Dock/desktoppicture.db"
        db_path = os.path.join(
            os.getenv("HOME", os.getenv("USERPROFILE")), db_file)
        img_dir, _ = os.path.split(image_path)
        sql = "delete from data; "
        sql += "insert into data values(\"%s\"); " % img_dir
        sql += "insert into data values(\"%s\"); " % image_path
        sql += "update preferences set data_id=2 where key=1 or key=2 or key=3; "
        sql += "update preferences set data_id=1 where key=10 or key=20 or key=30;"
        subprocess.call(["sqlite3", db_path, sql])
        subprocess.call(["killall", "Dock"])

    elif "win32" in host:
        if is_64bit_windows():
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 3)
        else:
            ctypes.windll.user32.SystemParametersInfoA(20, 0, image_path, 3)
    else:
        return f"Sorry, currently there is no support for {host}", False

    return "Changed wallpaper successfully", True
