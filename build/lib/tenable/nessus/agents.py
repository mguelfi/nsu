from .base import NessusEndpoint

class AgentsAPI(NessusEndpoint):

    def list(self):
        '''
        Retrieves the list of agent groups configured

        Args: None

        Returns:
             list: Listing of agent group resource records

        Examples:
            >>>> for agent in nessus.agents.list():
            ...     pprint(agent)

        '''
        return self._api.get('agents').json()['agents']
    
    def delete(self, *agent_ids):
        '''
        Delete an agent.

        `agent: delete <https://cloud.tenable.com/api#/resources/agents/delete>`_

        Args:
            agent_ids (int): The id of the agent to delete

        Examples:
            >>> nessus.agent.delete(1)
        '''
        if len(agent_ids) <= 1:
            self._api.delete('agents/{}'.format(
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            self._api.delete('agents',
                json={'ids': [self._check('agents', i, int) for i in agent_ids]})
            
    def unlink(self, *agent_ids):
        '''
        Unlink an agent.

        `agent: unlink <https://cloud.tenable.com/api#/resources/agents/unlink>`_

        Args:
            agent_ids (int): The id of the agent to unlink

        Returns:
            None: Agent unlinked successfully

        Examples:
            >>> nessus.agent.unlink(1)
        '''
        if len(agent_ids) <= 1:
            self._api.delete('agents/{}/unlink'.format(
                self._check('agent_id', agent_ids[0], int)
            ))
        else:
            return self._api.delete('agents/unlink',
                json={'ids': [self._check('agents', i, int) for i in agent_ids]}).json()
            