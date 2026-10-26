import io
import math
import struct
import wave

import pygame

# Sound effects are synthesised at start-up, so no audio files are needed.

SAMPLE_RATE = 22050

# Each effect is a list of (start Hz, end Hz, seconds) frequency sweeps.
EAT_NOTES = [(660, 660, 0.05), (990, 1320, 0.08)]
GAME_OVER_NOTES = [(440, 440, 0.16), (370, 370, 0.16), (311, 311, 0.16), (262, 196, 0.5)]


def _synthesize(notes, volume, square):
    samples = bytearray()
    phase = 0.0
    for start_hz, end_hz, seconds in notes:
        count = int(SAMPLE_RATE * seconds)
        for i in range(count):
            freq = start_hz + (end_hz - start_hz) * i / count
            phase += 2 * math.pi * freq / SAMPLE_RATE
            wave_value = math.sin(phase)
            if square:
                wave_value = 0.6 if wave_value >= 0 else -0.6
            # Short fade in/out on every note so they don't click.
            envelope = min(1.0, i / 150, (count - i) / 300)
            samples += struct.pack("<h", int(volume * envelope * wave_value * 32767))

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(bytes(samples))
    buffer.seek(0)
    return pygame.mixer.Sound(file=buffer)


class SoundManager:
    def __init__(self):
        # The game must still run without an audio device, so any mixer
        # failure just leaves the game silent.
        self.sounds = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.sounds["eat"] = _synthesize(EAT_NOTES, volume=0.5, square=False)
            self.sounds["game_over"] = _synthesize(GAME_OVER_NOTES, volume=0.35, square=True)
        except pygame.error:
            self.sounds = {}

    def play(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()
