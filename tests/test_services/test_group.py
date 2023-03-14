import datetime
from operator import and_

from models import UserGroup, Status
from schemas import CreateGroup
from services import create_group, add_user_in_group, read_users_group, read_user_groups
from tests.factories import UserFactory, GroupFactory


def test_create_group(session) -> None:
    user = UserFactory()
    user_data = {
        "login": user.login,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "picture": user.picture,
    }
    group = CreateGroup(title="test_title", description="test_description")
    data = create_group(session, group, user.id)
    assert data.title == "test_title"
    assert data.description == "test_description"
    assert data.status == Status.ACTIVE
    assert data.admin.login == user_data["login"]
    assert data.admin.first_name == user_data["first_name"]
    assert data.admin.last_name == user_data["last_name"]
    assert data.admin.picture == user_data["picture"]


def test_add_user_in_group(session) -> None:
    user = UserFactory()
    group = GroupFactory(admin_id=user.id)
    data = (
        session.query(UserGroup)
        .filter(and_(UserGroup.group_id == group.id, UserGroup.user_id == user.id))
        .one_or_none()
    )
    assert data is None
    add_user_in_group(session, group.id, user.id)
    data = (
        session.query(UserGroup)
        .filter(and_(UserGroup.group_id == group.id, UserGroup.user_id == user.id))
        .one_or_none()
    )
    assert data.user_id == user.id
    assert data.status == Status.ACTIVE
    assert data.group_id == group.id
    assert data.date_join.strftime("%Y-%m-%d") == datetime.date.today().strftime(
        "%Y-%m-%d"
    )


def test_read_users_group(session) -> None:
    first_user = UserFactory()
    second_user = UserFactory()
    group = GroupFactory(admin_id=first_user.id)
    add_user_in_group(session, group.id, first_user.id)
    add_user_in_group(session, group.id, second_user.id)
    data = read_users_group(session, group.id, first_user.id)
    users = [first_user, second_user]
    for data, user in zip(data.users_group, users):
        assert data.user.login == user.login
        assert data.status == Status.ACTIVE
        assert data.date_join.strftime("%Y-%m-%d") == datetime.date.today().strftime(
            "%Y-%m-%d"
        )


def test_read_user_groups(session) -> None:
    first_user = UserFactory()
    first_group = GroupFactory(admin_id=first_user.id)
    second_group = GroupFactory(admin_id=first_user.id)
    data = read_user_groups(session, first_user.id)
    assert data.user_groups == []
    add_user_in_group(session, first_group.id, first_user.id)
    add_user_in_group(session, second_group.id, first_user.id)
    data = read_user_groups(session, first_user.id)
    groups = [first_group, second_group]
    for data, group in zip(data.user_groups, groups):
        assert data.group.title == group.title
        assert data.group.status == Status.ACTIVE
