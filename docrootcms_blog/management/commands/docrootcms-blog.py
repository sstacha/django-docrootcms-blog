from django.core.management.base import BaseCommand
from argparse import RawTextHelpFormatter
import os
import shutil
import pathlib
from datetime import datetime
from distutils.sysconfig import get_python_lib


class Command(BaseCommand):
    help = """
    usage: ./manage.py docrootcms-blog [option]
    --------------------------------------
    example: ./manage.py docrootcms-blog develop

    options
    --------
    develop - copies the docrootcms-blog module in the virtual environment to local project for development
    """
    testing = False

    def create_parser(self, *args, **kwargs):
        parser = super(Command, self).create_parser(*args, **kwargs)
        parser.formatter_class = RawTextHelpFormatter
        return parser

    def add_arguments(self, parser):
        parser.add_argument('option', nargs='+', type=str)


    @staticmethod
    def get_module_path():
        # first try and get it from distutils (since pyenv symlinks to root version and site doesnt work for virtualenv)
        module_path = pathlib.Path(get_python_lib()) / 'docrootcms-blog'
        print(f'module path from DISTUTILS.SYSCONFIG: {module_path}')
        if not os.path.exists(module_path):
            module_path = pathlib.Path(os.__file__).parent / 'site-packages' / 'docrootcms-blog'
            print(f'module path from runtime: {module_path}')
        if not os.path.exists(module_path):
            # for debugging lets next try to find the app locally to copy from
            module_path = pathlib.Path('docrootcms-blog')
            print(f'module path from project: {module_path}')
        if not os.path.exists(module_path):
            raise ModuleNotFoundError(
                'Module docrootcms-blog was not installed.  Install using pip install django-docrootcms-blog and try again.')
        return module_path


    def develop(self):
        success_instructions = """
        Successfully Installed cms application for development.

        """
        # check that docroot-cms app doesn't already exist locally
        if os.path.exists('docrootcms-blog'):
            self.stderr.write(self.style.ERROR('docrootcms-blog application already exists locally for development!'))
            return 'Remove the existing directory to reload a newer version.'
        else:
            self.stdout.write(f'installing docrootcms-blog from virtual environment...')
            module_path = self.get_module_path()
            local_path = pathlib.Path() / 'docrootcms-blog'
            print(f'local path: {local_path}')
            shutil.copytree(module_path, local_path, dirs_exist_ok=True)
            self.stdout.write(
                self.style.SUCCESS(f'Successfully copied {module_path} to {local_path}'))
            return success_instructions

    def handle(self, *args, **options):
        if "develop" in options['option']:
            self.stdout.write(self.style.WARNING(f'{self.develop()}'))
        else:
            self.stdout.write(self.style.SUCCESS(self.help))
