''' Trigger this script from cron.sh or source your venv and run'''
# https://gitlab.com/doctormo/python-crontab/
from crontab import CronTab
import os


VENV_PATH_EXECUTABLE = os.environ['VIRTUAL_ENV'] + '/bin/python'

FILE_PATH = os.path.abspath(__file__).split('/')[:-1] # relative, removes last every time
FILE_PATH = "/".join(FILE_PATH)

LOG_FILE = os.getcwd() + '/cronlog.txt 2>&1'

FILE_TARGET = '/watcher.py'
FILE_TARGET = FILE_PATH + FILE_TARGET

class CronManager:
    def __init__(self):
        self.cron = CronTab(user=True)

    def add_job(self, cmd=None, comment='', user=True, minute=1):
        ''' Adds a job to crontable. '''
        cron_job = self.cron.new(command=cmd, comment=comment, user=user)

        # import pdb;pdb.set_trace()

        if CronManager.validity_check(cron_job) == True:
            cron_job.minute.every(minute)
            self.enable_job(cron_job)
            print(f"Added Job: {cron_job}")
            return True
        return False

    def disable_job(self, job):
        job.enable(False)
        self.cron.write()
        print('Job Disabled')

    def enable_job(self, job):
        job.enable(True)
        self.cron.write()
        print('Job Enabled')

    def remove_job(self, job):
        self.cron.remove(job)
        self.cron.write()
        print(f'Job Removed: {job}')

    def remove_jobs(self):
        self.cron.remove_all()
        self.cron.write()
        print('All Jobs Removed.')

    def get_jobs(self):
        ''' Prints all jobs. '''
        print(f"\n\t\t\t\t{'*'*25}ALL JOBS{'*'*25}\n{self.cron.render()}")

    def get_cron(self):
        ''' Returns all jobs. '''
        return self.cron

    def find_job_by_comment(self, comment=None):
        ''' Returns job if found - no jobs should have same comment. '''
        for job in self.cron:
            if str(job.comment) == (comment):
                return job
        return None

    @staticmethod
    def get_enable_status(job):
        print(f"Current Enabled Status: {job.is_enabled()}")
        return job.is_enabled()

    @staticmethod
    def run_job(job):
        ''' A dry run '''
        job_standard_output = job.run()
        print(f"job_standard_output --> {job_standard_output}")

    @staticmethod
    def validity_check(job):
        ''' Returns whether job command is valid. '''
        if job.is_valid() == True:
            return True
        return False

''' Working test which adds and removes a cron job '''
# cron = CronManager()
# cron.add_job(cmd=f'{VENV_PATH_EXECUTABLE} {FILE_TARGET} >> {LOG_FILE}', comment='bond watcher 1', minute=1)
# job = cron.find_job_by_comment('bond watcher 1')
# cron.remove_job(job)
