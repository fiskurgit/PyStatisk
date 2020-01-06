from statisk import Log


def test_title(capsys):
    Log.title()
    captured = capsys.readouterr()
    assert str(captured.out).__contains__(Log.ascii_title)
