import io
import base64
from PIL import Image
from PIL.ImageOps import invert as pil_invert


class ImageModifier:
    def __init__(self, base64_img: str):
        img_ext, img_data = self._separate_extension(base64_img)

        self.__original = base64_img
        self.__extension = img_ext
        self.__img_data = img_data
        self.__inverted_img = None

    @property
    def original(self):
        return self.__original

    @property
    def extension(self):
        return self.__extension

    @property
    def inverted_img(self):
        if self.__inverted_img is None:
            inv_data = self._invert()
            encoded = self._encode_base64(inv_data)
            self.__inverted_img = self._attach_extension(self.extension, encoded)

        return self.__inverted_img

    def _invert(self) -> bytes:
        img = Image.open(io.BytesIO(self._decode_base64(self.__img_data)))

        if img.mode == 'RGBA':
            r, g, b, a = img.split()
            img_rgb = Image.merge('RGB', (r, g, b))

            inverted_image = pil_invert(img_rgb)
            r2, g2, b2 = inverted_image.split()

            inverted_image = Image.merge('RGBA', (r2, g2, b2, a))
        else:
            inverted_image = pil_invert(img)

        buffered = io.BytesIO()
        inverted_image.save(buffered, format=self.extension.upper())
        return buffered.getvalue()

    @staticmethod
    def _decode_base64(img_data: str) -> bytes:
        return base64.decodebytes(img_data.encode())

    @staticmethod
    def _encode_base64(image: bytes) -> str:
        """ :return encoded to base64 image """
        return base64.encodebytes(image).decode('utf-8')

    @staticmethod
    def _attach_extension(extension: str, encoded_data: str) -> str:
        return f"data:image/{extension};base64,{encoded_data}"

    @staticmethod
    def _separate_extension(image: str) -> tuple:
        # image = 'data:image/{EXTENSION};base64,{DATA}
        ext, data = image.split(',')
        ext = ext[ext.index('/')+1:-7]
        return ext, data
