"""
Git operations followed by email operation
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta
def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'add_file_1' block
    add_file_1(container=container)

    # call 'prompt_1' block
    prompt_1(container=container)

    return

def add_file_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('add_file_1() called')

    artifact_count_value = container.get('artifact_count', None)

    # collect data for 'add_file_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.filePath', 'artifact:*.cef.vaultId', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'add_file_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'file_path': container_item[0],
                'contents': artifact_count_value,
                'vault_id': container_item[1],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[2]},
            })

    phantom.act(action="add file", parameters=parameters, assets=['gitassetsplunk'], callback=git_commit_1, name="add_file_1")

    return

def git_commit_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('git_commit_1() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'git_commit_1' call

    parameters = []
    
    # build parameters list for 'git_commit_1' call
    parameters.append({
        'message': "committed from phantom",
        'push': True,
    })

    phantom.act(action="git commit", parameters=parameters, assets=['gitassetsplunk'], callback=send_email_1, name="git_commit_1", parent_action=action)

    return

def send_email_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('send_email_1() called')
        
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'send_email_1' call

    parameters = []
    
    # build parameters list for 'send_email_1' call
    parameters.append({
        'from': "Splunk@admin.com",
        'to': "testertesting070@gmail.com",
        'cc': "",
        'bcc': "",
        'subject': "PLaybook Execution for git operations",
        'body': "The Playbook operations are started and the mail operation is cleared",
        'attachments': "",
        'headers': "",
    })

    phantom.act(action="send email", parameters=parameters, assets=['smtp'], name="send_email_1", parent_action=action)

    return

def prompt_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, **kwargs):
    phantom.debug('prompt_1() called')
    
    # set user and message variables for phantom.prompt call
    user = "admin"
    message = """Hello There this is to specify that the playbook has been activated and a prompt has been initiated, you have 30 minutes to respond back."""

    #responses:
    response_types = [
        {
            "prompt": "",
            "options": {
                "type": "message",
            },
        },
    ]

    phantom.prompt2(container=container, user=user, message=message, respond_in_mins=30, name="prompt_1", response_types=response_types)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return