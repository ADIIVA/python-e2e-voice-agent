import os
import wave
from typing import Callable, Optional


class ChalisaSequencer:
    """
    Orchestrates: Preface (TTS) -> Verse playback (mp3/wav) -> Explanation+Repeat (TTS).

    The sequencer is framework-agnostic. Provide callbacks for:
      - emit_conversation(role, content)
      - inject_tts(message): awaitable that triggers agent TTS
      - emit_mp3(bytes)
      - emit_pcm_chunk(bytes, sample_rate)
      - emit_pcm_done()
      - await_playback_done(): awaitable that resolves when client confirms playback finished
    """

    def __init__(
        self,
        emit_conversation: Callable[[str, str], None],
        inject_tts,  # async function(message: str) -> None
        emit_mp3: Callable[[bytes], None],
        emit_pcm_chunk: Callable[[bytes, int], None],
        emit_pcm_done: Callable[[], None],
        await_playback_done,  # async function() -> None
    ) -> None:
        self.emit_conversation = emit_conversation
        self.inject_tts = inject_tts
        self.emit_mp3 = emit_mp3
        self.emit_pcm_chunk = emit_pcm_chunk
        self.emit_pcm_done = emit_pcm_done
        self.await_playback_done = await_playback_done

    async def run_step(
        self,
        playback_path: Optional[str],
        translation_en: str,
        verse_prompt: Optional[str] = None,
        repeat_prompt: Optional[str] = None,
    ) -> None:
        preface = "Okay, let me play the verse for you first."
        self.emit_conversation("assistant", preface)
        await self.inject_tts(preface)

        if playback_path:
            await self._play_audio(playback_path)
            # Wait for browser playback confirmation
            await self.await_playback_done()

        meaning = f"Meaning in English: {translation_en}."
        repeat = repeat_prompt or "Now, would you like to repeat this line with me?"

        explanation = meaning if not verse_prompt else f"{verse_prompt} {meaning}"
        full_line = f"{explanation} {repeat}".strip()
        self.emit_conversation("assistant", full_line)
        await self.inject_tts(full_line)

    async def _play_audio(self, path: str) -> None:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".mp3":
            with open(path, "rb") as f:
                self.emit_mp3(f.read())
            return
        if ext == ".wav":
            with wave.open(path, "rb") as wf:
                sr = int(wf.getframerate()) or 16000
                frames_per_chunk = sr
                while True:
                    frames = wf.readframes(frames_per_chunk)
                    if not frames:
                        break
                    self.emit_pcm_chunk(frames, sr)
            self.emit_pcm_done()
            return
        # Unsupported - emit nothing
        return


