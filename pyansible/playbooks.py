#!/bin/python

import os
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor import playbook_executor
from ansible.utils.display import Display

class Options(object):
    """
    Options class to replace Ansible OptParser
    """
    def __init__(self, ask_pass=None, ask_su_pass=None, ask_sudo_pass=None, ask_vault_pass=None, become=None,
                 become_ask_pass=None, become_method=None, become_user=None, check=None, connection=None,
                 diff=None, extra_vars=None, flush_cache=None, forks=None, inventory=None, listhosts=None,
                 listtags=None, listtasks=None, module_path=None, new_vault_id=None, new_vault_password_file=None,
                 private_key_file=None, remote_user=None, scp_extra_args=None, sftp_extra_args=None,
                 skip_tags=None, ssh_common_args=None, ssh_extra_args=None, start_at_task=None, step=None,
                 su=None, su_user=None, subset=None, sudo=None, sudo_user=None, syntax=None, tags=None,
                 timeout=None, vault_ids=None, vault_password_files=None, verbosity=None):

        self.ask_pass = ask_pass
        self.ask_su_pass = ask_su_pass
        self.ask_sudo_pass = ask_sudo_pass
        self.ask_vault_pass = ask_vault_pass
        self.become = become

        self.become_ask_pass = become_ask_pass
        self.become_method = become_method
        self.become_user = become_user
        self.check = check
        self.connection = connection

        self.diff = diff
        self.extra_vars = extra_vars
        self.flush_cache = flush_cache
        self.forks = forks
        self.inventory = inventory
        self.listhosts = listhosts

        self.listtags = listtags
        self.listtasks = listtasks
        self.module_path = module_path
        self.new_vault_id = new_vault_id
        self.new_vault_password_file = new_vault_password_file

        self.private_key_file = private_key_file
        self.remote_user = remote_user
        self.scp_extra_args = scp_extra_args
        self.sftp_extra_args = sftp_extra_args

        self.skip_tags = skip_tags
        self.ssh_common_args = ssh_common_args
        self.ssh_extra_args = ssh_extra_args
        self.start_at_task = start_at_task
        self.step = step

        self.su_user = su
        self.su_user = su_user
        self.subset = subset
        self.sudo = sudo
        self.sudo_user = sudo_user
        self.syntax = syntax
        self.tags = tags

        self.timeout = timeout
        self.vault_ids = vault_ids
        self.vault_password_files = vault_password_files
        self.verbosity = verbosity

class Runner(object):

    def __init__(self, cfg_file, hosts_file, playbook_file, private_key_file, module_path, run_data, become_pass, verbosity=0):

        self.hosts_file = hosts_file
        self.playbook_file = playbook_file
        self.run_data = run_data

        self.options = Options()
        self.options.private_key_file = private_key_file
        self.options.verbosity = verbosity
        self.options.module_path = module_path
        self.options.connection = 'ssh'

        # set verbosity
        self.display = Display()
        self.display.verbosity = self.options.verbosity
        playbook_executor.verbosity = self.options.verbosity

        # Become Pass Needed if not logging in as user root
        if become_pass:
            self.options.become = True
            self.options.become_method = 'sudo'
            self.options.become_user = 'root'
            passwords = {'become_pass': become_pass}
        else:
            passwords = {}

        # Gets data from YAML/JSON files
        self.loader = DataLoader()
        self.loader.set_vault_password(os.environ['VAULT_PASS'])

        # Set inventory, using most of above objects
        self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=self.hosts_file)
        self.variable_manager = VariableManager(loader=loader, inventory=inventory)

        # Setup playbook executor, but don't run until run() called
        self.pbex = playbook_executor.PlaybookExecutor(
            playbooks=[self.playbook_file],
            inventory=self.inventory, 
            variable_manager=self.variable_manager,
            loader=self.loader, 
            options=self.options, 
            passwords=passwords)

    def run(self):
        # Results of PlaybookExecutor
        self.pbex.run()
