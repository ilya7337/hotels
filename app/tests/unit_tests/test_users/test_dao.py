from httpx import AsyncClient
import pytest
from app.users.dao import UsersDAO


@pytest.mark.parametrize(
    "id,email,exists", [(1, "fedor@moloko.ru", True), (73, None, False)]
)
async def test_find(id, email, exists):
    user = await UsersDAO.find_by_id(id)
    if exists:
        assert user
        assert user.email == email
        assert user.id == id
    else:
        assert not user
