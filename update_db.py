#!/usr/bin/env python
import shutil
from backend.database import init_db
init_db()
shutil.move('./database.db','./backend/database.db')