from src.log_analyzer.file_manager import parse_line, get_filename, is_nginx_log_file

from unittest.mock import MagicMock, patch
import pytest

valid_line = '1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390'
expected_value = {
    'another_field': '1498697422-2190034393-4708-9752759" "dc7161be3',
    'date_time': '29/Jun/2017:03:50:22 +0300',
    'http_version': '1.1', 'ip': '1.196.116.32',
    'method': 'GET', 'referrer': '-',
    'request_time': '0.390',
    'size': '927',
    'some_field': '-',
    'status': '200',
    'url': '/api/v2/banner/25019354',
    'user_agent': 'Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5',
    'user_id': '-'
}

@pytest.mark.parametrize("line, expected", [
    ("", None),
    (valid_line, expected_value),
    ("another_invalid_line", None),
])
def test_parse_line_cases(line, expected):
    with patch('src.log_analyzer.file_manager._get_logger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_logger.warning.return_value = None
        mock_get_logger.return_value = mock_logger
        result = parse_line(line)
        assert result == expected


class FakePath:
    def __init__(self, name, is_file=True):
        self.name = name
        self._is_file = is_file

    def is_file(self):
        return self._is_file

@pytest.mark.parametrize("expected, fake_files", [
    ("nginx-access-ui.log-20270710", [
        FakePath("nginx-access-ui.log-20170630"),
        FakePath("nginx-access-ui.log-20270630"),
        FakePath("random-file.txt", is_file=True),
        FakePath("nginx-access-ui.log-20270710"),
        FakePath("some_directory", is_file=False)
    ]),
    ("nginx-access-ui.log-20270810.gz", [
        FakePath("nginx-access-ui.log-20170630"),
        FakePath("nginx-access-ui.log-20270810.gz"),
        FakePath("random-file.txt", is_file=True),
        FakePath("nginx-access-ui.log-20270710"),
        FakePath("some_directory", is_file=False)
    ]),
    (None, [
            FakePath("random-file.txt", is_file=True),
            FakePath("some_directory", is_file=False)
        ]),
])
def test_get_filename_with_mocked_iterdir(fake_files, expected):
    with patch("src.log_analyzer.file_manager.Path") as mock_path_class, \
         patch('src.log_analyzer.file_manager._get_logger') as mock_get_logger:
        mock_path_instance = MagicMock()
        mock_path_instance.iterdir.return_value = fake_files
        mock_path_class.return_value = mock_path_instance
        mock_logger = MagicMock()
        mock_logger.warning.return_value = None
        mock_get_logger.return_value = mock_logger

        result = get_filename("some/dir")
        assert result == expected


@pytest.mark.parametrize("filename, expected", [
    ("nginx-access-ui.log-20170630", True),
    ("nginx-access-ui.log-20170630.gz", True),
    ("nginx-access-ui.log-20231201", True),
    ("nginx-access-ui.log-20231201.gz", True),
    ("nginx-access-ui.log-20170630.txt", False),
    ("nginx-access-ui.log-2017063", False),
    ("nginx-access-ui.log-201706301", False),
    ("nginx-access-ui.log-2017-06-30", False),
    ("nginx-access-ui.log-20170630.gz.bak", False),
    ("nginx-access-ui.log", False),
    ("nginx-access-ui.log.gz", False),
    ("access-ui.log-20170630", False),
    ("nginx-access-ui.log-20170630.gz.gz", False),
    ("", False),
])
def test_is_nginx_log_file(filename, expected):
    result = is_nginx_log_file(filename)
    assert result == expected

