import tempfile
import unittest
from pathlib import Path

from install import BLOCK, update


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="zen notch ")
        self.addCleanup(self.temp.cleanup)
        self.profile = Path(self.temp.name)
        (self.profile / "prefs.js").touch()
        self.chrome = self.profile / "chrome"
        self.chrome.mkdir()
        self.css = self.chrome / "userChrome.css"

    def test_round_trip_and_idempotency(self):
        for original in (b"", b"/* existing */\r\n:root { color: red; }\r\n",
                         b'@charset "UTF-8";\n/* existing */\n',
                         '\ufeff/* Unicode: café */\n'.encode()):
            with self.subTest(original=original):
                self.css.write_bytes(original)
                update(self.profile, "install")
                update(self.profile, "install")
                self.assertEqual(self.css.read_text().count(BLOCK), 1)
                self.assertEqual((self.chrome / "zen-notch/zen-notch.css").read_bytes(),
                                 Path(__file__).with_name("zen-notch.css").read_bytes())
                update(self.profile, "uninstall")
                update(self.profile, "uninstall")
                self.assertEqual(self.css.read_bytes(), original)
                self.assertFalse((self.chrome / "zen-notch").exists())

    def test_refuses_unmanaged_directory(self):
        (self.chrome / "zen-notch").mkdir()
        with self.assertRaises(ValueError):
            update(self.profile, "install")

    def test_preserves_added_files_and_styles(self):
        update(self.profile, "install")
        extra = self.chrome / "zen-notch/notes.txt"
        extra.write_text("keep")
        with self.css.open("a") as stream:
            stream.write("/* added after installation */\n")
        update(self.profile, "uninstall")
        self.assertEqual(extra.read_text(), "keep")
        self.assertEqual(self.css.read_text(), "/* added after installation */\n")

    def test_refuses_symlink(self):
        other = self.profile / "other.css"
        other.write_text("keep")
        self.css.symlink_to(other)
        with self.assertRaises(ValueError):
            update(self.profile, "install")
        self.assertEqual(other.read_text(), "keep")

    def test_invalid_profile(self):
        with self.assertRaises(ValueError):
            update(self.profile / "missing", "install")


if __name__ == "__main__":
    unittest.main()
