from unittest.mock import patch
from Scrapper.tasks import main, scrapper, websites


@patch('Scrapper.tasks.main')
def test_main(mock_scrapper_delay):
    main()

    for website, method in websites.items():
        mock_scrapper_delay.assert_any_call(website, method)

    assert mock_scrapper_delay.call_count == len(websites)
