import array
import math
import pygame

# Sound Effects
#
# Short tones are generated in code, so the game needs no audio files.
# If audio can't be initialized (no device, missing driver, etc.) the
# game keeps running silently.

VOLUME = 0.4


class Sounds:
    def __init__(self):
        self.enabled = False
        self._sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            rate, fmt, channels = pygame.mixer.get_init()
            if fmt != -16:
                raise pygame.error(f"unsupported mixer format {fmt}")
            self._rate, self._channels = rate, channels
            self._sounds = {
                "hit": self._make_tone([(880, 0.08)]),
                "miss": self._make_tone([(200, 0.12)], square=True),
                "round_end": self._make_tone([(660, 0.15), (523, 0.15), (392, 0.30)]),
            }
            self.enabled = True
        except (pygame.error, TypeError) as exc:
            print(f"Sound disabled: {exc}")

    def _make_tone(self, notes, square=False):
        # Build 16-bit samples for a sequence of (frequency, seconds) notes,
        # with a short fade in/out on each note to avoid clicks.
        samples = array.array("h")
        fade = int(self._rate * 0.005)
        for freq, seconds in notes:
            n = int(self._rate * seconds)
            for i in range(n):
                wave = math.sin(2 * math.pi * freq * i / self._rate)
                if square:
                    wave = 1.0 if wave >= 0 else -1.0
                envelope = min(1.0, i / fade, (n - i) / fade)
                value = int(32767 * VOLUME * envelope * wave)
                for _ in range(self._channels):
                    samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name):
        if self.enabled:
            self._sounds[name].play()
