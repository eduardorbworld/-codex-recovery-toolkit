import sqlite3
import tempfile
import unittest
from pathlib import Path
from recovery import recover, snapshot, NAME

class RecoveryTests(unittest.TestCase):
    def test_copy_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root/"source"
            source.mkdir()
            db = source/NAME
            c = sqlite3.connect(db)
            c.execute("create table sample (id integer)")
            c.commit()
            c.close()
            before = snapshot(db)
            backup = recover(db,root)
            self.assertEqual(snapshot(db),before)
            self.assertEqual(snapshot(backup/NAME),before)
            recover(db,root,True)
    def test_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                recover(Path(tmp)/NAME,Path(tmp))
