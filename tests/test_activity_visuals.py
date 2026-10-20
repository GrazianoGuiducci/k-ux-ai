"""Domain assets must be portable, local and reproducibly copied by the builder."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('griglia_builder', Path(__file__).parents[1] / 'tools/build_public_griglia.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ActivityAssets(unittest.TestCase):
    def test_optional_profile_and_colour_only_identity(self):
        self.assertEqual(builder.activity_visual_assets({}, Path('PROFILE.json')), {})
        self.assertEqual(builder.activity_visual_assets({'activityVisuals': {'fare': {'color': '#639241'}}}, Path('PROFILE.json')), {})

    def test_local_asset_resolution_and_missing_asset(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            image = root / 'assets/fare.webp'
            image.parent.mkdir()
            image.write_bytes(b'asset-bytes')
            profile = {'activityVisuals': {'fare': {'color': '#639241', 'image': 'assets/fare.webp'}}}
            self.assertEqual(builder.activity_visual_assets(profile, root / 'PROFILE.json'), {'assets/fare.webp': image.resolve()})
            image.unlink()
            with self.assertRaisesRegex(ValueError, 'Missing domain'):
                builder.activity_visual_assets(profile, root / 'PROFILE.json')

    def test_remote_or_escaping_images_are_not_compiled_into_portable_profiles(self):
        for image in ['https://example.com/pic.webp', '../assets/fare.webp', 'assets/../../fare.webp']:
            with self.subTest(image=image), self.assertRaisesRegex(ValueError, 'local assets'):
                builder.activity_visual_assets({'activityVisuals': {'fare': {'color': '#639241', 'image': image}}}, Path('PROFILE.json'))

    def test_empty_canvas_vector_is_optional_local_and_portable(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            image = root / 'assets/canvas-empty.svg'
            image.parent.mkdir()
            image.write_text('<svg xmlns="http://www.w3.org/2000/svg"/>', encoding='utf-8')
            profile = {'emptyCanvas': {'image': 'assets/canvas-empty.svg'}}
            self.assertEqual(builder.activity_visual_assets(profile, root / 'PROFILE.json'),
                             {'assets/canvas-empty.svg': image.resolve()})
        for image in ['https://example.com/empty.svg', '../empty.svg', 'assets/../../empty.svg']:
            with self.subTest(image=image), self.assertRaisesRegex(ValueError, 'local assets'):
                builder.activity_visual_assets({'emptyCanvas': {'image': image}}, Path('PROFILE.json'))


if __name__ == '__main__':
    unittest.main()
