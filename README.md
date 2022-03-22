# subgraph-dags
Pipelines to extract data from Subgraphs and pipe into a data warehouse

## Local Development

Start up a local development environment using Docker:

```bash
docker run --rm -it -w /usr/local/src -e GOOGLE_APPLICATION_CREDENTIALS=/key/<name_of_key>.json -v ~:/key -v $PWD:/usr/local/src python:3.10 bash
```

_NOTE: assumes there is a Google Cloud service account credential located in `~` with the filename `<name_of_key>.json`_

Then install dependencies:

```bash
pip install -r requirements.txt
```

Then you can either run `dagit` for visualization or use `python <name_of_dag>` to execute the DAG.
