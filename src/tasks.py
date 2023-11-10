from datetime import datetime
from django_q.tasks import schedule
from django_q.tasks import async_task
from django_q.models import Schedule
from src.models import Query
import oracledb
from decouple import config


def run_sql_query():
    conn = oracledb.connect(
        user=config('DB_USER_ORACLE'),
        password=config('DB_PASSWORD_ORACLE'),
        host=config('DB_HOST_ORACLE'), port=config('DB_PORT_ORACLE'), service_name=config('DB_SERVICE_NAME')
    )
    with conn.cursor() as cursor:
        query = Query.objects.get(name='total').query
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)

# Agende a tarefa para ser executada
# Executa uma programação a cada 1 minuto
Schedule.objects.create(
    name='run_query_schedule',
    func='src.tasks.run_sql_query',
    schedule_type=Schedule.MINUTES,
    minutes=1,
    repeats=-1,
    cluster='scheduler', # Nome dado ao cluster na constante Q_CLUSTER do arquivo de settings
    # next_run=datetime.utcnow().replace(hour=14, minute=30)
)


