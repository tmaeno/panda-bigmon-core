#!/usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0OA
#
# Authors:
# - Wen Guan, <wen.guan@cern.ch>, 2019

"""
Constants.
"""

from enum import Enum


SCOPE_LENGTH = 25
NAME_LENGTH = 255


class Sections:
    Main = 'main'
    Common = 'common'
    Clerk = 'clerk'
    Transformer = 'transformer'
    Transporter = 'transporter'
    Carrier = 'carrier'
    Conductor = 'conductor'


class HTTP_STATUS_CODE:
    OK = 200
    Created = 201
    Accepted = 202

    # Client Errors
    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404
    NoMethod = 405
    Conflict = 409

    # Server Errors
    InternalError = 500


class RequestStatus(Enum):
    New = 0
    Ready = 1
    Transforming = 2
    Finished = 3
    SubFinished = 4
    Failed = 5
    Extend = 6
    ToCancel = 7
    Cancelling = 8
    Cancelled = 9
    ToSuspend = 10
    Suspending = 11
    Suspended = 12
    ToResume = 13
    Resuming = 14
    ToExpire = 15
    Expiring = 16
    Expired = 17


class RequestLocking(Enum):
    Idle = 0
    Locking = 1


class RequestType(Enum):
    Workflow = 0
    EventStreaming = 1
    StageIn = 2
    ActiveLearning = 3
    HyperParameterOpt = 4
    Derivation = 5
    Other = 99


class TransformType(Enum):
    Workflow = 0
    EventStreaming = 1
    StageIn = 2
    ActiveLearning = 3
    HyperParameterOpt = 4
    Derivation = 5
    Processing = 6
    Actuating = 7
    Other = 99


class TransformStatus(Enum):
    New = 0
    Ready = 1
    Transforming = 2
    Finished = 3
    SubFinished = 4
    Failed = 5
    Extend = 6
    ToCancel = 7
    Cancelling = 8
    Cancelled = 9
    ToSuspend = 10
    Suspending = 11
    Suspended = 12
    ToResume = 13
    Resuming = 14
    ToExpire = 15
    Expiring = 16
    Expired = 17


class TransformLocking(Enum):
    Idle = 0
    Locking = 1


class CollectionType(Enum):
    Container = 0
    Dataset = 1
    File = 2
    PseudoDataset = 3


class CollectionRelationType(Enum):
    Input = 0
    Output = 1
    Log = 2


class CollectionStatus(Enum):
    New = 0
    Updated = 1
    Processing = 2
    Open = 3
    Closed = 4
    SubClosed = 5
    Failed = 6
    Deleted = 7
    Cancelled = 8
    Suspended = 9


class CollectionLocking(Enum):
    Idle = 0
    Locking = 1


class ContentType(Enum):
    File = 0
    Event = 1
    PseudoContent = 2


class ContentStatus(Enum):
    New = 0
    Processing = 1
    Available = 2
    Failed = 3
    FinalFailed = 4
    Lost = 5
    Deleted = 6
    Mapped = 7


class GranularityType(Enum):
    File = 0
    Event = 1


class ProcessingStatus(Enum):
    New = 0
    Submitting = 1
    Submitted = 2
    Running = 3
    Finished = 4
    Failed = 5
    Lost = 6
    Cancel = 7
    FinishedOnStep = 8
    FinishedOnExec = 9
    FinishedTerm = 10
    SubFinished = 11
    ToCancel = 12
    Cancelling = 13
    Cancelled = 14
    ToSuspend = 15
    Suspending = 16
    Suspended = 17
    ToResume = 18
    Resuming = 19
    ToExpire = 20
    Expiring = 21
    Expired = 22
    TimeOut = 23


class ProcessingLocking(Enum):
    Idle = 0
    Locking = 1


class MessageType(Enum):
    StageInFile = 0
    StageInCollection = 1
    StageInWork = 2
    ActiveLearningFile = 3
    ActiveLearningCollection = 4
    ActiveLearningWork = 5
    HyperParameterOptFile = 6
    HyperParameterOptCollection = 7
    HyperParameterOptWork = 8
    ProcessingFile = 9
    ProcessingCollection = 10
    ProcessingWork = 11
    HealthHeartbeat = 12
    UnknownFile = 97
    UnknownCollection = 98
    UnknownWork = 99


class MessageStatus(Enum):
    New = 0
    Fetched = 1
    Delivered = 2


class MessageLocking(Enum):
    Idle = 0
    Locking = 1


class MessageSource(Enum):
    Clerk = 0
    Transformer = 1
    Transporter = 2
    Carrier = 3
    Conductor = 4