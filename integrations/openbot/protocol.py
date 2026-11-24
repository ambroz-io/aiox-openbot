"""Pure validation helpers; live execution uses OpenBot tools, not this module."""
ROLES = frozenset(('aiox-master', 'dev', 'qa', 'architect', 'analyst', 'pm', 'po', 'sm', 'data-engineer', 'ux-design-expert', 'devops', 'squad-creator'))

def can_delegate(sender, recipient):
    return sender == 'aiox-master' and recipient in ROLES - {'aiox-master'}

def accept_result(task, result):
    if task.get('status') != 'running':
        raise ValueError('Task is not running: duplicate or late result')
    for key in ('task_id', 'attempt', 'role'):
        if key not in task or result.get(key) != task[key]:
            raise ValueError('Mismatched ' + key)
    if result.get('status') == 'blocked':
        return 'blocked'
    if result.get('status') != 'completed' or not result.get('evidence'):
        raise ValueError('Completion requires evidence')
    return 'review'

def can_close(status, qa_verdict, evidence_checked):
    return status == 'review' and qa_verdict == 'PASS' and evidence_checked is True
