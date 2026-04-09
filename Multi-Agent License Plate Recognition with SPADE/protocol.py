from spade.message import Message
from spade.template import Template
from datetime import datetime

# Types de messages
TYPE_IMAGE_FULL = "IMAGE_FULL"
TYPE_PLATE_CROP = "PLATE_CROP"
TYPE_OCR_RESULT = "OCR_RESULT"

# JIDs des agents
CLIENT_JID = "client@localhost"
DETECTOR_JID = "detector@localhost"
OCR_JID = "ocr@localhost"