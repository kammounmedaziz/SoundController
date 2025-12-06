import platform
import subprocess
import re

class VolumeController:
    """
    Platform-agnostic volume controller.
    """

    def __init__(self):
        self.os = platform.system()
        if self.os == 'Windows':
            try:
                import comtypes
                comtypes.CoInitialize()
                from pycaw.pycaw import AudioUtilities
                devices = AudioUtilities.GetSpeakers()
                self.volume = devices.EndpointVolume
            except ImportError:
                raise ImportError("PyCaw and comtypes are required for Windows volume control.")
        elif self.os not in ['Linux', 'Darwin']:
            raise NotImplementedError("Unsupported OS")

    def get_volume(self):
        """
        Get the current volume level (0-100).

        Returns:
            int: Current volume percentage.
        """
        if self.os == 'Windows':
            return int(self.volume.GetMasterVolumeLevelScalar() * 100)
        elif self.os == 'Linux':
            result = subprocess.run(['amixer', 'get', 'Master'], capture_output=True, text=True)
            match = re.search(r'\[(\d+)%\]', result.stdout)
            return int(match.group(1)) if match else 50
        elif self.os == 'Darwin':  # macOS
            result = subprocess.run(['osascript', '-e', 'output volume of (get volume settings)'], capture_output=True, text=True)
            return int(result.stdout.strip())

    def set_volume(self, volume):
        """
        Set the volume level (0-100).

        Args:
            volume (int): Volume percentage.
        """
        volume = max(0, min(100, volume))
        if self.os == 'Windows':
            self.volume.SetMasterVolumeLevelScalar(volume / 100, None)
        elif self.os == 'Linux':
            subprocess.run(['amixer', 'set', 'Master', f'{volume}%'])
        elif self.os == 'Darwin':
            subprocess.run(['osascript', '-e', f'set volume output volume {volume}'])

    def mute(self):
        """
        Mute the volume.
        """
        if self.os == 'Windows':
            self.volume.SetMute(1, None)
        elif self.os == 'Linux':
            subprocess.run(['amixer', 'set', 'Master', 'mute'])
        elif self.os == 'Darwin':
            subprocess.run(['osascript', '-e', 'set volume with output muted'])

    def unmute(self):
        """
        Unmute the volume.
        """
        if self.os == 'Windows':
            self.volume.SetMute(0, None)
        elif self.os == 'Linux':
            subprocess.run(['amixer', 'set', 'Master', 'unmute'])
        elif self.os == 'Darwin':
            subprocess.run(['osascript', '-e', 'set volume without output muted'])

    def is_muted(self):
        """
        Check if volume is muted.

        Returns:
            bool: True if muted.
        """
        if self.os == 'Windows':
            return self.volume.GetMute()
        elif self.os == 'Linux':
            result = subprocess.run(['amixer', 'get', 'Master'], capture_output=True, text=True)
            return '[off]' in result.stdout
        elif self.os == 'Darwin':
            result = subprocess.run(['osascript', '-e', 'output muted of (get volume settings)'], capture_output=True, text=True)
            return result.stdout.strip() == 'true'