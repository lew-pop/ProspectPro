# data_loader.py - Securely loads and processes data
import pandas as pd
import os
from dotenv import load_dotenv
from prospect_data import ProspectData

# Load environment variables
load_dotenv()

# Load data securely
# username = os.getenv("DB_USERNAME")
# assword = os.getenv("DB_PASSWORD")
mongo_uri = os.getenv("MONGO_SRV")
players = ProspectData(mongo_uri)
df = pd.DataFrame.from_records(players.read_all({}))
