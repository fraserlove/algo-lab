'''
PyWrap - A Python Import Wrapper
Author: Fraser Love, me@fraser.love
Created: 2020-06-21
Latest Release: v1.0.1, 2023-08-10
Python: v3.10.12
Dependencies: requests

A import wrapper for Python files. Scans for and installs the dependencies in a Python file, then runs the python file.

Usage:  pyrap <python-file> <args>. The args are the arguments to be passed into the underlying Python file.
'''

import os, sys, subprocess, requests, re

imports = []


def scan_dependencies():
    print("======== Scanning Dependencies ========")
    c_dir = os.getcwd()
    files = [f for f in os.listdir(c_dir) if
             (os.path.isfile(os.path.join(c_dir, f)) and os.path.splitext(f)[1] == ".py")]
    for file in files:
        with open(file, "r") as file:
            for line in file:
                regex = re.search("\Aimport (.*)", line)
                if regex:
                    for group in regex.groups():
                        for library in group.split(", "):
                            if requests.get("https://pypi.org/simple/{}/".format(library)).status_code != 404:
                                if "<a href=" in requests.get("https://pypi.org/simple/{}/".format(library)).text:
                                    imports.append(library)
    print("--> Found packages:", *imports)


def installing_dependencies():
    print("======= Installing Dependencies =======")
    pip = subprocess.Popen(["which", "pip"], stdout=subprocess.PIPE)
    pip_out = pip.stdout.readline()
    if pip_out == "":
        print("Error: no version of pip found.\n")
        sys.exit()
    for library in imports:
        print("--> Installing package: {}...".format(library), end="")
        # subprocess.Popen(["pip3", "install", library])
        with open(os.devnull, "w") as f:
            subprocess.check_call(["pip", "install", library], stdout=f)
        print(" Done")


def run_program(py_file, args):
    print("=========== Running Program ===========")
    if not os.path.isfile(py_file):
        print("Error: file specified does not exist.\n")
        sys.exit()
    subprocess.Popen(["python3", py_file, *args])


def main():
    print(
        """     _ __  _   _ _ __ __ _ _ __  
    | '_ \| | | | '__/ _` | '_ \ 
    | |_) | |_| | | | (_| | |_) |
    | .__/ \__, |_|  \__,_| .__/ 
    |_|    |___/          |_|  
    """)
    if len(sys.argv) < 2 or not bool(re.match("^[\w,\s-]+\.py$", sys.argv[1])):
        print("Usage: pyrap <python-file> <args>\n")
        sys.exit()
    py_file = sys.argv[1]
    args = []
    if len(sys.argv) > 2:
        args = sys.argv[2:]
    scan_dependencies()
    installing_dependencies()
    run_program(py_file, args)


if __name__ == "__main__":
    main()