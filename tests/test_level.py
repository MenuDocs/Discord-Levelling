import unittest  # TODO Look into using pytest

# noinspection PyUnresolvedReferences
from discord.ext.levelling import Level


class TestLevels(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        pass

    async def test_init(self) -> None:
        with self.assertRaises(ValueError):
            Level(cache=1)

        with self.assertRaises(ValueError):
            Level(data_store=1)
