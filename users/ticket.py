
import requests

def post_ticket_to_zendesk(ticket,contact_email, contact_phone):
    
    zendesk_api_url = "https://example.zendesk.com/api/v2/tickets"

    payload = {
        "ticket": {
            "comment": {
                "body": ticket.body
            },
            "priority": ticket.priority,
            "subject": ticket.subject
        }
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(
        zendesk_api_url,
        auth=(contact_email, contact_phone),
        headers=headers,
        json=payload
    )

    return response
