import redis
import stripe
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from swarm.departments.finance.billing_agent import BillingAgent
from swarm.tools.stripe_tool import StripeTool

from ...database import get_db
from ...main import send_agent_message  # Import send_agent_message utility
from ..redis_client import \
    get_redis  # Import get_redis to pass to send_agent_message

router = APIRouter()

# Initialize StripeTool and BillingAgent outside the endpoint to avoid re-initialization
stripe_tool = StripeTool()
billing_agent = BillingAgent()  # Initialize BillingAgent


@router.post("/stripe-webhook")
async def stripe_webhook(
    request: Request, db: Session = Depends(get_db), r: redis.Redis = Depends(get_redis)
):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    event = None

    try:
        event = stripe_tool.construct_webhook_event(payload, sig_header)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid payload: {e}"
        )
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid signature: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Webhook Error: {e}"
        )

    # Delegate the event handling to the BillingAgent
    # The BillingAgent will directly interact with the DB and other agents via its methods
    # For now, we call the agent directly. In a more complex setup, we might queue a message for it.
    try:
        # Instead of calling agent directly, we send a message to its Redis queue
        # The BillingAgent will be running in the background and listening to its queue
        send_agent_message(
            recipient_id=billing_agent.agent_id,
            sender_id="stripe_webhook",
            message_content={
                "action": "handle_webhook_event",
                "event_payload": payload.decode("utf-8"),  # Pass payload as string
                "signature": sig_header,
            },
            r=r,
        )
        return {
            "status": "success",
            "message": f"Event {event.type} received and queued for BillingAgent.",
        }
    except Exception as e:
        print(f"Error sending webhook event to BillingAgent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook event: {e}",
        )
