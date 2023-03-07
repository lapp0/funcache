import funcache
from unittest.mock import Mock


def test_filepath_cache(tmp_path):

    function_called_indicator = Mock(return_value=None)


    @funcache.filename_cache()
    def sum_files_lines(file_path):
        function_called_indicator()
        with open(file_path) as f:
            return sum([int(line) for line in f.readlines()])

    # set up file contents
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "test_filecache.txt"
    p.write_text("""1
    2
    3
    4""")
    file_path = str(p)

    # run twice, assert cache called once
    assert len(function_called_indicator.mock_calls) == 0
    result = sum_files_lines(file_path)
    assert len(function_called_indicator.mock_calls) == 1
    assert result == 10
    result = sum_files_lines(file_path)
    assert len(function_called_indicator.mock_calls) == 1  # still 1, cached
    assert result == 10

    # change file contents
    p.write_text("""10
    20
    30
    40""")

    # run again once, assert contents changed, function executed twice
    result = sum_files_lines(file_path)
    assert len(function_called_indicator.mock_calls) == 2
    assert result == 100

    # run with original file contents, assert function IS executed again
    # because original results have been purged
    p.write_text("""1
    2
    3
    4""")
    result = sum_files_lines(file_path)
    assert len(function_called_indicator.mock_calls) == 3
    assert result == 10
