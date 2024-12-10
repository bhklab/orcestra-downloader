from __future__ import annotations
import click
import difflib
import aiohttp
import asyncio
from rich.progress import Progress
from dataclasses import dataclass, field
from typing import List, Optional, Any
from pathlib import Path
from datetime import datetime
from rich.table import Table
from rich.console import Console
from orcestradownloader.cache import Cache
from orcestradownloader.models.pset import PharmacoSet
from orcestradownloader.models.clinical_icb import DatasetRecord
from orcestradownloader.models.radioset import RadioSet
from orcestradownloader.logging_config import logger as log

CACHE_DIR = Path.home() / ".cache/orcestradownloader"
PHARMACOS_CACHE_FILE = "pharmacosets.json"
ICB_CACHE_FILE = "icb_records.json"
RADIOSETS_CACHE_FILE = "radiosets.json"
XEVASETS_CACHE_FILE = "xevaset.json"
TOXICOSETS_CACHE_FILE = "toxicoset.json"

CACHE_DAYS_TO_KEEP = 7


class UnifiedDataManager:
    """Unified manager to handle both PharmacoSets and ICB Records."""

    def __init__(self, force: bool = False) -> None:
        self.pharmaco_cache = Cache(CACHE_DIR, PHARMACOS_CACHE_FILE, CACHE_DAYS_TO_KEEP)
        self.icb_cache = Cache(CACHE_DIR, ICB_CACHE_FILE, CACHE_DAYS_TO_KEEP)
        self.radiosets_cache = Cache(CACHE_DIR, RADIOSETS_CACHE_FILE, CACHE_DAYS_TO_KEEP)
        self.xevasets_cache = Cache(CACHE_DIR, XEVASETS_CACHE_FILE, CACHE_DAYS_TO_KEEP)
        self.toxicosets_cache = Cache(CACHE_DIR, TOXICOSETS_CACHE_FILE, CACHE_DAYS_TO_KEEP)

        self.pharmacosets: List[PharmacoSet] = []
        self.icb_records: List[DatasetRecord] = []
        self.radiosets: List[RadioSet] = []
        asyncio.run(self.fetch_all(force))

    async def fetch_data(self, url: str, cache: Cache, force: bool) -> List[dict]:
        """Fetch data from the API."""
        log.info("Fetching data from %s (force=%s)...", url, force)
        if not force and (cached_data := cache.get_cached_response()):
            return cached_data

        log.info("Making API call to %s", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json()
                log.info("Fetched %d items from API.", len(data))
                cache.cache_response(data)
                return data

    async def fetch_all(self, force: bool = False) -> None:
        """Fetch PharmacoSets and ICB records asynchronously."""
        pharmaco_url = "https://orcestra.ca/api/psets/available"
        icb_url = "https://orcestra.ca/api/clinical_icb/available"
        radiosets_url = "https://orcestra.ca/api/radiosets/available"
        xevasets_url = "https://orcestra.ca/api/xevasets/available"
        toxicosets_url = "https://orcestra.ca/api/toxicosets/available"

        with Progress(transient=True) as progress:
            pharmaco_task = progress.add_task("[cyan]Fetching PharmacoSets...", total=None)
            icb_task = progress.add_task("[cyan]Fetching ICB Records...", total=None)
            radiosets_task = progress.add_task("[cyan]Fetching RadioSets...", total=None)
            xevasets_task = progress.add_task("[cyan]Fetching XevaSets...", total=None)
            toxicosets_task = progress.add_task("[cyan]Fetching ToxicoSets...", total=None)

            pharmaco_data, icb_data, radiosets_data, xevasets_data, toxicosets_data = await asyncio.gather(
                self.fetch_data(pharmaco_url, self.pharmaco_cache, force),
                self.fetch_data(icb_url, self.icb_cache, force),
                self.fetch_data(radiosets_url, self.radiosets_cache, force),
                self.fetch_data(xevasets_url, self.xevasets_cache, force),
                self.fetch_data(toxicosets_url, self.toxicosets_cache, force),
            )

            progress.update(pharmaco_task, completed=True)
            progress.update(icb_task, completed=True)
            progress.update(radiosets_task, completed=True)
            progress.update(xevasets_task, completed=True)
            progress.update(toxicosets_task, completed=True)

        self.pharmacosets = [PharmacoSet.from_json(data) for data in pharmaco_data]
        self.icb_records = [DatasetRecord.from_json(data) for data in icb_data]
        self.radiosets = [RadioSet.from_json(data) for data in radiosets_data]
        log.info("Loaded %d PharmacoSets and %d ICB records.", len(self.pharmacosets), len(self.icb_records))

    def find_similar(self, name: str, items: List[Any], n: int = 3, cutoff: float = 0.3) -> List[str]:
        """Find similar names from a given list."""
        names = [item.name for item in items]
        return difflib.get_close_matches(name, names, n=n, cutoff=cutoff)

    def print_table(self, items: List[Any], title: str, sort: bool = True) -> None:
        """Print a table of items."""
        if sort:
            items = sorted(items, key=lambda item: item.name.lower())

        table = Table(title=title)

        table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("Dataset Name", justify="left", style="magenta")
        table.add_column("DOI", justify="left", style="yellow")
        table.add_column("Date Created", justify="left", style="green")
        table.add_column("Available Datatypes", justify="left", style="blue")

        for item in items:
            table.add_row(
                item.name,
                item.dataset.name,
                getattr(item, "doi", "N/A"),
                item.date_created.strftime("%Y-%m-%d") if getattr(item, "date_created", None) else "N/A",
                ", ".join(item.datatypes) if hasattr(item, "datatypes") else "N/A",
            )

        console = Console()
        console.print(table)

    def print_all(self) -> None:
        """Print both PharmacoSets and ICB records."""
        self.print_table(self.pharmacosets, "PharmacoSets")
        self.print_table(self.icb_records, "ICB Records")
        self.print_table(self.radiosets, "RadioSets")


@click.command()
@click.option("--force", is_flag=True, help="Force fetch new data")
@click.argument("names", nargs=-1, type=str, required=False)
def cli(names: List[str], force: bool = False) -> None:
    """Unified CLI for fetching and managing PharmacoSets and ICB records."""
    log.info("Starting UnifiedDataManager...")
    manager = UnifiedDataManager(force=force)

    if not names:
        manager.print_all()
        return

if __name__ == "__main__":
    cli()