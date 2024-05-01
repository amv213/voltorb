import os
from datetime import datetime, timedelta, timezone

import httpx
from dotenv import load_dotenv
from rich import print

from electron import electricity_maps, executor, token_auth
from electron.typing import ZoneKey

if __name__ == "__main__":
    load_dotenv()
    API_TOKEN = os.environ.get("API_TOKEN")

    geolocation = ZoneKey("IT")
    historical_datetime = datetime.now(timezone.utc) - timedelta(days=7)

    queries = [
        # no auth
        # electricity_maps.get_zones(),
        # electricity_maps.get_health(),
        # free API for personal use
        electricity_maps.carbon_intensity.get_latest(geolocation=geolocation),
        electricity_maps.carbon_intensity.get_history(geolocation=geolocation),
        electricity_maps.power_breakdown.get_latest(geolocation=geolocation),
        electricity_maps.power_breakdown.get_history(geolocation=geolocation),
        # commercial API
        # electricity_maps.carbon_intensity.get_past(geolocation=geolocation),
        # electricity_maps.carbon_intensity.get_past_range(geolocation=geolocation),
        # electricity_maps.carbon_intensity.get_forecast(geolocation=geolocation),
        # electricity_maps.power_breakdown.get_past(geolocation=geolocation),
        # electricity_maps.power_breakdown.get_past_range(geolocation=geolocation),
        # electricity_maps.power_breakdown.get_forecast(geolocation=geolocation),
        # electricity_maps.marginal_carbon_intensity.get_past(geolocation=geolocation, date_time=historical_datetime),
        # electricity_maps.marginal_carbon_intensity.get_range(geolocation=geolocation, start=historical_datetime, end=historical_datetime + timedelta(days=3)),
        # electricity_maps.power_production_breakdown.get_forecast(geolocation=geolocation),
        # electricity_maps.power_consumption_breakdown.get_forecast(geolocation=geolocation),
        # electricity_maps.get_updated_since(geolocation=geolocation, since=datetime.now(timezone.utc) - timedelta(days=7))
    ]

    with httpx.Client() as client:
        # convenience to avoid having to always have to call snug.execute(query, auth=)
        execute = executor(auth=token_auth(API_TOKEN), client=client)

        for i, query in enumerate(queries):
            # for some reason passing free API token to /zones() gives 401 Invalid Token
            out = execute(query)

            print(out, end="\n\n")
