"""Custom fastapi-mvc python_base generator implementation."""
import os

import click
import copier
from fastapi_mvc.cli import GeneratorCommand
from fastapi_mvc.utils import get_git_user_info, run_shell
from fastapi_mvc.constants import VERSION


cmd_short_help = "Create a new Python base application."
cmd_help = """\
The 'fastapi-mvc generate python_base' command creates a new Python application with a
default directory structure and configuration at the path you specify.

Default Project template used: https://github.com/rszamszur/copier-python-base
"""
epilog = """\
Example:
    `fastapi-mvc generate python_base ~/apis/Skynet`

    This generates a skeletal Python base project in ~/apis/Skynet.

"""
template = "https://github.com/rszamszur/copier-python-base"
vcs_ref = "master"
answers_file = ".python-base.yml"


@click.command(
    cls=Generator,
    category="Project",
    help=cmd_help,
    short_help=cmd_short_help,
)
@click.argument(
    "APP_PATH",
    nargs=1,
    type=click.Path(exists=False),
    required=True,
)
@click.option(
    "-G",
    "--skip-actions",
    help="Skip GitHub actions files.",
    is_flag=True,
)
@click.option(
    "-I",
    "--skip-install",
    help="Do not run make install after project generation.",
    is_flag=True,
)
@click.option(
    "-N",
    "--skip-nix",
    help="Skip nix expression files.",
    is_flag=True,
)
@click.option(
    "--license",
    help="Choose license.",
    type=click.Choice(
        [
            "MIT",
            "BSD2",
            "BSD3",
            "ISC",
            "Apache2.0",
            "LGPLv3+",
            "LGPLv3",
            "LGPLv2+",
            "LGPLv2",
            "no",
        ]
    ),
    default="MIT",
    show_default=True,
)
@click.option(
    "--repo-url",
    help="New project repository url.",
    type=click.STRING,
    envvar="REPO_URL",
    default="https://your.repo.url.here",
)
@click.option(
    "-n",
    "--no-interaction",
    help="Do not ask any interactive question.",
    is_flag=True,
)
@click.option(
    "--use-repo",
    help="Overrides fastapi-mvc copier-project repository.",
    type=click.STRING,
)
@click.option(
    "--use-version",
    help="The branch, tag or commit ID to checkout after clone.",
    type=click.STRING,
)
def python_base(app_path: str, **options: Dict[str, Any]) -> None:
    """Define python-base generator command-line interface.

    Args:
        app_path (str): Destination path where to render the project.
        options (typing.Dict[str, typing.Any]): Map of command option names to their
            parsed values.

    """
    app_abspath = os.path.abspath(app_path)

    if app_path == "." or os.path.exists(app_abspath):
        ensure_permissions(app_abspath, w=True)
    else:
        ensure_permissions(os.path.dirname(app_abspath), w=True)

    author, email = get_git_user_info()
    data = {
        "project_name": os.path.basename(app_abspath),
        "author": author,
        "email": email,
        "copyright_date": datetime.today().year,
        "fastapi_mvc_version": VERSION,
        "nix": not options["skip_nix"],
        "github_actions": not options["skip_actions"],
        "license": options["license"],
        "repo_url": options["repo_url"],
        "container_image_name": os.path.basename(app_abspath),
        "chart_name": os.path.basename(app_abspath),
        "script_name": os.path.basename(app_abspath),
        "project_description": "This project was generated with fastapi-mvc.",
        "version": "0.1.0",
    }

    if options["no_interaction"]:
        copier.run_copy(
            src_path=options["use_repo"] or template,
            vcs_ref=options["use_version"] or vcs_ref,
            dst_path=app_abspath,
            data=data,
            overwrite=True,
            answers_file=answers_file,
        )
    else:
        copier.run_copy(
            src_path=options["use_repo"] or template,
            vcs_ref=options["use_version"] or vcs_ref,
            dst_path=app_abspath,
            user_defaults=data,
            answers_file=answers_file,
        )

    copier.run_copy(
        src_path=os.path.dirname(__file__),
        data=data,
        answers_file=answers_file,
    )

    copier.printf(action="run", msg="git init", style=copier.Style.OK)
    run_shell(cmd=["git", "init"], cwd=app_abspath)

    if not options["skip_install"]:
        if shutil.which("make"):
            copier.printf(
                action="run",
                msg="make install",
                style=copier.Style.OK,
            )
            run_shell(cmd=["make", "install"], cwd=app_abspath)
        else:
            click.secho("make: shell command not found", fg="yellow")
            copier.printf(
                action="skipping",
                msg="make install",
                style=copier.Style.IGNORE,
            )
