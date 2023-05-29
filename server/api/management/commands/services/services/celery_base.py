from .base import BaseService
from ..hands import *


class CeleryBaseService(BaseService):

    def __init__(self, queue, num=10, **kwargs):
        super().__init__(**kwargs)
        self.queue = queue
        # self.num = settings.CELERY_WORKER_CONCURRENCY if settings.CELERY_WORKER_CONCURRENCY else num
        self.autoscale = settings.CELERY_WORKER_AUTOSCALE

    @property
    def cmd(self):
        print('\n- Start Celery as Distributed Task Queue: {}'.format(self.queue.capitalize()))

        os.environ.setdefault('PYTHONOPTIMIZE', '1')
        os.environ.setdefault('ANSIBLE_FORCE_COLOR', 'True')

        if os.getuid() == 0:
            os.environ.setdefault('C_FORCE_ROOT', '1')
        server_hostname = os.environ.get("SERVER_HOSTNAME")
        if not server_hostname:
            server_hostname = '%h'

        cmd = [
            'celery',
            '-A', 'xbook',
            'worker',
            '-P', 'prefork',
            '-l', 'INFO',
            # '-c', str(self.num),
            '--autoscale', ",".join([str(x) for x in self.autoscale]),
            '-Q', self.queue,
            '--heartbeat-interval', '10',
            '-n', f'{self.queue}@{server_hostname}',
            '--without-mingle',
        ]
        if self.uid:
            cmd.extend(['--uid', self.uid])
        if self.gid:
            cmd.extend(['--gid', self.gid])
        return cmd

    @property
    def cwd(self):
        return APPS_DIR
