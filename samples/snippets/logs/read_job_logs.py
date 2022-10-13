#  Copyright 2022 Google LLC
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


# [START batch_job_logs]
from typing import Generator, NoReturn

from google.cloud import batch_v1
from google.cloud import logging


def get_job_logs(project_id: str, job: batch_v1.Job) -> Generator[logging.TextEntry, None, None]:
    log_client = logging.Client(project=project_id)
    logger = log_client.logger("batch_task_logs")

    yield from logger.list_entries(filter_=f"labels.job_uid={job.uid}")


def print_job_logs(project_id: str, job: batch_v1.Job) -> NoReturn:
    """
    Prints the log messages created by given job.

    Args:
        project_id: name of the project hosting the job.
        job: the job which logs you want to print.
    """
    for log_entry in get_job_logs(project_id, job):
        print(log_entry.payload)

# [END batch_job_logs]
