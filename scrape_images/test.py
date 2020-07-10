import asyncio
import unittest
from unittest import mock
import scrape_images.concurrent_image_scraper as c



def _run(coro):
    """Run the given coroutine."""
    return asyncio.get_event_loop().run_until_complete(coro)


def AsyncMock(*args, **kwargs):
    """Create an async function mock."""
    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


class MyTestCase(unittest.TestCase):
    @mock.patch('concurrent_image_scraper.create_source_selenium', new=AsyncMock())
    def test_create_source_selenium(self):
        pass_ = True
        source = _run(c.create_source_selenium('http://127.0.0.1:5000/static/test.html'))
        # inspected element and found these random strings
        class_name_1 = "rpBJOHq2PR60pnwJlUyP0"
        class_name_2 = "hciOr5UGrnYrZxB11tX9s"
        src = 'src="https://c.aaxads.com/pxusr.gif"'
        self.assertIn(class_name_1, source)
        self.assertIn(class_name_2, source)
        self.assertIn(src, source)



if __name__ == '__main__':
    unittest.main()
