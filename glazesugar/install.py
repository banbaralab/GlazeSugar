import subprocess
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sugar', dest='sugar', action='store_true',
                        default=False, help='Install sugar')
    parser.add_argument('--kissat', dest='kissat', action='store_true',
                        default=False, help='Install kissat')
    install_path_default = os.path.join("~", ".sugar_solvers")
    parser.add_argument('--install-path', dest='install_path',
                        type=str, default=install_path_default,
                        help=f'The folder to use for the installation(defaults to: {install_path_default})')
    options = parser.parse_args()

    install_dir = os.path.expanduser(options.install_path)
    if not os.path.exists(install_dir):
        os.makedirs(install_dir)

    if getattr(options, 'sugar'):
        print("install sugar")
        subprocess.run(["git", "clone", "https://gitlab.com/cspsat/prog-sugar", f"{install_dir}/prog-sugar"])

    if getattr(options, 'kissat'):
        subprocess.run(["git", "clone", "https://github.com/arminbiere/kissat", f"{install_dir}/kissat"])
        subprocess.run(['./configure && make test'], shell=True, cwd=f"{install_dir}/kissat")
        print("add solver path to `$PATH`")
        print(f"    export PATH=$PATH:{install_dir}/kissat/build")
