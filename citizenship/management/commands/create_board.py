from django.core.management.base import BaseCommand, CommandError

from ..factory.factories import BoardFactory, RoleFactory, BoardMemberFactory


class Command(BaseCommand):
    help = 'Create a new Board using the BoardFactory'

    def handle(self, *args, **kwargs):
        try:
            # Use the factory to create a Board instance
            chair_person = RoleFactory(name='Chairperson')
            police_officer = RoleFactory(name='Police Officer')
            deputy_chair = RoleFactory(name='Deputy Chair')
            citizenship_officer = RoleFactory(name='Citizenship Officer')
            board = BoardFactory(
                quorum_roles=[chair_person, police_officer, deputy_chair, citizenship_officer])
            self.stdout.write(self.style.SUCCESS(f'Successfully created board "{board.name}"'))

            chair_person_member = BoardMemberFactory(board=board, role=chair_person)
            self.stdout.write(self.style.SUCCESS(f'Successfully created member chair person member."'))

            police_officer_member = BoardMemberFactory(board=board, role=police_officer)
            self.stdout.write(self.style.SUCCESS(f'Successfully created member police officer member ."'))

            deputy_chair_member = BoardMemberFactory(board=board, role=deputy_chair)
            self.stdout.write(self.style.SUCCESS(f'Successfully created member deputy chair member ."'))

            citizenship_officer = BoardMemberFactory(board=board, role=citizenship_officer)
            self.stdout.write(self.style.SUCCESS(f'Successfully created member citizenship officer ."'))

            self.stdout.write(self.style.SUCCESS(f'Successfully created board "{board.name}"'))
        except Exception as e:
            raise CommandError(f'Error creating board, member, roles: {e}')
