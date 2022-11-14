import pathlib
import os

import requests
from starlette.requests import Request
from starlette.responses import HTMLResponse
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from zeep import Client, helpers

from credentials import credentials
from parsers.fedex import FedexResponseParser

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def wsdl_uri() -> str:
    return pathlib.Path(os.path.abspath("description.wsdl")).as_uri()


def fedex_request_controller(track_number: str):
    url = wsdl_uri()
    client = Client(wsdl=url)
    try:
        response = client.service.track(
            **credentials,
            SelectionDetails={
                'PackageIdentifier': {
                    'Type': 'TRACKING_NUMBER_OR_DOORTAG',
                    'Value': track_number
                }
            },
            Version={
                'ServiceId': 'trck',
                'Major': 16,
                'Intermediate': 0,
                'Minor': 0,
            }
        )
    # in case we have connection issues or Fedex is blocked in some country
    except requests.exceptions.RequestException:
        response = {'error': 'Sorry, connection issues'}
    else:
        if response['HighestSeverity'] != 'SUCCESS':
            response = {
                'error': response['Notifications'][0]['Message']
            }
        else:
            parser = FedexResponseParser(
                response=helpers.serialize_object(response)
            )
            response = parser.parse()

    return response


# This is a route for simple HTML page being rendered by FastApi + Jinja2
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, track_number: str = None):
    if track_number:
        response = fedex_request_controller(track_number)
    else:
        response = None
    return templates.TemplateResponse(
        "main.html", {"request": request, "response": response}
    )
