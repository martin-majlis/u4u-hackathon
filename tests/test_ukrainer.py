import pytest

from ukrainer import extract_texts


@pytest.mark.parametrize(
    "content,expected",
    [
        pytest.param(
            """
        <div>
            <p>A</p>
        </div>
        <div class="text-section">
            <b>C</b>
            <p>D</p>
        </div>
        """,
            ["D"],
            id="extract only concrete tags and classes",
        ),
        pytest.param(
            """
        <div class="text-section">
            <p>A</p>
            <p>B</p>
        </div>
        <div class="text-section">
            <p>C</p>
            <p>D</p>
        </div>
        """,
            ["A", "B", "C", "D"],
            id="plain text",
        ),
        pytest.param(
            """
        <div class="text-section">
            <p><b>A</b> A <i>A</i></p>
            <p><span class="foo">B</span></p>
        </div>
        """,
            ["A A A", "B"],
            id="content with tags",
        ),
        pytest.param(
            """
        <div class="text-section">
            <h1>H1</h1>
            <p>P1</p>
            <h2>H2</h2>
            <p>P2</p>
        </div>
        """,
            ["H1", "H2", "P1", "P2"],
            id="content with headers",
        ),
    ],
)
def test_eval(content, expected):
    assert list(extract_texts(content)) == expected
