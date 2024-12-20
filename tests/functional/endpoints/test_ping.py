from http import HTTPStatus

import pytest


@pytest.mark.asyncio
async def test_ping(make_get_request):
    status, body = await make_get_request("/ping")
    assert status == HTTPStatus.OK
    assert body == {"message": "pong"}
