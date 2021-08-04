import uuid
import unittest

from fastapi.testclient import TestClient

import models
import schemas
from main import app


class ModelsImageTestCase(unittest.TestCase):
    def test_str(self):
        base64_image = 'data:image/png;base64,GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
        img = models.Image(id=2987, uuid=uuid.uuid1(), is_negative=True, image=base64_image)
        exp_str = f"ID: {img.id}, is_neg: {img.is_negative}, uuid: {img.uuid}"

        self.assertIsInstance(str(img), str)
        self.assertEqual(str(img), exp_str)


class SchemasGetPairsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        base64_image1 = 'data:image/png;base64,AAAAAAAAAAAAAAAAAAAAAAAAAA'
        base64_image2 = 'data:image/png;base64,BBBBBBBBBBBBBBBBBBBBBBBBBB'

        uuid1 = '291e734e-f500-11eb-a20a-0242ac120003'
        uuid2 = '2b8cd080-f500-11eb-a20a-0242ac120003'

        cls.images = [
            schemas.ImageOut(uuid=uuid1, image=base64_image1, is_negative=True),
            schemas.ImageOut(uuid=uuid1, image=base64_image1, is_negative=False),
            schemas.ImageOut(uuid=uuid2, image=base64_image2, is_negative=True),
            schemas.ImageOut(uuid=uuid2, image=base64_image2, is_negative=False),
        ]

    def test_get_pairs1(self):
        in_imgs = [self.images[0], self.images[1]]
        exp_result = [schemas.ImagePair(
            uuid=self.images[0].uuid, image=self.images[1].image, neg_image=self.images[0].image,
        )]
        result = schemas.get_pairs(in_imgs)

        self.assertListEqual(exp_result, result)

    def test_get_pairs1_desc(self):
        in_imgs = [self.images[1], self.images[0]]
        exp_result = [schemas.ImagePair(
            uuid=self.images[0].uuid, image=self.images[1].image, neg_image=self.images[0].image,
        )]
        result = schemas.get_pairs(in_imgs)

        self.assertListEqual(exp_result, result)

    def test_get_pairs2(self):
        in_imgs = [self.images[0], self.images[1], self.images[2], self.images[3]]
        exp_result = [
            schemas.ImagePair(uuid=self.images[0].uuid, image=self.images[1].image, neg_image=self.images[0].image),
            schemas.ImagePair(uuid=self.images[2].uuid, image=self.images[3].image, neg_image=self.images[2].image),
        ]
        result = schemas.get_pairs(in_imgs)

        self.assertListEqual(exp_result, result)

    def test_get_pairs2_desc(self):
        in_imgs = [self.images[1], self.images[0], self.images[3], self.images[2]]
        exp_result = [
            schemas.ImagePair(uuid=self.images[0].uuid, image=self.images[1].image, neg_image=self.images[0].image),
            schemas.ImagePair(uuid=self.images[2].uuid, image=self.images[3].image, neg_image=self.images[2].image),
        ]
        result = schemas.get_pairs(in_imgs)

        self.assertListEqual(exp_result, result)


class ApiTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_index_page(self):
        with open('frontend/index.html', encoding='utf-8') as file:
            html_content = ''.join(file.readlines())

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'text/html; charset=utf-8')
        self.assertEqual(response.content, html_content.encode())

    def test_negative_image(self):
        image = {'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACXBIWXMAAA7zAAAO8wEcU5k6AAAAEXRFWHRUaXRsZQBQREYgQ3JlYXRvckFevCgAAAATdEVYdEF1dGhvcgBQREYgVG9vbHMgQUcbz3cwAAAALXpUWHREZXNjcmlwdGlvbgAACJnLKCkpsNLXLy8v1ytISdMtyc/PKdZLzs8FAG6fCPGXryy4AAAACklEQVQIHWNgAAAAAgABz8g15QAAAABJRU5ErkJggg=='}
        exp_json = {
            'image': 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAAAAAA6fptVAAAACklEQVR4nGP4DwABAQEAsTj2FAAA\nAABJRU5ErkJggg==\n',
            'uuid': '',
            'is_negative': True,
        }
        response = self.client.post('/negative_image', json=image)
        json = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        self.assertListEqual(list(json.keys()), list(exp_json.keys()))
        self.assertEqual(json['image'], exp_json['image'])
        self.assertEqual(json['is_negative'], True)
        # uuid is correct
        uuid_ = uuid.UUID(json['uuid'])
