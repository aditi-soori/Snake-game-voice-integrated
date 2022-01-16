#
# Copyright 2018-2020 Picovoice Inc.
#
# You may not use this file except in compliance with the license. A copy of the license is located in the "LICENSE"
# file accompanying this source.
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

import os
from ctypes import *
from enum import Enum


class Porcupine(object):
    """
    Python binding for Porcupine wake word engine. It detects utterances of given keywords within an incoming stream of
    audio in real-time. It processes incoming audio in consecutive frames and for each frame emits the detection result.
    The number of samples per frame can be attained by calling `.frame_length`. The incoming audio needs to have a
    sample rate equal to `.sample_rate` and be 16-bit linearly-encoded. Porcupine operates on single-channel audio.
    """

    class PicovoiceStatuses(Enum):
        SUCCESS = 0
        OUT_OF_MEMORY = 1
        IO_ERROR = 2
        INVALID_ARGUMENT = 3
        STOP_ITERATION = 4
        KEY_ERROR = 5
        INVALID_STATE = 6

    _PICOVOICE_STATUS_TO_EXCEPTION = {
        PicovoiceStatuses.OUT_OF_MEMORY: MemoryError,
        PicovoiceStatuses.IO_ERROR: IOError,
        PicovoiceStatuses.INVALID_ARGUMENT: ValueError,
        PicovoiceStatuses.STOP_ITERATION: StopIteration,
        PicovoiceStatuses.KEY_ERROR: KeyError,
        PicovoiceStatuses.INVALID_STATE: ValueError,
    }

    class CPorcupine(Structure):
        pass

    def __init__(self, library_path, model_path, keyword_paths, sensitivities):
        """
        Constructor.

        :param library_path: Absolute path to Porcupine's dynamic library.
        :param model_path: Absolute path to the file containing model parameters.
        :param keyword_paths: Absolute paths to keyword model files.
        :param sensitivities: Sensitivities for detecting keywords. Each value should be a number within [0, 1]. A
        higher sensitivity results in fewer misses at the cost of increasing the false alarm rate.
        """

        if not os.path.exists(library_path):
            raise IOError("Couldn't find Porcupine's dynamic library at '%s'." % library_path)

        library = cdll.LoadLibrary(library_path)

        if not os.path.exists(model_path):
            raise IOError("Couldn't find model file at '%s'." % model_path)

        if len(keyword_paths) != len(sensitivities):
            raise ValueError("Number of keywords does not match the number of sensitivities.")

        for x in keyword_paths:
            if not os.path.exists(os.path.expanduser(x)):
                raise IOError("Couldn't find keyword file at '%s'." % x)

        for x in sensitivities:
            if not (0 <= x <= 1):
                raise ValueError('A sensitivity value should be within [0, 1].')

        init_func = library.pv_porcupine_init
        init_func.argtypes = [
            c_char_p,
            c_int,
            POINTER(c_char_p),
            POINTER(c_float),
            POINTER(POINTER(self.CPorcupine))]
        init_func.restype = self.PicovoiceStatuses

        self._handle = POINTER(self.CPorcupine)()

        status = init_func(
            model_path.encode('utf-8'),
            len(keyword_paths),
            (c_char_p * len(keyword_paths))(*[os.path.expanduser(x).encode('utf-8') for x in keyword_paths]),
            (c_float * len(keyword_paths))(*sensitivities),
            byref(self._handle))
        if status is not self.PicovoiceStatuses.SUCCESS:
            raise self._PICOVOICE_STATUS_TO_EXCEPTION[status]()

        self._delete_func = library.pv_porcupine_delete
        self._delete_func.argtypes = [POINTER(self.CPorcupine)]
        self._delete_func.restype = None

        self.process_func = library.pv_porcupine_process
        self.process_func.argtypes = [POINTER(self.CPorcupine), POINTER(c_short), POINTER(c_int)]
        self.process_func.restype = self.PicovoiceStatuses

        version_func = library.pv_porcupine_version
        version_func.argtypes = []
        version_func.restype = c_char_p
        self._version = version_func().decode('utf-8')

        self._frame_length = library.pv_porcupine_frame_length()

        self._sample_rate = library.pv_sample_rate()

    def delete(self):
        """Releases resources acquired by Porcupine."""

        self._delete_func(self._handle)

    def process(self, pcm):
        """
        Processes a frame of the incoming audio stream and emits the detection result.

        :param pcm: A frame of audio samples. The number of samples per frame can be attained by calling
        `.frame_length`. The incoming audio needs to have a sample rate equal to `.sample_rate` and be 16-bit
        linearly-encoded. Porcupine operates on single-channel audio.
        :return: Index of observed keyword at the end of the current frame. Indexing is 0-based and matches the ordering
        of keyword models provided to the constructor. If no keyword is detected then it returns -1.
        """

        if len(pcm) != self.frame_length:
            raise ValueError("Invalid frame length. expected %d but received %d" % (self.frame_length, len(pcm)))

        result = c_int()
        status = self.process_func(self._handle, (c_short * len(pcm))(*pcm), byref(result))
        if status is not self.PicovoiceStatuses.SUCCESS:
            raise self._PICOVOICE_STATUS_TO_EXCEPTION[status]()

        return result.value

    @property
    def version(self):
        """Version"""

        return self._version

    @property
    def frame_length(self):
        """Number of audio samples per frame."""

        return self._frame_length

    @property
    def sample_rate(self):
        """Audio sample rate accepted by Picovoice."""

        return self._sample_rate

import pyaudio
import struct
import pyautogui  # to press a button to play the game


key1 = r'C:\Users\aditi\OneDrive\Desktop\snek game\porcupine-master\resources\keyword_files\windows\snake_down.ppn'
key2 = r'C:\Users\aditi\OneDrive\Desktop\snek game\porcupine-master\resources\keyword_files\windows\snake_up.ppn'
key3 = r'C:\Users\aditi\OneDrive\Desktop\snek game\porcupine-master\resources\keyword_files\windows\snake_right.ppn'
key4 = r'C:\Users\aditi\OneDrive\Desktop\snek game\porcupine-master\resources\keyword_files\windows\snake_left.ppn'


library_path = r'C:\Users\aditi\OneDrive\Desktop\snek game\porcupine-master\lib\windows\amd64\libpv_porcupine.dll' 


model_file_path = r'C:\Users\aditi\OneDrive\Desktop\snek game\porcupine-master\lib\common\porcupine_params.pv'


handle = Porcupine(library_path, model_file_path,keyword_paths = [key1, key2, key3, key4] ,sensitivities = [0.5,0.5,0.5,0.5] )

def get_next_audio_frame():
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(rate=handle.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=handle.frame_length,input_device_index=None)
    pcm = audio_stream.read(handle.frame_length)
    pcm = struct.unpack_from("h" * handle.frame_length, pcm)
    return pcm

while True:
    pcm = get_next_audio_frame()
    keyword_index = handle.process(pcm)
    if keyword_index==1:
        print(keyword_index)
        pyautogui.press('up')
    if keyword_index==3:
        print(keyword_index)
        pyautogui.press('left')
    if keyword_index==2:
        print(keyword_index)
        pyautogui.press('right')
    if keyword_index==0:
        print(keyword_index)
        pyautogui.press('down')
