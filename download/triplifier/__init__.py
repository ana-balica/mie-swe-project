import os
from jinja2 import FileSystemLoader, Environment

pwd = os.getcwd()
template_dir = os.path.join(pwd, 'templates/')
env = Environment(loader=FileSystemLoader(template_dir))
