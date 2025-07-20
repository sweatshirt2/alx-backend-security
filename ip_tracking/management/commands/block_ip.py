from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP
import ipaddress

class Command(BaseCommand):
    help = 'Blocks an IP address by adding it to the BlockedIP list.'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block.')

    def handle(self, *args, **options):
        ip_str = options['ip_address']
        try:
            ipaddress.ip_address(ip_str)
        except ValueError:
            raise CommandError(f"'{ip_str}' is not a valid IP address.")

        if BlockedIP.objects.filter(ip_address=ip_str).exists():
            self.stdout.write(self.style.WARNING(f"IP address {ip_str} is already blocked."))
        else:
            BlockedIP.objects.create(ip_address=ip_str)
            self.stdout.write(self.style.SUCCESS(f"Successfully blocked IP address {ip_str}."))
