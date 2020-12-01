import argparse
import json
import os
import subprocess
import shlex


def main():
    parser = argparse.ArgumentParser()
    compile_name = "compile_commands.json"
    link_name = "link_commands.json"
    parser.add_argument(
        '--dir_proj'
        , required=True
        , help='directory with project, where place build'
    )

    args = parser.parse_args()
    cur_dir = args.dir_proj
    os.chdir(cur_dir)
    with open(link_name, "r") as read_file:
        link_data = json.load(read_file)

    with open(compile_name, "r") as read_file:
        compile_data = json.load(read_file)
    cur_dir = " "
    for elem in compile_data:
        if cur_dir != elem.get('directory'):
            if not os.path.exists(elem.get('directory')):
                raise FileExistsError
            cur_dir = elem.get('directory')
            os.chdir(cur_dir)

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

    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')

    cur_dir = " "
    for elem in link_data:
        if cur_dir != elem.get('directory'):
            if not os.path.exists(elem.get('directory')):
                raise FileExistsError
            cur_dir = elem.get('directory')
            os.chdir(cur_dir)

        command = shlex.split(elem.get('command'))
        process = subprocess.Popen(command
                                   , stdout=subprocess.PIPE
                                   , stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        return_code = process.returncode
        print(process)
        print(stderr)
        # assert (stderr == b'')
        # assert (return_code == 0)


if __name__ == '__main__':
    main()
