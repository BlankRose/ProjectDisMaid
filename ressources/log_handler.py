import logging as log
import os

def danger(msg: str):
	log.critical(msg)
	os.abort()