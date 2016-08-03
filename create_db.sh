
## you'll need a sqlite db 'counted' already created in your directory
sqlite3 counted < initialize_db.sql
python create_historical.py
