import argparse
import json
import os
import re
import subprocess
import shlex
import pathlib


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--compile_JSON'
        , required=True
        , help='path to compile commands JSON file'
    )

    parser.add_argument(
        '--link_JSON'
        , required=True
        , help='path to link commands JSON file'
    )

    args = parser.parse_args()

    with open(args.compile_JSON, "r") as read_file:
        compile_data = json.load(read_file)

    with open(args.link_JSON, "r") as read_file:
        link_data = json.load(read_file)
    cur_dir = pathlib.Path(__file__).parent.absolute()

    for elem in compile_data:
        os.chdir(cur_dir)
        build = re.findall(r'build\S*', elem.get('directory'))[0]
        for dir in build.split('\\'):
            if not os.path.exists(dir):
                os.makedirs(dir)
            os.chdir(dir)

        path_to_obj = re.findall(r'(\S*)\.o', elem.get('command'))
        for directories in path_to_obj:
            for dir in directories.split('\\'):
                if not os.path.exists(dir):
                    os.makedirs(dir)

        command = shlex.split(elem.get('command'))
        process = subprocess.Popen(command
                                   , stdout=subprocess.PIPE
                                   , stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        return_code = process.returncode
        print(process)
        print(stderr)
        assert (stderr == b'')
        assert (return_code == 0)

    for elem in link_data:
        os.chdir(cur_dir)
        build = re.findall(r'build\S*', elem.get('directory'))[0]
        for dir in build.split('\\'):
            if not os.path.exists(dir):
                os.makedirs(dir)
            os.chdir(dir)

        command = shlex.split(elem.get('command'))
        process = subprocess.Popen(command
                                   , stdout=subprocess.PIPE
                                   , stderr=subprocess.PIPE)

        _, stderr = process.communicate()
        return_code = process.returncode
        print(process)
        print(stderr)
        assert (stderr == b'')
        assert (return_code == 0)


if __name__ == '__main__':
    main()
