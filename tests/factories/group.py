import datetime

import factory

from models import Group, UserGroup
from .base_factory import BaseFactory


class GroupFactory(BaseFactory):
    id = factory.Sequence(lambda n: n)
    title = factory.Faker("word")
    description = factory.Faker("word")
    admin_id = None

    class Meta:
        model = Group


class UserGroupFactory(BaseFactory):
    user_id = factory.Sequence(lambda n: n)
    group_id = factory.Sequence(lambda n: n)
    date_join = datetime.date.today()

    class Meta:
        model = UserGroup
