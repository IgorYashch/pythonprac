def task_test():
    """Preform tests."""
    yield {'actions': ['coverage run -m unittest -v'], 'name': "run"}
    yield {'actions': ['coverage report'], 'verbosity': 2, 'name': "report"}


def task_pot():
    """Re-create .pot ."""
    return {
            'actions': ['pybabel extract -o DateTime.pot AppBase'],
            'file_dep': glob.glob('AppBase/*.py'),
            'targets': ['DateTime.pot'],
           }


def task_po():
    """Update translations."""
    return {
            'actions': ['pybabel update -D DateTime -d po -i DateTime.pot'],
            'file_dep': ['DateTime.pot'],
            'targets': ['po/ru/LC_MESSAGES/DateTime.po'],
           }
