from logging import debug

from gitlabform.gitlab import GitLab
from gitlabform.processors.abstract_processor import AbstractProcessor


class RunnersProcessor(AbstractProcessor):
    def __init__(self, gitlab: GitLab):
        super().__init__("runners", gitlab)

    def _process_configuration(self, project_and_group: str, configuration: dict):
        project = self.gl.get_project_by_path_cached(name=project_and_group, lazy=True)
        runner_list = project.runners.list()
        debug(runner_list)

        for runner_id in sorted(configuration["runners"]):
            debug("Runner: " + runner_id)
            id_enabled = any(runner.id == int(runner_id) for runner in runner_list)

            if configuration["runners"][runner_id]["enabled"] and not id_enabled:
                project.runners.create({'runner_id': runner_id})
            elif not configuration["runners"][runner_id]["enabled"] and id_enabled:
                project.runners.delete(runner_id)
                
