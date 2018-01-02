import os
import unittest
import pickle

import ytad.persisted
import ytad.test_support


class TestPersisted(unittest.TestCase):
    def test__full_cycle(self):
        with ytad.test_support.temp_path() as path:
            filepath = os.path.join(path, 'state')

            id_ = 'MY-ID'
            hash_ = 'MY-HASH'

            with ytad.test_support.environment(
                    YTAD_STATE_FILEPATH=filepath):
                p = ytad.persisted.Persisted()

                metadata = { 'aa': 11 }
                p.set_playlist_state(id_, hash_, metadata)

                # Check that the file was created and has the right contents.

                hash_, timestamp_phrase, recorded_metadata = p.get_playlist_state(id_)

                self.assertEquals(recorded_metadata, metadata)

                with open(filepath) as f:
                    actual = pickle.load(f)

                expected = {id_: (hash_, timestamp_phrase, metadata)}
                self.assertEquals(actual, expected)

                # Check that the same hash is interpreted as a no-change.

                has_changed, timedelta, recorded_metadata = p.has_changed(id_, hash_, metadata)
                self.assertFalse(has_changed)
                self.assertTrue(0.00 < timedelta.total_seconds() < 1.00)

                # Run the check while allowing updates and verify that no
                # update happened.

                has_changed, timedelta, recorded_metadata = p.has_changed(id_, hash_, metadata)

                self.assertFalse(has_changed)
                self.assertTrue(0.00 < timedelta.total_seconds() < 1.00)

                # Verify that a new hash is seen as a change while not allowing
                # updates.

                has_changed, timedelta, recorded_metadata = \
                    p.has_changed(
                        id_,
                        'DIFFERENT-HASH',
                        metadata)

                self.assertTrue(has_changed)
                self.assertTrue(0.00 < timedelta.total_seconds() < 1.00)

                with open(filepath) as f:
                    actual2 = pickle.load(f)

                self.assertEquals(actual2, actual)

                # Verify that a new hash is seen as a change and *now* allow an
                # update.

                updated_metadata = { 'bb': 22 }

                has_changed, timedelta, recorded_metadata = \
                    p.has_changed(
                        id_,
                        'DIFFERENT-HASH',
                        updated_metadata,
                        allow_update=True)

                self.assertTrue(has_changed)
                self.assertTrue(0.00 < timedelta.total_seconds() < 1.00)

                # The metadata returned is the old metadata.
                self.assertEquals(recorded_metadata, metadata)

                hash_, timestamp_phrase, recorded_metadata = p.get_playlist_state(id_)
                self.assertEquals(hash_, 'DIFFERENT-HASH')

                with open(filepath) as f:
                    actual = pickle.load(f)

                expected = {id_: (hash_, timestamp_phrase, updated_metadata)}
                self.assertEquals(actual, expected)

    def test__fault_and_update(self):
        with ytad.test_support.temp_path() as path:
            filepath = os.path.join(path, 'state')

            hash_ = 'MY-HASH'

            with ytad.test_support.environment(
                    YTAD_STATE_FILEPATH=filepath):
                p = ytad.persisted.Persisted()

                # Check for a missing item.

                has_changed, timestamp, metadata = \
                    p.has_changed('MISSING-ID', 'SOME-HASH', {})

                self.assertTrue(has_changed)
                self.assertIsNone(timestamp)
                self.assertIsNone(metadata)

                # Verify it still doesn't exist.

                self.assertFalse(os.path.exists(filepath))

                # Check for a missing item but induce an update.

                has_changed, timestamp, metadata = \
                    p.has_changed(
                        'SOME-ID',
                        'SOME-HASH',
                        {},
                        allow_update=True)

                self.assertTrue(has_changed)
                self.assertIsNone(timestamp)
                self.assertIsNone(metadata)

                self.assertTrue(os.path.exists(filepath))
