import math
import struct
import wave


def synth_to_file(
    text: str, path: str, seconds: float = 1.0, freq: float = 440.0, rate: int = 16000
):
    n_samples = int(seconds * rate)
    with wave.open(path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        for i in range(n_samples):
            value = int(32767.0 * math.sin(2.0 * math.pi * freq * (i / rate)))
            data = struct.pack("<h", value)
            wav.writeframesraw(data)
