import pytest
from starlette.exceptions import HTTPException

from models import Category, CategoryGroups
from enums import GroupStatusEnum
from schemas import CreateCategory
from services import create_category
from tests.factories import (
    CategoryFactory,
    GroupFactory,
    UserFactory,
    UserGroupFactory,
    IconFactory,
    ColorFactory,
    IconColorFactory,
)


def test_create_category(session, dependence_factory) -> None:
    factories = dependence_factory
    category = CreateCategory(title="BoOK")
    data = create_category(
        session, factories["first_user"].id, factories["first_group"].id, category
    )
    db_category = session.query(Category).filter_by(id=data.id).one_or_none()
    assert db_category is not None
    db_category_group = (
        session.query(CategoryGroups).filter_by(category_id=data.id).one_or_none()
    )
    assert db_category_group is not None


def test_create_category_not_admin(session, dependence_factory) -> None:
    factories = dependence_factory
    category = CreateCategory(title="Book")
    with pytest.raises(HTTPException) as ex_info:
        create_category(session, 9999, factories["first_group"].id, category)
    assert "You are not admin in this group!" in str(ex_info.value.detail)


def test_create_category_inactive_group(session) -> None:
    user = UserFactory()
    icon = IconFactory()
    color = ColorFactory()
    icon_color = IconColorFactory(icon_id=icon.id, color_id=color.id)
    group = GroupFactory(
        admin_id=user.id, status=GroupStatusEnum.INACTIVE, icon_color_id=icon_color.id
    )
    UserGroupFactory(
        user_id=user.id,
        group_id=group.id,
        status=GroupStatusEnum.INACTIVE,
    )
    category = CreateCategory(title="Book")
    with pytest.raises(HTTPException) as ex_info:
        create_category(session, user.id, group.id, category)
    assert "Group is not active!" in str(ex_info.value.detail)


def test_create_category_exist(session) -> None:
    user = UserFactory()
    icon = IconFactory()
    color = ColorFactory()
    icon_color = IconColorFactory(icon_id=icon.id, color_id=color.id)
    group = GroupFactory(admin_id=user.id, icon_color_id=icon_color.id)
    category = CreateCategory(title="BoOK")
    create_category(session, user.id, group.id, category)
    category = CreateCategory(title="BOoK")
    with pytest.raises(HTTPException) as ex_info:
        create_category(session, user.id, group.id, category)
    assert "The category is already in this group!" in str(ex_info.value.detail)


def test_add_exist_category_in_group(session, dependence_factory) -> None:
    factories = dependence_factory
    CategoryFactory(title="book")
    category = CreateCategory(title="BOOK")
    create_category(
        session,
        dependence_factory["first_user"].id,
        factories["first_group"].id,
        category,
    )
    db_category_group = session.query(CategoryGroups).all()
    assert len(db_category_group) == 1
