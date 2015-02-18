from django.test import TestCase
from .models import User, Folder
import cms.plugin


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User()
        self.folder = Folder()
        self.user.save()
        self.folder.save()

    def test_relationship(self):
        self.folder.user_auth_for_delete.add(self.user)
        self.folder.save()
        print(User.objects.filter(folder_uafd__path="").count())
