import click
from pathlib import Path
import shutil
from datetime import datetime
from djinn.core.config import Config, DEFAULT_CONFIG
from djinn.core.registry import Registry
from djinn.core.installer import Installer
from djinn.core.utils import calculate_hash


@click.command(name="upgrade")
@click.argument("component", required=False)
@click.option("--all", "upgrade_all", is_flag=True, help="Upgrade all installed components.")
@click.option("--force", is_flag=True, help="Upgrade without prompting.")
@click.option("--diff", "show_diff", is_flag=True, help="Show diff of changes without applying.")
@click.option("--backup", "create_backup", is_flag=True, help="Create backups before overwriting.")
def upgrade(component, upgrade_all, force, show_diff, create_backup):
    """Upgrade a component to the latest registry version.

    By default, shows what changed and prompts before overwriting.
    Use --force to skip prompts. Use --diff to preview changes only.
    Use --backup to create timestamped backups of files before overwriting.
    """
    config = Config.load()
    if not config:
        config = Config(**DEFAULT_CONFIG.copy())
        click.echo("Djinn not initialized. Using bundled registry defaults.")

    registry = Registry(config)
    installer = Installer(config, registry)

    if upgrade_all:
        components = registry.list_components()
        upgraded = 0
        for metadata in components:
            comp_name = metadata.name
            any_installed = False
            for file_obj in metadata.files:
                file_name = file_obj["name"]
                file_dir = file_obj.get("dir", "")
                if "templates" in file_dir:
                    dest_base = Path(metadata.install.get("template_path", config.get_template_path()))
                elif "templatetags" in file_dir:
                    dest_base = Path(metadata.install.get("python_path", config.get_python_path()))
                else:
                    dest_base = Path(file_dir) if file_dir else Path("components")
                dest_path = dest_base / file_name
                if dest_path.exists():
                    any_installed = True
                    break

            if not any_installed:
                continue

            click.echo(f"\nChecking '{comp_name}'...")
            if _upgrade_single(registry, installer, config, comp_name, force=True,
                               show_diff=show_diff, create_backup=create_backup):
                upgraded += 1

        click.echo(f"\nUpgraded {upgraded} component(s).")
        return

    if not component:
        click.secho("Error: Specify a component name or use --all to upgrade all components.", fg="red")
        return

    _upgrade_single(registry, installer, config, component, force=force,
                    show_diff=show_diff, create_backup=create_backup)


def _diff_files(registry_content, dest_path):
    """Return (added_lines, removed_lines) between registry and local content."""
    if not dest_path.exists():
        return [], []
    local_lines = dest_path.read_text(encoding="utf-8").splitlines(keepends=True)
    registry_lines = registry_content.splitlines(keepends=True)

    added = [l for l in registry_lines if l not in local_lines]
    removed = [l for l in local_lines if l not in registry_lines]
    return added, removed


def _upgrade_single(registry, installer, config, component, force=False,
                    show_diff=False, create_backup=False):
    """Upgrade a single component with diff preview and optional backup."""
    metadata = registry.load_component(component)
    if not metadata:
        click.secho(f"Component '{component}' not found in registry.", fg="red")
        return False

    changed = []
    for file_obj in metadata.files:
        file_name = file_obj["name"]
        file_dir = file_obj.get("dir", "")
        registry_content = file_obj.get("content", "")

        if "templates" in file_dir:
            dest_base = Path(metadata.install.get("template_path", config.get_template_path()))
        elif "templatetags" in file_dir:
            dest_base = Path(metadata.install.get("python_path", config.get_python_path()))
        else:
            dest_base = Path(file_dir) if file_dir else Path("components")

        dest_path = dest_base / file_name

        src_hash = calculate_hash(registry_content.encode("utf-8"))

        if not dest_path.exists():
            changed.append((file_name, dest_path, "missing", registry_content, ""))
        else:
            dest_hash = calculate_hash(dest_path)
            if src_hash != dest_hash:
                added, removed = _diff_files(registry_content, dest_path)
                changed.append((file_name, dest_path, "changed", registry_content,
                                dest_path.read_text(encoding="utf-8"),
                                added, removed))

    if not changed:
        click.echo(f"'{component}' is already up to date.")
        return True

    click.echo(f"\nFound {len(changed)} out-of-date file(s) for '{component}':")
    for entry in changed:
        file_name = entry[0]
        dest_path = entry[1]
        status = entry[2]
        click.echo(f"\n  {file_name} ({status})")
        click.echo(f"    Path: {dest_path}")

        if show_diff or status == "changed":
            added = entry[5] if len(entry) > 5 else []
            removed = entry[6] if len(entry) > 6 else []
            if added:
                click.echo("    + Additions:")
                for line in added[:10]:
                    click.echo(f"      +{line.rstrip()}")
                if len(added) > 10:
                    click.echo(f"      ... ({len(added) - 10} more lines)")
            if removed:
                click.echo("    - Removals:")
                for line in removed[:10]:
                    click.echo(f"      -{line.rstrip()}")
                if len(removed) > 10:
                    click.echo(f"      ... ({len(removed) - 10} more lines)")

    if show_diff:
        click.echo("\nDiff preview complete. No files were modified.")
        return True

    # Create backups if requested
    if create_backup:
        backup_dir = Path(f".djinn-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}") / component
        backup_dir.mkdir(parents=True, exist_ok=True)
        for entry in changed:
            dest_path = entry[1]
            if dest_path.exists():
                backup_path = backup_dir / dest_path.name
                shutil.copy2(dest_path, backup_path)
                click.echo(f"  Backed up: {dest_path} -> {backup_path}")

    if not force:
        click.echo(f"\nThis will overwrite {len(changed)} file(s) for '{component}'.")
        if create_backup:
            click.echo("Backups have been created.")
        if not click.confirm(f"Proceed with upgrade?", default=True):
            click.echo("Upgrade cancelled.")
            return False

    installed = installer.install(component, force=True)
    click.echo(f"\nSuccessfully upgraded '{component}':")
    for _, path in installed:
        click.echo(f"  - {path}")
    return True
