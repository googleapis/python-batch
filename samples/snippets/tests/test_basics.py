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
import time
import uuid

import google.auth
from google.cloud import batch_v1
from google.cloud import logging
import pytest

from ..create.create_with_container_no_mounting import create_container_job
from ..create.create_with_script_no_mounting import create_script_job

from ..delete.delete_job import delete_job
from ..get.get_job import get_job
from ..list.list_jobs import list_jobs

PROJECT = google.auth.default()[1]
REGION = 'europe-north1'

TIMEOUT = 600  # 10 minutes

WAIT_STATES = {
    batch_v1.JobStatus.State.STATE_UNSPECIFIED,
    batch_v1.JobStatus.State.QUEUED,
    batch_v1.JobStatus.State.RUNNING,
    batch_v1.JobStatus.State.SCHEDULED,
}


@pytest.fixture
def job_name():
    return f"test-job-{uuid.uuid4().hex[:10]}"


def _test_body(job: batch_v1.Job):
    logging_client = logging.Client()
    start_time = time.time()
    try:
        while job.status.state in WAIT_STATES:
            if time.time() - start_time > TIMEOUT:
                pytest.fail("Timed out while waiting for job to complete!")
            job = get_job(PROJECT, REGION, job.name.rsplit('/', maxsplit=1)[1])
            time.sleep(5)
        time.sleep(15)  # Let the logging properly register all messages
        logger = logging_client.logger("batch_task_logs", labels={'job_uid': job.uid})
        tasks_done = 0
        for entry in logger.list_entries():
            if entry.labels['job_uid'] != job.uid:
                continue
            if "Hello world! This is task" in entry.payload:
                tasks_done += 1
        assert (tasks_done == 4)

        for job in list_jobs(PROJECT, REGION):
            if job.uid == job.uid:
                break
        else:
            pytest.fail(f"Couldn't find job {job.uid} on the list of jobs.")
    finally:
        delete_job(PROJECT, REGION, job.name.rsplit('/', maxsplit=1)[1])


def test_script_job(job_name):
    job = create_script_job(PROJECT, REGION, job_name)
    _test_body(job)


def test_container_job(job_name):
    job = create_container_job(PROJECT, REGION, job_name)
    _test_body(job)
