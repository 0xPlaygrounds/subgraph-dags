import requests
import csv

from dagster import job, op, get_dagster_logger, resource
import dagster_gcp
from google import cloud
import pandas as pd
from subgrounds.subgrounds import Subgrounds


sg = Subgrounds()

olympus_pro = sg.load_subgraph('https://api.thegraph.com/subgraphs/name/0xplaygrounds/olympus-pro-subgraph')


@resource
def bigquery():
    return cloud.bigquery.Client()


@op
def fetch_user_bonds() -> pd.DataFrame:
    user_bonds = olympus_pro.Query.userBonds(
        orderBy=olympus_pro.UserBond.timestamp,
        orderDirection='asc',
        first=5000,
    )

    return sg.query_df([
        user_bonds.id,
        user_bonds.timestamp,
        user_bonds.bond.id,
        user_bonds.user,
        user_bonds.deposit,
        user_bonds.depositUSD,
        user_bonds.payout,
        user_bonds.payoutUSD,
        user_bonds.expires,
        user_bonds.expiresTimestamp,
        user_bonds.discount
    ])


@job(resource_defs={"bigquery": bigquery})
def fetch_subgraph_job():
    dagster_gcp.import_df_to_bq(fetch_user_bonds())


if __name__ == "__main__":
    result = fetch_subgraph_job.execute_in_process(
        run_config={
            "ops": {
                "import_df_to_bq": {"config": {"destination": "pga_poc.olympus_pro_daily_bonds"}}
            }
        }
    )
