import pytest
from orcestradownloader.main import hello, main;


def test_say_hello():
    assert hello() == (
        "Hello from orcestradownloader, [bold magenta]World[/bold magenta]!", ":vampire:"
    )

def test_main(capsys):
    """Test the main function."""
    main()
    captured = capsys.readouterr()
    assert "orcestradownloader" in captured.out
    assert "World" in captured.out
    assert "🧛" in captured.out

if __name__ == "__main__":
    pytest.main()
