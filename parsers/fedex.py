from datetime import datetime
from typing import Tuple, Optional


class FedexResponseParser:
    def __init__(self, response: dict):
        self.response = response

    @staticmethod
    def get_checkpoints(events: list) -> list:
        checkpoints = []
        for event in events:
            time = event.get('Timestamp', 'undefined')
            if isinstance(time, datetime):
                time = time.strftime('%A %d %B %Y')
            checkpoint = {
                'status': event.get('EventDescription', 'undefined'),
                'tracking_stage': event.get('EventDescription', 'undefined'),
                'time': time
            }
            checkpoints.append(checkpoint)
        return checkpoints

    @staticmethod
    def check_response_is_meaningful(
            track_details: dict
    ) -> Tuple[bool, Optional[str]]:
        notification = track_details.get('Notification', {})
        if notification.get('Severity', 'Error') != 'SUCCESS':
            return False, notification.get(
                'Message', 'There is no data for this track number'
            )
        return True, None

    def parse(self) -> dict:
        parsed_response = {}
        # using indexed here, because assuming that TrackDetails will be
        # in every response no matter which status.
        track_details = self.response.get('CompletedTrackDetails')[0].get(
            'TrackDetails'
        )[0]
        status_details = track_details.get('StatusDetail', {})
        is_meaningful, error_message = self.check_response_is_meaningful(
            track_details
        )
        if not is_meaningful:
            return {'error': error_message}

        # --- Creating parsed response for the customer here ---
        parsed_response['checkpoints'] = self.get_checkpoints(
            track_details.get('Events', [])
        )
        parsed_response['carrier'] = 'Fedex'
        # got this from official docs, page 38, 5.1.5 Tracking Status
        parsed_response['delivered'] = True if status_details.get(
            'Code'
        ) == 'DL' else False
        parsed_response['description'] = status_details.get('Description')
        parsed_response['time'] = status_details.get(
            'CreationTime'
        ).strftime('%A %d %B %Y')
        parsed_response['tracking_number'] = track_details.get('TrackingNumber')

        return parsed_response
