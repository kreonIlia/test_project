from src.modules.user.infrastructure import mapper as user_mapper
from src.modules.vacation.infrastructure import mapper as vacation_mapper
from src.modules.jira_employee.infrastructure import mapper as jira_employee_mapper


def start_mapper():
    user_mapper.start_mapper()
    vacation_mapper.start_mapper()
    jira_employee_mapper.start_mapper()
