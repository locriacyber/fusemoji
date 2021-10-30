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
    if ctx.exec_command("pipenv install", stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr) != 0:
        ctx.fatal(pipenv_errormsg)
    

ibus_component_path = "/usr/share/ibus/component"


def build(bld):
    bld(
        rule=lambda buildctx: generate_ibus_config(bld.path.abspath(), buildctx),
        source="uniemoji.xml.in",
        target="uniemoji.xml",
    )
    if not os.path.exists(ibus_component_path):
        bld.fatal(
            f"{ibus_component_path} doesn't exist. Maybe you need to install iBus first?"
        )
    bld.symlink_as(f"{ibus_component_path}/uniemoji.xml", "uniemoji.xml")


def generate_ibus_config(project_path, task):
    config = open(task.inputs[0].abspath()).read()
    config = config.replace("@PROJECTPATH@", project_path)
    open(task.outputs[0].abspath(), "w").write(config)
