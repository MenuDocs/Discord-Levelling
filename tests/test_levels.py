import unittest  # TODO Look into using pytest


class TestLevels(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        pass

    async def test_setup(self) -> None:
        self.assertEqual(True, True)
