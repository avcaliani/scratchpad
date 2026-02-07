import platform
import sys

if __name__ == '__main__':
    py_version = platform.python_version()
    prefix = sys.prefix
    base_prefix = sys.base_prefix if py_version.startswith('3') else sys.exec_prefix
    print('------------< venv checker >------------')
    print('Python Version.: {}'.format(py_version))
    print('Prefix.........: {}'.format(prefix))
    print('Base Prefix....: {}'.format(base_prefix))
    if prefix == base_prefix:
        print('you ARE NOT using a venv!')
    else:
        print('you ARE using a venv \\o/')
    print('----------------< end >-----------------')
