import logging
from core.iDDS.useconstants import SubstitleValue
from core.iDDS.rawsqlquery import getWorkFlowProgressItemized
from core.libs.exlib import lower_dicts_in_list
import pandas as pd

_logger = logging.getLogger('bigpandamon')

CACHE_TIMEOUT = 20
OI_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

subtitleValue = SubstitleValue()


def prepare_requests_summary(workflows):
    summary = {'status': {}, 'username': {}}
    """
    completion
    age
    """
    for workflow in workflows:
        summary['status'][workflow['r_status']] = summary['status'].get(workflow['r_status'], 0) + 1
        if workflow['username'] == '':
            workflow['username'] = "Not set"
        summary['username'][workflow['username']] = summary['username'].get(workflow['username'], 0) + 1
    return summary


def get_workflow_progress_data(request_params, **kwargs):
    workflows_items = getWorkFlowProgressItemized(request_params, **kwargs)
    workflows_items = pd.DataFrame(workflows_items)
    workflows_semi_grouped = []
    if not workflows_items.empty:
        workflows_items.USERNAME.fillna(value='', inplace=True)
        workflows_pd = workflows_items.astype({"WORKLOAD_ID":str}).astype({"R_CREATED_AT":str}).groupby(['REQUEST_ID', 'R_STATUS', 'P_STATUS', 'R_NAME', 'USERNAME']).agg(
            PROCESSING_FILES_SUM=pd.NamedAgg(column="PROCESSING_FILES", aggfunc="sum"),
            PROCESSED_FILES_SUM=pd.NamedAgg(column="PROCESSED_FILES", aggfunc="sum"),
            TOTAL_FILES=pd.NamedAgg(column="TOTAL_FILES", aggfunc="sum"),
            P_STATUS_COUNT=pd.NamedAgg(column="P_STATUS", aggfunc="count"),
            R_CREATED_AT=pd.NamedAgg(column="R_CREATED_AT", aggfunc="first"),
            workload_ids=('WORKLOAD_ID', lambda x: '|'.join(x)),
        ).reset_index()
        workflows_pd = workflows_pd.astype({"R_STATUS":int, 'P_STATUS':int, "PROCESSING_FILES_SUM": int,
                                            "PROCESSED_FILES_SUM": int, "TOTAL_FILES": int, "P_STATUS_COUNT": int})
        workflows_semi_grouped = workflows_pd.values.tolist()
    workflows = {}
    for workflow_group in workflows_semi_grouped:
        workflow = workflows.setdefault(workflow_group[0], {
            "REQUEST_ID":workflow_group[0], "R_STATUS": subtitleValue.substitleValue("requests", "status")[workflow_group[1]], "CREATED_AT":workflow_group[8],"TOTAL_TASKS":0,
            "TASKS_STATUSES":{}, "TASKS_LINKS":{}, "REMAINING_FILES":0,"PROCESSED_FILES":0,"PROCESSING_FILES":0,
            "TOTAL_FILES":0, "TASKS_LINKS_ALL":''})
        workflow['TOTAL_TASKS'] += workflow_group[8]
        workflow['R_NAME'] = workflow_group[3]
        workflow['USERNAME'] = workflow_group[4]
        workflow['CREATED_AT'] = workflow_group[9]
        processing_status_name = subtitleValue.substitleValue("processings", "status")[workflow_group[2]]
        workflow["TASKS_STATUSES"][processing_status_name] = workflow_group[8]
        workflow["TASKS_LINKS_ALL"] += ('|'+ workflow_group[10].replace('.0','')) if \
            len(workflow["TASKS_LINKS_ALL"]) > 0 else \
            workflow_group[10].replace('.0','')
        workflow["TASKS_LINKS"][processing_status_name] = workflow_group[10].replace('.0','')
        workflow['PROCESSED_FILES'] += workflow_group[6]
        workflow['PROCESSING_FILES'] += workflow_group[5]
        workflow['TOTAL_FILES'] += workflow_group[7]
        workflow['REMAINING_FILES'] = workflow['TOTAL_FILES'] - workflow['PROCESSED_FILES']
    workflows = lower_dicts_in_list(list(workflows.values()))
    return workflows




