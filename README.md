# Installation

### Clone repository

`git clone https://github.com/itsAnanth/streamlit-job-notifier`

### Install Dependencies

`cd streamlit-job-notifier`

`uv sync`

### Fetch latest job listings

`uv run utils/fetch.py`

#### To list a specific number of pages

`uv run utils/fetch.py --page <number of pages>`

By default its 2 pages
