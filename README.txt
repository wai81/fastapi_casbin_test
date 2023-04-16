
* Миграцииия
* migration init '[name_migration]'
alembic revision --autogenerate -m "Added account table"
* fixed migration
alembic upgrade head
* fixed migration revision version
alembic upgrade [number_revison]
alembic upgrade ae1027a6acf or alembic upgrade ae1(first three symbols revision migration)

* Работа с Docker
* собираем
docker-compose build
* запускаем
docker-compose up -d
* вход в контейнер
docker exec -it {name_contaner} sh(bash)

