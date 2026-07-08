# import logging
# import os
# from datetime import datetime
# os.makedirs("logs", exist_ok=True)
#
# log_file = f"logs/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
#
# logging.basicConfig(
#     level=logging.CRITICAL,
#     filename=log_file,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# NDIWEC



logging.critical("this is logging error message") # 10
logging.debug("this is logging debug message") #30
logging.info("this is logging logg message") #400
logging.warning("this is logging warn message") #40
logging.error("this is logging error message") #20
