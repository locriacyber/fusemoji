#!/usr/bin/env python
import sys, os

APPNAME = "uniemoji"
VERSION = "1.0"

top = "."
out = "build"


def configure(ctx):
    ctx.log = True
    print("→ prefix is " + ctx.options.prefix)
    install_dependencies(ctx)


pipenv_errormsg = """
Compilation failed
You probably need this:
How to install PyGObject: https://pygobject.readthedocs.io/en/latest/getting_started.html
""".lstrip()


def install_dependencies(ctx):
    if (
        ctx.exec_command(
            r'''python -c "__import__('gi')"''', stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
        != 0
    ):
        ctx.fatal("PyGObject is not installed")
    if (
        ctx.exec_command(
            r'''python -c "__import__('Levenshtein')"''', stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr
        )
        != 0
    ):
        ctx.fatal("Python module 'levenshtine' is not installed")

ibus_component_directory = "/usr/share/ibus/component"
ibus_component_path = "uniemoji.xml"

def build(bld):
    ibus_component = bld(
        rule=lambda buildctx: generate_ibus_config(bld.path.abspath(), buildctx),
        source="uniemoji.xml.in",
        target="uniemoji.xml",
    )
    if not os.path.exists(ibus_component_directory):
        bld.fatal(
            f"{ibus_component_directory} doesn't exist. Maybe you need to install iBus first?"
        )
    bld.symlink_as(f"{ibus_component_directory}/{ibus_component_path}", os.path.abspath(f"{out}/{ibus_component_path}"))


def generate_ibus_config(project_path, task):
    config = open(task.inputs[0].abspath()).read()
    config = config.replace("@PROJECTPATH@", project_path)
    open(task.outputs[0].abspath(), "w").write(config)


def main():
    os.chdir(os.path.dirname(__file__))
    exit(os.system("./ibus.py --ibus"))


if __name__ == "__main__":
    main()
