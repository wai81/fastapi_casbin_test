#run migrations
alembic upgrade head
# create initial data in DB
python /app/initial_data.py