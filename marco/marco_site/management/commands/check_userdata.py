from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from accounts.models import UserData


class Command(NoArgsCommand):
    help = ("Verifies that all users in the system have a UserData model"
            "associated with them.")

    def handle_noargs(self, **options):
        users = User.objects.all()

        users_updated = []

        for u in users:
            try:
                userdata = u.userdata
            except UserData.DoesNotExist:
                users_updated.append(u)
                u.userdata = UserData()
                u.userdata.save()
                u.save()

        if users_updated:
            self.stdout.write("Updated users: %s" % str(users_updated))
        else:
            self.stdout.write("No users updated.")