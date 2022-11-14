import datetime
from unittest.mock import patch

from fastapi.testclient import TestClient

import main

client = TestClient(main.app)


# just cleaned version of Fedex real response
def mocked_fedex_response():
    return {
        'HighestSeverity': 'SUCCESS',
        'CompletedTrackDetails': [
            {
                'TrackDetails': [
                    {
                        'Notification': {
                            'Severity': 'SUCCESS',
                        },
                        'TrackingNumber': '122816215025810',
                        'TrackingNumberUniqueIdentifier': '12013~',
                        'StatusDetail': {
                            'CreationTime': datetime.datetime(2014, 1, 9, 0, 0),
                            'Code': 'DL',
                            'Description': 'Delivered'
                        },
                        'Events': [
                            {
                                'Timestamp': datetime.datetime(
                                    2014, 1, 9, 0, 0
                                ),
                                'EventType': 'DL',
                                'EventDescription': 'Delivered',
                                'ArrivalLocation': 'DELIVERY_LOCATION'
                            }
                        ]
                    }
                ]
            }
        ]
    }


# This is the only one testcase for the app just to show I can mock requests.
# Ideally I would test other cases like: internet issues, empty response,
# etc. As you can check main.py and parser.py files - there are catches for
# different situations.
@patch('main.Client.service')
def test_read(mock):
    mock.track.return_value = mocked_fedex_response()
    response = main.fedex_request_controller('123')
    mock.track.assert_called()
    assert response == {
        'checkpoints': [
            {
                'status': 'Delivered',
                'tracking_stage': 'Delivered',
                'time': 'Thursday 09 January 2014'
            }
        ],
        'carrier': 'Fedex',
        'delivered': True,
        'description': 'Delivered',
        'time': 'Thursday 09 January 2014',
        'tracking_number': '122816215025810'
    }
