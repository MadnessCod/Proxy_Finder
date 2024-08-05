import subprocess
import os
import time


def start_redis():
    redis_server_path = os.path.abspath(f'{os.getcwd()}\\..\\redis\\redis-server.exe')
    redis_process = subprocess.Popen([redis_server_path])
    return redis_process


def start_celery_worker(app_name, loglevel='info'):
    celery_worker_command = [
        'celery',
        '-A',
        app_name,
        'worker',
        '--loglevel=' + loglevel,
        '-P',
        'eventlet'
    ]
    celery_worker_process = subprocess.Popen(celery_worker_command)
    return celery_worker_process


def start_flower(app_name):
    flower_worker_process = [
        'celery',
        '-A', app_name,
        'flower',
    ]
    flower_worker_process = subprocess.Popen(flower_worker_process)
    return flower_worker_process


def start_celery_beat(app_name, loglevel='info'):
    celery_beat_beat_command = [
        'celery',
        '-A', app_name,
        'beat',
        '--loglevel=' + loglevel,
    ]
    celery_beat_process = subprocess.Popen(celery_beat_beat_command)
    return celery_beat_process


if __name__ == '__main__':
    print('starting')
    process = subprocess.Popen(
        ['poetry', 'run', 'python', 'database_creation.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    print("Output from database_creation.py:")
    print(stdout.decode())

    if stderr:
        print("Errors from database_creation.py:")
        print(stderr.decode())

    redis_process = start_redis()
    print('redis started')
    time.sleep(5)
    flower_process = start_flower('tasks')
    print('flower started, head to http://localhost:5555/')
    time.sleep(5)
    celery_worker_process = start_celery_worker('tasks')
    print('celery started')
    time.sleep(5)
    celery_beat_process = start_celery_beat('tasks')
    print('celery beat started')
    time.sleep(5)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        redis_process.terminate()
        flower_process.terminate()
        celery_beat_process.terminate()
        celery_worker_process.terminate()
        print('process terminated')
