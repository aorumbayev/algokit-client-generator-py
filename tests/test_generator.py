import pathlib
from itertools import chain, product

import pytest
from inflection import camelize

from algokit_client_generator import generate_client


@pytest.mark.parametrize(
    ("app", "extension"),
    chain(
        product(
            [
                "duplicate_structs",
                "hello_world",
                "life_cycle",
                "minimal",
                "state",
                "voting_round",
            ],
            ["arc32"],
        ),
        product(
            [
                "ARC56_test",
                "structs",
                "nested",
                "NFD",
                "reti",
                "zero_coupon_bond",
            ],
            ["arc56"],
        ),
    ),
)
def test_generate_clients(app: str, extension: str) -> None:
    artifacts = pathlib.Path(__file__).parent.parent / "examples" / "smart_contracts" / "artifacts"
    app_path = artifacts / app
    app_spec = app_path / f"{camelize(app)}.{extension}.json"
    generated_path = app_path / "client_generated.py"
    approved_path = app_path / f"{app}_client.py"
    generate_client(app_spec, generated_path)
    assert generated_path.read_text() == approved_path.read_text()
