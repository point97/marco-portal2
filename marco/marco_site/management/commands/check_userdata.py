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
                u.userdata = UserData()

            if not u.userdata.real_name:
                users_updated.append(u)
                u.userdata.real_name = ' '.join([u.first_name, u.last_name])
                u.userdata.preferred_name = u.first_name
                u.userdata.save()
                u.save()

        if users_updated:
            self.stdout.write("Updated users: %s" % str(users_updated))
        else:
            self.stdout.write("No users updated.")