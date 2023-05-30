from doit.task import clean_targets
import shutil


DOIT_CONFIG = {'default_tasks': ['html']}


def task_html():
    """Create documentation"""
    return {
		'actions': ['make -C docs html'],
		'targets': ['docs/build'],
		'clean': [clean_targets, lambda: shutil.rmtree('docs/build')],
		}


def task_wheel_client():
    """Build client wheel"""
    return {
        'actions': ['python3 -m build -nw moodclient'],
        'file_dep': ['moodclient/moodclient/ClientCmd.py', 'moodclient/pyproject.toml'],
        'targets': ['moodclient/dist/*.whl'],
        'clean': [(shutil.rmtree, ['moodclient/dist']), (shutil.rmtree, ['moodclient/build']), (shutil.rmtree, ['moodclient/MoodClient.egg-info'])],
        }


def task_wheel_server():
    """Build server wheel"""
    return {
        'actions': ['python3 -m build -nw moodserver'],
        'file_dep': ['moodserver/moodserver/Server.py', 'moodserver/pyproject.toml'],
        'targets': ['moodserver/dist/*.whl'],
        'clean': [(shutil.rmtree, ['moodserver/dist']), (shutil.rmtree, ['moodserver/build']), (shutil.rmtree, ['moodserver/MoodServer.egg-info'])],
        }