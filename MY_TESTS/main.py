import argparse
import json
import os
import subprocess
import shlex


def prepare_commands():
    mycmake = '/home/gleb/Documents/CMake/cmake-build-debug/bin/cmake'

    process1 = subprocess.Popen(f'{mycmake} ..'
                                , shell=True)
    process1.wait()
    print(f'myCMake return code: {process1.returncode}')

    process_delete = subprocess.Popen('find . -type f -not \( -name \'*o\' -or -name \'*json\' \) -delete'
                                , shell=True)
    process_delete.wait()

    print(f'delete second return code: {process_delete.returncode}')


def write_statistics():
    cmd1 = ['git', 'ls-files']
    cmd2 = ['xargs', 'wc', '-l']
    process1 = subprocess.Popen(cmd1
                                , stdout=subprocess.PIPE)
    process1.wait()
    process2 = subprocess.Popen(cmd2
                                , stdin=process1.stdout
                                , stdout=subprocess.PIPE
                                , stderr=subprocess.PIPE)
    process2.wait()

    stdout, stderr = process2.communicate()
    new_stdout = stdout.decode("utf-8").replace(' ', '').split('\n')
    total_files, total_lines = len(new_stdout) - 2, new_stdout[len(new_stdout) - 2].split('t')[0]
    print(f'totalf files: {total_files}\n')
    print(f'total lines: {total_lines}')
    with open('statistics', "w") as file:
        file.write(f'totalf files: {total_files}\n')
        file.write(f'total lines: {total_lines}')


def sort_link_json(tmp_name, link_name):
    with open(link_name, "r") as read_file:
        link_data = json.load(read_file)

    json_elems = []
    with open(tmp_name, "w") as json_file:
        json_file.write('[\n')
        for elem in link_data:
            fst_command = elem.get('command').split(' ')[0].split(os.path.sep)
            command = fst_command[len(fst_command) - 1]
            if command == 'ar' or command == 'ranlib':
                json.dump(elem, json_file, indent=2)
                json_file.write(',\n')
            else:
                json_elems.append(elem)

        for i in range(len(json_elems)):
            json.dump(json_elems[i], json_file, indent=2)
            if i != len(json_elems) - 1:
                json_file.write(',\n')
            else:
                json_file.write('\n')

        json_file.write(']')

    os.remove(link_name)
    os.rename(tmp_name, link_name)


def main():
    parser = argparse.ArgumentParser()
    compile_name = "compile_commands.json"
    link_name = "link_commands.json"
    tmp_name = "tmp.json"
    parser.add_argument(
        '--i'
        , required=True
        , help='directory with project'
    )

    args = parser.parse_args()
    repo = args.i
    os.chdir(repo)
    build_dir = os.path.join(os.getcwd(), 'build')
    # write_statistics()
    os.chdir(build_dir)
    prepare_commands()

    sort_link_json(tmp_name, link_name)

    with open(link_name, "r") as read_file:
        link_data = json.load(read_file)

    # with open(compile_name, "r") as read_file:
    #     compile_data = json.load(read_file)
    # cur_dir = " "
    # for elem in compile_data:
    #     if cur_dir != elem.get('directory'):
    #         if not os.path.exists(elem.get('directory')):
    #             raise FileExistsError
    #         cur_dir = elem.get('directory')
    #         os.chdir(cur_dir)
    #
    #     command = shlex.split(elem.get('command'))
    #     process = subprocess.Popen(command
    #                                , stdout=subprocess.PIPE
    #                                , stderr=subprocess.PIPE)
    #     _, stderr = process.communicate()
    #     return_code = process.returncode
    #     print(process)
    #     print(stderr)
    #     assert (stderr == b'')
    #     assert (return_code == 0)

    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')

    all_commands = len(link_data)
    incorrect_commands = 0
    build_dir = " "
    for elem in link_data:
        if build_dir != elem.get('directory'):
            if not os.path.exists(elem.get('directory')):
                raise FileExistsError
            build_dir = elem.get('directory')
            os.chdir(build_dir)

        command = shlex.split(elem.get('command'))
        process = subprocess.Popen(command
                                   , stdout=subprocess.PIPE
                                   , stderr=subprocess.PIPE)
        _, stderr = process.communicate()
        return_code = process.returncode
        print(process)
        print(stderr)

        if stderr != b'' or return_code != 0:
            incorrect_commands += 1

        # assert (stderr == b'')
        # assert (return_code == 0)
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print('----------------------------------------------------------------------------')
    print(all_commands)
    print(incorrect_commands)


if __name__ == '__main__':
    main()
