# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import proto  # type: ignore

from google.cloud.batch_v1.types import volume
from google.protobuf import duration_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.cloud.batch.v1",
    manifest={
        "ComputeResource",
        "StatusEvent",
        "TaskExecution",
        "TaskStatus",
        "Runnable",
        "TaskSpec",
        "LifecyclePolicy",
        "Task",
        "Environment",
    },
)


class ComputeResource(proto.Message):
    r"""Compute resource requirements

    Attributes:
        cpu_milli (int):
            The milliCPU count.
        memory_mib (int):
            Memory in MiB.
        boot_disk_mib (int):
            Extra boot disk size in MiB for each task.
    """

    cpu_milli = proto.Field(
        proto.INT64,
        number=1,
    )
    memory_mib = proto.Field(
        proto.INT64,
        number=2,
    )
    boot_disk_mib = proto.Field(
        proto.INT64,
        number=4,
    )


class StatusEvent(proto.Message):
    r"""Status event

    Attributes:
        type_ (str):
            Type of the event.
        description (str):
            Description of the event.
        event_time (google.protobuf.timestamp_pb2.Timestamp):
            The time this event occurred.
        task_execution (google.cloud.batch_v1.types.TaskExecution):
            Task Execution
    """

    type_ = proto.Field(
        proto.STRING,
        number=3,
    )
    description = proto.Field(
        proto.STRING,
        number=1,
    )
    event_time = proto.Field(
        proto.MESSAGE,
        number=2,
        message=timestamp_pb2.Timestamp,
    )
    task_execution = proto.Field(
        proto.MESSAGE,
        number=4,
        message="TaskExecution",
    )


class TaskExecution(proto.Message):
    r"""This Task Execution field includes detail information for
    task execution procedures, based on StatusEvent types.

    Attributes:
        exit_code (int):
            When task is completed as the status of
            FAILED or SUCCEEDED, exit code is for one task
            execution result, default is 0 as success.
    """

    exit_code = proto.Field(
        proto.INT32,
        number=1,
    )


class TaskStatus(proto.Message):
    r"""Status of a task

    Attributes:
        state (google.cloud.batch_v1.types.TaskStatus.State):
            Task state
        status_events (Sequence[google.cloud.batch_v1.types.StatusEvent]):
            Detailed info about why the state is reached.
    """

    class State(proto.Enum):
        r"""Task states."""
        STATE_UNSPECIFIED = 0
        PENDING = 1
        ASSIGNED = 2
        RUNNING = 3
        FAILED = 4
        SUCCEEDED = 5

    state = proto.Field(
        proto.ENUM,
        number=1,
        enum=State,
    )
    status_events = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="StatusEvent",
    )


class Runnable(proto.Message):
    r"""Runnable describes instructions for executing a specific
    script or container as part of a Task.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        container (google.cloud.batch_v1.types.Runnable.Container):
            Container runnable.

            This field is a member of `oneof`_ ``executable``.
        script (google.cloud.batch_v1.types.Runnable.Script):
            Script runnable.

            This field is a member of `oneof`_ ``executable``.
        barrier (google.cloud.batch_v1.types.Runnable.Barrier):
            Barrier runnable.

            This field is a member of `oneof`_ ``executable``.
        ignore_exit_status (bool):
            Normally, a non-zero exit status causes the
            Task to fail. This flag allows execution of
            other Runnables to continue instead.
        background (bool):
            This flag allows a Runnable to continue
            running in the background while the Task
            executes subsequent Runnables. This is useful to
            provide services to other Runnables (or to
            provide debugging support tools like SSH
            servers).
        always_run (bool):
            By default, after a Runnable fails, no further Runnable are
            executed. This flag indicates that this Runnable must be run
            even if the Task has already failed. This is useful for
            Runnables that copy output files off of the VM or for
            debugging.

            The always_run flag does not override the Task's overall
            max_run_duration. If the max_run_duration has expired then
            no further Runnables will execute, not even always_run
            Runnables.
        environment (google.cloud.batch_v1.types.Environment):
            Environment variables for this Runnable
            (overrides variables set for the whole Task or
            TaskGroup).
        timeout (google.protobuf.duration_pb2.Duration):
            Timeout for this Runnable.
    """

    class Container(proto.Message):
        r"""Container runnable.

        Attributes:
            image_uri (str):
                The URI to pull the container image from.
            commands (Sequence[str]):
                Overrides the ``CMD`` specified in the container. If there
                is an ENTRYPOINT (either in the container image or with the
                entrypoint field below) then commands are appended as
                arguments to the ENTRYPOINT.
            entrypoint (str):
                Overrides the ``ENTRYPOINT`` specified in the container.
            volumes (Sequence[str]):
                Volumes to mount (bind mount) from the host
                machine files or directories into the container,
                formatted to match docker run's --volume option,
                e.g. /foo:/bar, or /foo:/bar:ro
            options (str):
                Arbitrary additional options to include in
                the "docker run" command when running this
                container, e.g. "--network host".
            block_external_network (bool):
                If set to true, external network access to
                and from container will be blocked. The
                container will use the default internal network
                'goog-internal'.
            username (str):
                Optional username for logging in to a docker registry. If
                username matches `projects/*/secrets/*/versions/*` then
                Batch will read the username from the Secret Manager.
            password (str):
                Optional password for logging in to a docker registry. If
                password matches `projects/*/secrets/*/versions/*` then
                Batch will read the password from the Secret Manager;
        """

        image_uri = proto.Field(
            proto.STRING,
            number=1,
        )
        commands = proto.RepeatedField(
            proto.STRING,
            number=2,
        )
        entrypoint = proto.Field(
            proto.STRING,
            number=3,
        )
        volumes = proto.RepeatedField(
            proto.STRING,
            number=7,
        )
        options = proto.Field(
            proto.STRING,
            number=8,
        )
        block_external_network = proto.Field(
            proto.BOOL,
            number=9,
        )
        username = proto.Field(
            proto.STRING,
            number=10,
        )
        password = proto.Field(
            proto.STRING,
            number=11,
        )

    class Script(proto.Message):
        r"""Script runnable.

        This message has `oneof`_ fields (mutually exclusive fields).
        For each oneof, at most one member field can be set at the same time.
        Setting any member of the oneof automatically clears all other
        members.

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            path (str):
                Script file path on the host VM.

                This field is a member of `oneof`_ ``command``.
            text (str):
                Shell script text.

                This field is a member of `oneof`_ ``command``.
        """

        path = proto.Field(
            proto.STRING,
            number=1,
            oneof="command",
        )
        text = proto.Field(
            proto.STRING,
            number=2,
            oneof="command",
        )

    class Barrier(proto.Message):
        r"""Barrier runnable blocks until all tasks in a taskgroup reach
        it.

        Attributes:
            name (str):
                Barriers are identified by their index in
                runnable list. Names are not required, but if
                present should be an identifier.
        """

        name = proto.Field(
            proto.STRING,
            number=1,
        )

    container = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="executable",
        message=Container,
    )
    script = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="executable",
        message=Script,
    )
    barrier = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="executable",
        message=Barrier,
    )
    ignore_exit_status = proto.Field(
        proto.BOOL,
        number=3,
    )
    background = proto.Field(
        proto.BOOL,
        number=4,
    )
    always_run = proto.Field(
        proto.BOOL,
        number=5,
    )
    environment = proto.Field(
        proto.MESSAGE,
        number=7,
        message="Environment",
    )
    timeout = proto.Field(
        proto.MESSAGE,
        number=8,
        message=duration_pb2.Duration,
    )


class TaskSpec(proto.Message):
    r"""Spec of a task

    Attributes:
        runnables (Sequence[google.cloud.batch_v1.types.Runnable]):
            The sequence of scripts or containers to run for this Task.
            Each Task using this TaskSpec executes its list of runnables
            in order. The Task succeeds if all of its runnables either
            exit with a zero status or any that exit with a non-zero
            status have the ignore_exit_status flag.

            Background runnables are killed automatically (if they have
            not already exited) a short time after all foreground
            runnables have completed. Even though this is likely to
            result in a non-zero exit status for the background
            runnable, these automatic kills are not treated as Task
            failures.
        compute_resource (google.cloud.batch_v1.types.ComputeResource):
            ComputeResource requirements.
        max_run_duration (google.protobuf.duration_pb2.Duration):
            Maximum duration the task should run.
            The task will be killed and marked as FAILED if
            over this limit.
        max_retry_count (int):
            Maximum number of retries on failures. The default, 0, which
            means never retry. The valid value range is [0, 10].
        lifecycle_policies (Sequence[google.cloud.batch_v1.types.LifecyclePolicy]):
            Lifecycle management schema when any task in a task group is
            failed. The valid size of lifecycle policies are [0, 10].
            For each lifecycle policy, when the condition is met, the
            action in that policy will execute. If there are multiple
            policies that the task execution result matches, we use the
            action from the first matched policy. If task execution
            result does not meet with any of the defined lifecycle
            policy, we consider it as the default policy. Default policy
            means if the exit code is 0, exit task. If task ends with
            non-zero exit code, retry the task with max_retry_count.
        environments (Mapping[str, str]):
            Environment variables to set before running
            the Task. You can set up to 100 environments.
        volumes (Sequence[google.cloud.batch_v1.types.Volume]):
            Volumes to mount before running Tasks using
            this TaskSpec.
        environment (google.cloud.batch_v1.types.Environment):
            Environment variables to set before running
            the Task.
    """

    runnables = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="Runnable",
    )
    compute_resource = proto.Field(
        proto.MESSAGE,
        number=3,
        message="ComputeResource",
    )
    max_run_duration = proto.Field(
        proto.MESSAGE,
        number=4,
        message=duration_pb2.Duration,
    )
    max_retry_count = proto.Field(
        proto.INT32,
        number=5,
    )
    lifecycle_policies = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="LifecyclePolicy",
    )
    environments = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=6,
    )
    volumes = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message=volume.Volume,
    )
    environment = proto.Field(
        proto.MESSAGE,
        number=10,
        message="Environment",
    )


class LifecyclePolicy(proto.Message):
    r"""LifecyclePolicy describes how to deal with task failures
    based on different conditions.

    Attributes:
        action (google.cloud.batch_v1.types.LifecyclePolicy.Action):
            Action to execute when ActionCondition is
            true.
        action_condition (google.cloud.batch_v1.types.LifecyclePolicy.ActionCondition):
            Conditions that decide why a task failure is
            dealt with a specific action.
    """

    class Action(proto.Enum):
        r"""Action on task failures based on different conditions."""
        ACTION_UNSPECIFIED = 0
        RETRY_TASK = 1
        FAIL_TASK = 2

    class ActionCondition(proto.Message):
        r"""Conditions for actions to deal with task failures.

        Attributes:
            exit_codes (Sequence[int]):
                Exit codes of a task execution.
                If there are more than 1 exit codes,
                when task executes with any of the exit code in
                the list, the condition is met and the action
                will be executed.
        """

        exit_codes = proto.RepeatedField(
            proto.INT32,
            number=1,
        )

    action = proto.Field(
        proto.ENUM,
        number=1,
        enum=Action,
    )
    action_condition = proto.Field(
        proto.MESSAGE,
        number=2,
        message=ActionCondition,
    )


class Task(proto.Message):
    r"""A Cloud Batch task.

    Attributes:
        name (str):
            Task name.
            The name is generated from the parent TaskGroup
            name and 'id' field. For example:
            "projects/123456/locations/us-west1/jobs/job01/taskGroups/group01/tasks/task01".
        status (google.cloud.batch_v1.types.TaskStatus):
            Task Status.
    """

    name = proto.Field(
        proto.STRING,
        number=1,
    )
    status = proto.Field(
        proto.MESSAGE,
        number=2,
        message="TaskStatus",
    )


class Environment(proto.Message):
    r"""An Environment describes a collection of environment
    variables to set when executing Tasks.

    Attributes:
        variables (Mapping[str, str]):
            A map of environment variable names to
            values.
    """

    variables = proto.MapField(
        proto.STRING,
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
