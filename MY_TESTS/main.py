import argparse
import json
import os
import subprocess
import shlex


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
    # repo = args.i
    # command = shlex.split('git ls-files | xargs cat | wc -l')
    # process = subprocess.Popen(command
    #                            , stdout=subprocess.PIPE
    #                            , stderr=subprocess.PIPE)
    #
    # stdout, stderr = process.communicate()
    # print(stderr)
    # if process.returncode != 0:
    #     print(f"Cannot write lines of code in repo {repo}")

    build_dir = os.path.join(args.i, 'build')
    print(build_dir)
    os.chdir(build_dir)

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
        assert (stderr == b'')
        assert (return_code == 0)


if __name__ == '__main__':
    main()
