from datasette import hookimpl
import click
from subprocess import call

from .common import (
    add_common_publish_arguments_and_options,
    fail_if_publish_binary_not_installed,
)
from ..utils import temporary_docker_directory


@hookimpl
def publish_subcommand(publish):
    @publish.command()
    @add_common_publish_arguments_and_options
    @click.option(
        "-n",
        "--name",
        default="datasette",
        help="Application name to use when deploying",
    )
    @click.option("--force", is_flag=True, help="Pass --force option to now")
    @click.option("--token", help="Auth token to use for deploy (Now only)")
    @click.option("--spatialite", is_flag=True, help="Enable SpatialLite extension")
    def now(
        files,
        metadata,
        extra_options,
        branch,
        template_dir,
        plugins_dir,
        static,
        install,
        version_note,
        title,
        license,
        license_url,
        source,
        source_url,
        name,
        force,
        token,
        spatialite,
    ):
        fail_if_publish_binary_not_installed("now", "Zeit Now", "https://zeit.co/now")
        if extra_options:
            extra_options += " "
        else:
            extra_options = ""
        extra_options += "--config force_https_urls:on"

        with temporary_docker_directory(
            files,
            name,
            metadata,
            extra_options,
            branch,
            template_dir,
            plugins_dir,
            static,
            install,
            spatialite,
            version_note,
            {
                "title": title,
                "license": license,
                "license_url": license_url,
                "source": source,
                "source_url": source_url,
            },
        ):
            args = []
            if force:
                args.append("--force")
            if token:
                args.append("--token={}".format(token))
            if args:
                call(["now"] + args)
            else:
                call("now")
