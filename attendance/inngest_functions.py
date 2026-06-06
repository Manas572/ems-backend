import inngest
from datetime import time
from django.utils import timezone
from emsbackend.inngest_client import inngest_client

@inngest_client.create_function(
    fn_id="daily-auto-checkout",
    trigger=inngest.TriggerCron(cron="30 12 * * *"), 
)
def auto_checkout_cron(ctx: inngest.ContextSync) -> dict:
    today = timezone.localdate()
    # Your background execution logic goes here...
    print(today)
    return {"status": "success", "message": f"Processed auto-checkout for {today}"}