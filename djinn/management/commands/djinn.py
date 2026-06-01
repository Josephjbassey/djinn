import os
import json
import requests
import click
from django.core.management.base import BaseCommand

DJINN_API_URL = "https://djinn-backend.vercel.app/api/v1"
RAW_REPO_URL = "https://raw.githubusercontent.com/josephjbassey/djinn/main"

class Command(BaseCommand):
    help = "Installs Djinn components using a Hybrid Fetch Architecture (Live API + GitHub Fallback)."

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument("component_name", type=str, help="Name of the component to install")

    def write_to_disk(self, component_name, filename, content):
        """Helper method to write component files to the local project structure."""
        target_dir = os.path.join("components", component_name)
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

    def handle(self, *args, **options):
        """Main command handler implementing Hybrid Fetch Architecture."""
        component_name = options["component_name"]

        # Phase 1: Vercel API (Live Database)
        try:
            api_endpoint = f"{DJINN_API_URL}/registry/{component_name}/"
            response = requests.get(api_endpoint, timeout=5)

            if response.status_code == 200:
                click.secho("✓ Found in Live Database. Extracting custom primitives...", fg="green")
                payload = response.json()
                files = payload.get("files", [])

                for file_data in files:
                    filename = file_data.get("filename")
                    content = file_data.get("content")
                    if filename and content:
                        self.write_to_disk(component_name, filename, content)
                return

        except (requests.ConnectionError, requests.Timeout):
            # Gracefully drop down to GitHub mechanism on network issues
            pass
        except Exception:
            # Other potential errors also trigger fallback
            pass

        # Phase 2: Fallback to GitHub mechanism
        click.echo("Looking in core package repo...")
        try:
            # Check for the existence of the registry index
            registry_index_url = f"{RAW_REPO_URL}/registry.json"
            index_response = requests.get(registry_index_url, timeout=5)

            if index_response.status_code == 200:
                # Download metadata just like the original static version did
                # Structure: registry/components/<name>/registry.json
                comp_reg_url = f"{RAW_REPO_URL}/registry/components/{component_name}/registry.json"
                comp_reg_resp = requests.get(comp_reg_url, timeout=5)

                if comp_reg_resp.status_code == 200:
                    metadata = comp_reg_resp.json()
                    files_map = metadata.get("files", {})

                    for file_type, filename in files_map.items():
                        # Fetch and write each asset relative to the component directory
                        asset_url = f"{RAW_REPO_URL}/registry/components/{component_name}/{filename}"
                        asset_resp = requests.get(asset_url, timeout=5)
                        if asset_resp.status_code == 200:
                            self.write_to_disk(component_name, filename, asset_resp.text)
                    return

        except Exception:
            # GitHub fallback failed
            pass

        # Final Error State
        click.secho(f"❌ Error: Component '{component_name}' not found anywhere.", fg="red")
