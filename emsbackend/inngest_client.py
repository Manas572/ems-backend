import logging
import inngest

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)

inngest_client = inngest.Inngest(
    app_id="ems_backend",
    logger=logger,
)