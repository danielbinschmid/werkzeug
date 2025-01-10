import numpy as np 
import scipy.io
from typing import Optional, List
import os
from pathlib import Path
import shutil
import os

def save_audio_as_wav(
    audio_out: np.ndarray, t_folder: str, prompts: Optional[List[str]] = None
) -> None:
    """
    if prompts are none, empty prompts are taken
    """
    os.makedirs(t_folder, exist_ok=True)
    for idx in range(len(audio_out)):
        prompt = prompts[idx] if prompts is not None else ""
        filename = f"{idx}_{prompt}.wav"
        filepath = os.path.join(t_folder, filename)
        scipy.io.wavfile.write(filepath, rate=16000, data=audio_out[idx])


def merge_output_folders(src_folder: str):
    src_path = Path(src_folder)

    for subfolder in src_path.iterdir():
        if subfolder.is_dir():
            folder_name = subfolder.name

            for wav_file in subfolder.glob("*.wav"):
                new_filename = f"{folder_name}_{wav_file.name}"
                dest_path = src_path / new_filename

                shutil.move(str(wav_file), dest_path)