from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import EventType, FollowupAction, SlotSet, ReminderScheduled, ReminderCancelled, AllSlotsReset, UserUtteranceReverted
from .utils import log, filter_entities, filter_in_runs, runs_json, get_attachment, get_sites
from rasa_sdk.types import DomainDict
from datetime import datetime, timedelta
from rasa_sdk.forms import FormValidationAction, Optional
from random import choice, randint
import json
import re