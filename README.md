# arXiv Paper Fetcher

This repository contains scripts to fetch recent papers from arXiv based on a search query and download their PDFs.

## Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```
   python3 -m venv arxiv_env
   ```

3. Activate the virtual environment:
   - On Unix or MacOS:
     ```
     source arxiv_env/bin/activate
     ```
   - On Windows:
     ```
     arxiv_env\Scripts\activate
     ```

4. Install the required packages:
   ```
   pip install feedparser
   ```

## Usage

### Fetching Papers from arXiv

Use the `run_arxiv_fetch.sh` script to fetch papers from arXiv:

```
./run_arxiv_fetch.sh -q "your search query" -n 5
```

Options:
- `-q` or `--query`: Specify the search query (required)
- `-n` or `--num`: Specify the number of results to fetch (default: 5)
- `-h` or `--help`: Display help message

This script will:
1. Fetch papers matching your query from arXiv
2. Download the PDFs to a `pdfs` folder
3. Name the PDFs using the search query and the first 10 words of the paper title

## Files in this Repository

- `run_arxiv_fetch.sh`: Shell script to fetch papers from arXiv
- `arxiv_query.py`: Python script that interacts with the arXiv API
- `README.md`: This file, containing setup and usage instructions

## Notes

- The scripts assume a Unix-like environment. For Windows users, you may need to adapt the shell script or run the Python scripts directly.
- Always comply with arXiv's terms of service when using these scripts.
- Be mindful of the number of requests you make to the arXiv API to avoid overloading their servers.

## Example

To fetch the 5 most recent papers about quantum computing:

```
./run_arxiv_fetch.sh -q "quantum computing" -n 5
```

This will download up to 5 PDFs into the `pdfs` folder, with filenames like:
```
quantum_computing_Quantum advantage in learning from experiments_2112.00778.pdf
```

## Contributing

Contributions to improve the scripts or extend functionality are welcome. Please feel free to submit issues or pull requests.
