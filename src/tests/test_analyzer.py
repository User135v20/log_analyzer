import pytest

from src.log_analyzer.analyzer import LogAnalyzerClass

request1_url = '/api/v2/banner/25019354'
request1_time = 0.390
request1_parsed_line = {
    'another_field': '1498697422-2190034393-4708-9752759" "dc7161be3',
    'date_time': '29/Jun/2017:03:50:22 +0300',
    'http_version': '1.1', 'ip': '1.196.116.32',
    'method': 'GET', 'referrer': '-',
    'request_time': f'{request1_time}',
    'size': '927',
    'some_field': '-',
    'status': '200',
    'url': request1_url,
    'user_agent': 'Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5',
    'user_id': '-'
}

request2_url = request1_url+'/v2'
request2_time = request1_time+0.1
request2_parsed_line = {
    'another_field': '1498697422-2190034393-4708-9752759" "dc7161be3',
    'date_time': '29/Jun/2017:03:50:22 +0300',
    'http_version': '1.1', 'ip': '1.196.116.32',
    'method': 'GET', 'referrer': '-',
    'request_time': f'{request2_time}',
    'size': '927',
    'some_field': '-',
    'status': '200',
    'url': request2_url,
    'user_agent': 'Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5',
    'user_id': '-'
}
@pytest.mark.parametrize(
    "count, time, log_info,  lines",
    [
        (
                1,
                request1_time,
                {request1_url: {'count': 1, 'times': [request1_time], 'url': request1_url}},
                [request1_parsed_line]
        ),
        (
                2,
                2 * request1_time,
                {request1_url: {'count': 2, 'times': [request1_time, request1_time], 'url': request1_url}},
                [request1_parsed_line, request1_parsed_line]
        ),
        (
                3,
                2 * request1_time+request2_time,
                {
                    request1_url: {'count': 2, 'times': [request1_time, request1_time], 'url': request1_url},
                    request2_url: {'count': 1, 'times': [request2_time], 'url': request2_url}
                 },
                [request1_parsed_line, request1_parsed_line, request2_parsed_line]
        ),

])
def test_add_line(count, time, log_info, lines):
    analyzer = LogAnalyzerClass()
    for line in lines:
        analyzer.add_line(line)
    assert analyzer.count_lines == count
    assert analyzer.log_info == log_info
    assert analyzer.all_requests_time == time




@pytest.mark.parametrize(
    "lines, statistics",
    [
        (
                [request1_parsed_line],
                [
                    {
                        'count': 1,
                        'count_perc': 100.0,
                        'time_avg': 0.39,
                        'time_max': 0.39,
                        'time_med': 0.39,
                        'time_perc': 100.0,
                        'time_sum': 0.39,
                        'url': '/api/v2/banner/25019354'
                    }
                ]
        ),
        (
            [request1_parsed_line, request1_parsed_line,],
            [
                {
                    'count': 2,
                     'count_perc': 100.0,
                     'time_avg': 0.39,
                     'time_max': 0.39,
                     'time_med': 0.39,
                     'time_perc': 100.0,
                     'time_sum': 0.78,
                     'url': '/api/v2/banner/25019354'
                }
            ]
        ),
        (
            [request1_parsed_line, request1_parsed_line, request2_parsed_line],
            [
                {
                    'count': 2,
                    'count_perc': 66.667,
                    'time_avg': 0.39,
                    'time_max': 0.39,
                    'time_med': 0.39,
                    'time_perc': 61.417,
                    'time_sum': 0.78,
                    'url': '/api/v2/banner/25019354'
                },
                {
                    'count': 1,
                    'count_perc': 33.333,
                    'time_avg': 0.49,
                    'time_max': 0.49,
                    'time_med': 0.49,
                    'time_perc': 38.583,
                    'time_sum': 0.49,
                    'url': '/api/v2/banner/25019354/v2'
                }]
        )

])
def test_get_statistic(lines, statistics):
    analyzer = LogAnalyzerClass()
    for line in lines:
        analyzer.add_line(line)
    assert list(analyzer.get_statistic()) == list(statistics)