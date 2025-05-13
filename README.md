<div align="center">

# orcestra-downloader

Simplified access to download data from orcestra.ca

[![pixi-badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json&style=flat-square)](https://github.com/prefix-dev/pixi)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=flat-square)](https://github.com/astral-sh/ruff)
[![Built with Material for MkDocs](https://img.shields.io/badge/mkdocs--material-gray?logo=materialformkdocs&style=flat-square)](https://github.com/squidfunk/mkdocs-material)

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/orcestra-downloader)](https://pypi.org/project/orcestra-downloader/)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/bhklab/orcestra-downloader?label=GitHub%20Release&style=flat-square)
[![PyPI - Version](https://img.shields.io/pypi/v/orcestra-downloader)](https://pypi.org/project/orcestra-downloader/)
[![Downloads](https://static.pepy.tech/badge/orcestra-downloader)](https://pepy.tech/project/orcestra-downloader)

![GitHub last commit](https://img.shields.io/github/last-commit/bhklab/orcestra-downloader?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/bhklab/orcestra-downloader?style=flat-square)
![GitHub pull requests](https://img.shields.io/github/issues-pr/bhklab/orcestra-downloader?style=flat-square)
![GitHub contributors](https://img.shields.io/github/contributors/bhklab/orcestra-downloader?style=flat-square)
![GitHub stars](https://img.shields.io/github/stars/bhklab/orcestra-downloader?style=flat-square)
![GitHub forks](https://img.shields.io/github/forks/bhklab/orcestra-downloader?style=flat-square)

</div>

## Installation

### 1. Recommended CLI access

The recommended way to use `orcestra-downloader` is through its CLI tool, which
can be easily done without ever installing it on your system.
You can run the CLI directly using `pixi` or `uvx` commands.

#### [pixi exec](https://pixi.sh/latest/reference/cli/pixi/exec/#pixi-exec) **via [conda](https://anaconda.org/conda-forge/orcestra-downloader)**

<table>
<tr>
<td>

```console
pixi exec orcestra-downloader --help                                                               
```

<details>
<summary>Output</summary>

![pixi-exec-help](assets/pixi-exec-help.png)

</details>
</table>

#### [uvx](https://docs.astral.sh/uv/guides/tools/#running-tools) **via [pypi](https://pypi.org/project/orcestra-downloader)**

<table>
<tr>
<td>

```console
uvx orcestra-downloader --help                                                                     
```

<details>
<summary>Output</summary>

![uvx-help](assets/uvx-help.png)

</details>
</td>
</tr>
</table>

### 2. Install into `pixi` project

If you wish to use `orcestra-downloader` in a [pixi](https://pixi.sh) project,
you can install `orcestra-downloader` into your project.

**conda-forge**:

```console
pixi add orcestra-downloader         # from conda-forge

pixi add --pypi orcestra-downloader  # from pypi
```

### 3. Install with `pip`

If you have a [python virtual environment](https://docs.python.org/3/tutorial/venv.html) set up,
you can install `orcestra-downloader` directly using `pip` or `python -m pip`.

To install the package, use `pip`:

```console
pip install orcestra-downloader
```

## Usage

The `orcestra-downloader` provides a convenient command-line interface to interact with the [orcestra.ca](https://orcestra.ca) API. The CLI allows you to list, view, and download various datasets easily.

### Available Dataset Types

<table>
<tr>
<td>

:microscope: Seven different dataset types are available through orcestra.ca:

</td>
</tr>
<tr>
<td>

| Dataset Type | Description |
|-------------|-------------|
| `pharmacosets` | Pharmacological screening datasets |
| `icbsets` | Immune checkpoint blockade datasets |
| `radiosets` | Radiotherapy response datasets |
| `xevasets` | Xenograft-derived datasets |
| `toxicosets` | Toxicological screening datasets |
| `radiomicsets` | Radiomics datasets |
| `clinicalgenomics` | Clinical genomics datasets |

</td>
</tr>
</table>

### Basic Commands

<table>
<tr>
<td>

:technologist: Each dataset type supports these common commands:

</td>
</tr>
<tr>
<td>

```bash
# List all items in a dataset
orcestra-downloader [dataset_type] list

# Print a table of items in a dataset
orcestra-downloader [dataset_type] table [DATASET_NAME]

# Download a file for a dataset
orcestra-downloader [dataset_type] download [DATASET_NAME]

# Download all files for a dataset
orcestra-downloader [dataset_type] download-all
```

</td>
</tr>
</table>

### Examples

<table>
<tr>
<td>

:clipboard: Basic listing and table commands

</td>
</tr>
<tr>
<td>

```console
# List all radiosets
orcestra-downloader radiosets list

# Print a table of all xevasets after refreshing the cache
orcestra-downloader xevasets table --force

# Print a table of a specific dataset with more details
orcestra-downloader pharmacosets table GDSC_2020(v2-8.2)
```

</td>
</tr>
<tr>
<td>
<details>
<summary>:eyes: Command Demo</summary>

![orcestra-gif](./tapes/orcestra.gif)

</details>
</td>
</tr>
</table>

### Refreshing Cache

<table>
<tr>
<td>

:bulb: `orcestra-downloader` uses a cache to store dataset metadata from the Orcestra API.
This should be located at `~/.cache/orcestra-downloader`.

</td>
</tr>
<tr>
<td>

By default, the tool will only update cache when used 7 days after the last update.
To refresh the cache, use the `--refresh` flag.

```console
orcestra-downloader --refresh
```

</td>
</tr>
</table>

### Downloading Datasets

<table>
<tr>
<td>

:arrow_down: Download specific datasets or entire collections:

</td>
</tr>
<tr>
<td>

```console
# Download a specific pharmacoset
orcestra-downloader pharmacosets download 'GDSC_2020(v2-8.2)'

# Download multiple datasets at once
orcestra-downloader radiomicsets download HNSCC_Features RADCURE_Features

# Specify a custom download directory
orcestra-downloader toxicosets download 'DrugMatrix Rat' --directory ./my-data-folder

# Download all datasets of a specific type (with progress bar)
orcestra-downloader xevasets download-all

# Force overwrite of existing files
orcestra-downloader icbsets download-all --overwrite
```

</td>
</tr>
</table>

### Command Reference

<table>
<tr>
<td>

:gear: Global options available for all commands:

</td>
</tr>
<tr>
<td>

```console
Options:
  -r, --refresh  Fetch all datasets and hydrate the cache.
  -h, --help     Show this message and exit.
  -q, --quiet    Suppress all logging except errors.
  -v, --verbose  Increase verbosity of logging (0-3: ERROR, WARNING, INFO, DEBUG).
```

</td>
</tr>
<tr>
<td>
<details>
<summary>:keyboard: Dataset-specific command options</summary>

For the `list` command:

```console
Options:
  --force      Force fetch new data.
  --no-pretty  Disable pretty printing.
```

For the `table` command:

```console
Arguments:
  [NAME OF DATASET]  Optional dataset name for detailed information.

Options:
  --force      Force fetch new data.
```

For the `download` command:

```console
Arguments:
  [ORCESTRA DATASET NAME]  Required dataset name(s) to download.

Options:
  -o, --overwrite          Overwrite existing file if it exists.
  -d, --directory PATH     Directory to save the file to.
  --force                  Force fetch new data from the API.
```

For the `download-all` command:

```console
Options:
  -o, --overwrite          Overwrite existing files if they exist.
  -d, --directory PATH     Directory to save the files to.
  --force                  Force fetch new data from the API.
```

</details>
</td>
</tr>
</table>

## Troubleshooting

<table>
<tr>
<td>

:question: Common issues and solutions:

</td>
</tr>
<tr>
<td>

- **Cache issues**: If you're getting outdated information, try using the `--refresh` flag or `--force` option.
- **Download errors**: Check your internet connection and make sure the orcestra.ca API is accessible.
- **Permission errors**: Ensure you have write permissions to the download directory.
- **Dataset not found**: Make sure the dataset name is correct and exists on orcestra.ca.

</td>
</tr>
</table>

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

If you encounter any issues or have questions, please open an issue on the GitHub repository:
[https://github.com/bhklab/orcestra-downloader/issues](https://github.com/bhklab/orcestra-downloader/issues)
