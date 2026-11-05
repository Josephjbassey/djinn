import click
from pathlib import Path
from djinn.core.config import Config


@click.command(name="doctor")
def doctor():
    """Check the project setup for common issues."""
    config = Config.load()
    if not config:
        click.secho("Djinn not initialized. Run 'djinn init' first.", fg="red")
        raise SystemExit(1)

    issues = []
    checks = []

    # Check config file
    checks.append(("djinn.json exists", True))

    # Check tailwind config
    tailwind_config = Path(config.tailwind.get("config", "tailwind.config.js"))
    checks.append((
        f"Tailwind config ({tailwind_config})",
        tailwind_config.exists()
    ))

    # Check tailwind content paths include templates
    if tailwind_config.exists():
        try:
            content = tailwind_config.read_text()
            templates_included = "templates" in content
            checks.append((
                "Tailwind content includes templates",
                templates_included
            ))
            if not templates_included:
                issues.append("tailwind.config.js content array doesn't include templates directory")
        except Exception:
            checks.append(("Tailwind content paths", False))
            issues.append("Could not read tailwind.config.js")

    # Check base CSS
    css_path = Path(config.tailwind.get("css", "static/css/base.css"))
    checks.append((
        f"Base CSS ({css_path})",
        css_path.exists()
    ))

    # Check cn tag
    utils_path = Path(config.get_python_path()) / "djinn_tags.py"
    checks.append((
        f"cn template tag ({utils_path})",
        utils_path.exists()
    ))

    # Check components dir
    components_path = Path(config.get_template_path())
    checks.append((
        f"Components directory ({components_path})",
        components_path.exists()
    ))

    # Report
    click.echo("Djinn Project Health Check")
    click.echo("=" * 40)
    all_ok = True
    for name, ok in checks:
        status = "PASS" if ok else "FAIL"
        color = "green" if ok else "red"
        click.echo(f"  [{click.style(status, fg=color)}] {name}")
        if not ok:
            all_ok = False

    if issues:
        click.echo("\nIssues found:")
        for issue in issues:
            click.echo(f"  - {issue}")

    if all_ok:
        click.echo("\nAll checks passed. Your project is ready for Djinn.")
    else:
        click.echo("\nSome checks failed. Run 'djinn init --force' to fix common issues.")
        raise SystemExit(1)
