from django.core.management.base import BaseCommand
from django.utils import timezone
from isety.models import Evenement, Archives

class Command(BaseCommand):
    help = 'Archive events whose date has surpassed the current date'

    def handle(self, *args, **options):
        current_date = timezone.now().date()
        events_to_archive = Evenement.objects.filter(date_enev__lt=current_date)

        for event in events_to_archive:
            # Check if the event is already archived
            if not Archives.objects.filter(event=event).exists():
                # Archive the event
                archive_reason = f"Event '{event.title}' date has surpassed the current date"
                archive_entry = Archives(event=event, reason=archive_reason)
                archive_entry.save()

                self.stdout.write(self.style.SUCCESS(f"Event '{event.title}' has been archived."))
