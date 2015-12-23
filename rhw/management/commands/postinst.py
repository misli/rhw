from django.core.management.base import BaseCommand, CommandError
from subprocess import call

class Command(BaseCommand):
    help = 'Runs post installations procedures (sets up SELinux)'

    def handle(self, *args, **options):
        call(['semanage', 'fcontext', '-a', '-t', 'httpd_sys_rw_content_t', '/var/lib/rhw/data(/.*)?'])
        call(['restorecon', '-R', '/var/lib/rhw/data'])
        call(['setsebool', '-P', 'httpd_can_network_connect', 'on'])
