#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: updation
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the classes related to T_System's updating itself ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import os  # Miscellaneous operating system interfaces
import inspect  # Inspect live objects
import subprocess  # Subprocess managements
import time  # Time access and conversions
import hashlib
import git

from elevate import elevate  # partial root authentication interface

from t_system.db_fetching import DBFetcher
from t_system import dot_t_system_dir, T_SYSTEM_PATH
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


class UpdateManager:
    """Class to define an update manager for managing updates and installation after updates.

    This class provides necessary initiations and functions named :func:`t_system.updation.UpdateManager.update`for provide update code and install necessary dependencies.
    """

    def __init__(self, editable=False, verbose=False):
        """Initialization method of :class:`t_system.updation.UpdateManager` class.

        Args:
                editable:   	        Editable updation mode flag. For making updates as development.
                verbose:   	            Verbosity flag about printing debug messages.
        """
        self.editable = editable
        self.verbose = verbose  # this argument will be added.

        self.table = DBFetcher(dot_t_system_dir, "db", "update").fetch()

        self.auto_update = None
        self.refresh_members()

        self.updater = Updater(self.verbose)
        self.installer = Installer(self.editable, self.verbose)

    def update(self):
        """Method to pulling updates from remote git repo, checking differences inside installation scripts and starting the installation if necessary.
        """
        if self.is_update_available():
            self.updater.update_self()
            self.installer.install()
            return True
        return False

    def is_update_auto(self):
        """Method to getting auto-update status from the database.
        """

        return self.auto_update

    def is_update_available(self):
        """Method to getting availability of the update from remote software repository.
        """

        return self.updater.is_update_available()

    def db_upsert(self, auto_update):
        """Function to insert(or update) the update status to the database.

        Args:
                auto_update (bool):     Auto update flag of the UpdateManager

        Returns:
                str:  Response.
        """

        update = self.table.all()

        if update:
            self.table.update({'auto_update': auto_update})
        else:
            self.table.insert({
                'auto_update': auto_update,
            })  # insert the given data

        return ""

    def refresh_members(self):
        """low-level method to refreshing the members
        """

        update = self.table.all()
        if update:
            self.auto_update = update[0]["auto_update"]
        else:
            self.auto_update = False
            self.db_upsert(self.auto_update)

    def change_members(self, auto_update):
        """high-level method to changing members via given parameters.

        Args:
                auto_update (bool):     Auto update flag of the UpdateManager

        Returns:
                str:  Response.
        """

        self.db_upsert(auto_update)
        self.refresh_members()

    def set_editability(self, editable):
        """Method to set editable member externally.

        Args:
                editable:   	        Editable updation mode flag. For making updates as development.
        """

        self.editable = editable

    def set_verbosity(self, verbose):
        """Method to set verbose member externally.

        Args:
                verbose:   	            Verbosity flag about printing debug messages.
        """

        self.verbose = verbose

    def listen_updates(self):
        """Method to controlling repo is up-to-date with updater object. (Deprecated)
        """

        while True:
            if self.updater.is_update_available():
                return True
            time.sleep(43200)  # per 12 hours


class Updater:
    """Class to define an updater of tracking system itself.

    This class provides necessary initiations and functions named :func:`t_system.updation.Updater.update`
    as the update point from the remote git repository, named :func:`t_system.updation.Updater.pull`
    for pulling repo data and named :func:`t_system.updation.Updater.push` for git push.
    """

    def __init__(self, verbose):
        """Initialization method of :class:`t_system.updation.Updater` class.

        Args:
                verbose:   	            Verbosity flag about printing debug messages.
        """
        self.verbose = verbose  # this argument will be added.

    def update_self(self, force=False, check_dev=True, verbose=False):
        """Method that can be called to automatically update the repo in which the calling file is located.

        Args:
                force (bool):           Force pull flag.
                check_dev:   	        Flag to check development environment.
                verbose:   	            Verbosity flag about printing debug messages.
        """
        self.pull(force=force, check_dev=check_dev, verbose=verbose)
        self.__print(verbose, "Pulled any possible remote changes")

    def is_update_available(self, verbose=False):
        """Method to check git repo is up-to-date with git.fetch.

        Args:
                verbose:   	            Verbosity flag about printing debug messages.
        Returns:
                bool: Result flag.
        """

        repo_path = self.__find_repo()
        repo = git.Repo(repo_path)

        # fetch all
        fetch_resp = str(repo.git.fetch("--all"))
        self.__print(verbose, "Fetched any and all changes with response: {}".format(fetch_resp))

        if "Your branch is up-to-date" in repo.git.status():
            self.__print(verbose, "Status check passes.\nCode up to date.")
            return False
        else:
            self.__print(verbose, "Code update available.")
            return True

    def pull(self, force=False, check_dev=True, verbose=False):
        """Method to attempt to pull any remote changes down to the repository that the calling script is contained in. If
        there are any file conflicts the pull will fail and the function will return. This function is *safe* and does not perform
        destructive actions on the repo it is being called on. This function returns a tuple containing 2 fields. The first is a
        boolean value that indicates if the pull was successful or not. The second field contains a list of the files that were effected
        by the pull. If the pull was successful, this is the files that were updated by the pull action. If the pull was unsuccessful,
        this list contains the files that have conflicts and stopped the pull. All files listed in the case of a success or failure are
        referenced relative to the base of the repository. This function attempts to capture git errors but it is entirely possible that
        it does not handle a git error correctly in which case it will be raised again to be potentially handled higher up.

        Args:
                force (bool):           Force pull flag.
                check_dev:   	        Flag to check development environment.
                verbose:   	            Verbosity flag about printing debug messages.
        """
        repo_path = self.__find_repo()
        repo = git.Repo(repo_path)
        if not force:
            try:
                resp = str(repo.git.pull()).splitlines()
                if resp[0] == "Already up-to-date.":
                    self.__print(verbose, "Repository is already up to date.")
                    return False, []

                files = [a.split("|")[0][1:-1] for a in resp[2:-1]]
                self.__print(verbose, "Files that were updated:" + "\n  ".join(files))
                return True, files

            except git.exc.GitCommandError as err:
                err_list = str(err).splitlines()

                # this is a poor and rudimentary way to tell if there was a specific error TODO: fix
                if err_list[3] == "  stderr: 'error: Your local changes to the following files would be overwritten by merge:":
                    files = [a[1:] for a in err_list[4:-2]]
                    self.__print(verbose, "Pull failed. Files with conflicts:" + "\n  ".join(files))
                    return False, files
                # we got an error we didn't expect, pass it back up
                raise
        else:
            if check_dev and self.__is_dev_env(repo_path):
                self.__print(verbose, "Detected development environment. Aborting hard pull")
                return False, []

            branch = self.__find_current_branch(repo)

            # record the diff, these will all replaced
            diffs = self.__get_file_diffs(repo)

            if len(diffs) == 0:
                return False, []

            # fetch all
            fetch_resp = str(repo.git.fetch("--all"))
            self.__print(verbose, "Fetched any and all changes with response: {}".format(fetch_resp))
            # reset
            reset_resp = str(repo.git.reset("--hard", "origin/{}".format(branch)))
            self.__print(verbose, "Completed hard pull with response: {}".format(reset_resp))
            # clean
            clean_resp = str(repo.git.clean("-f"))
            self.__print(verbose, "Completed clean with response: {}".format(clean_resp))
            return True, diffs

    def push(self, force=False, check_dev=True, message="Pushing up changes with python updation", username=None, password=None, verbose=False):
        """The higgh-level method to perform a push up of all local changes that have been made into a repo. However, if there is a file conflict this function will
        raise a SystemError flag if force is set to False. If force is True, it will force the push. The function will first run "git add -A", followed up by
        "git commit -m 'users message here'" and finally "git push" or possibly "git push <credentials>" if needed. If the function is called with the
        username and password populated it will attempt to push using the provided credentials otherwise it will fall back to simply "git push". This method
        is currently unable to handle repositories that may need credentials and that are protected with 2-factor authentication. It is recommended to
        clone the repo using SSH to avoid issues in this case.

        Args:
                force (bool):           Force pull flag.
                check_dev:   	        Flag to check development environment.
                message:   	            Commit message of git.
                username:   	        Username of the pushed repository.
                password:   	        Password of the pushed repository.
                verbose:   	            Verbosity flag about printing debug messages.
        """
        repo_path = self.__find_repo()
        repo = git.Repo(repo_path)

        if check_dev and self.__is_dev_env(repo_path) and force:
            self.__print(verbose, "Detected development environment. Aborting hard pull")
            return

        conflicts = self.__get_file_conflicts(repo)
        if len(conflicts) != 0 and not force:
            self.__print(verbose, "Can not push, there are file conflicts")
            raise SystemError("Can not push up changes when there are file conflicts")

        # perform "git add -A"
        add_resp = str(repo.git.add("-A"))
        self.__print(verbose, "Added all local changes with response: {}".format(add_resp))

        # perform "git commit -m '<message>'"
        try:
            commit_resp = str(repo.git.commit("-m", "'{}'".format(message)))
            self.__print(verbose, "Commit all local changes with response: {}".format(commit_resp))
        except git.exc.GitCommandError:
            # TODO: handle errors that may occur when doing a commit
            pass

        # perform "git push" with credentials if provided
        try:
            if username is not None and password is not None:
                # user is attempting to send credentials with the push, fabricate URL
                repo_url = str(repo.git.remote("-v")).splitlines()[0][7:-8].split("//")[1]
                repo_url = "https://{}:{}@{}".format(username, password, repo_url)
                if force:
                    push_resp = str(repo.git.push(repo_url, "-f"))
                else:
                    push_resp = str(repo.git.push(repo_url))
            else:
                branch = self.__find_current_branch(repo)
                if force:
                    push_resp = str(repo.git.push("origin", branch, "-f"))
                else:
                    push_resp = str(repo.git.push("origin", branch))
            self.__print(verbose, "Push all local changes with response: {}".format(push_resp))
        except git.exc.GitCommandError as err:
            err = str(err).splitlines()
            # handle incorrect username/password
            if "remote: Invalid username or password." in err[-2]:
                self.__print(verbose, "Wrong login credentials, authentication failed")
                raise ValueError("Wrong login credentials, authentication failed")
            # correct credentials but something else went wrong, most likely 2-factor auth
            elif "remote: Anonymous access to " in err[-2]:
                self.__print(verbose, "Cannot gain access, authentication failed. This is often caused by 2-factor authentication")
                raise ValueError("Cannot gain access, authentication failed. This is often caused by 2-factor authentication")
            # we really goofed, pass the error along
            else:
                raise

    def update_git_repo(self, force=False, check_dev=True, message="Pushing up changes with python selfupdate", username=None, password=None, verbose=False):
        """Method that can be called to automatically update the repo in which the calling file is located.
        The 'force' parameter will cause the module to force do a pull and push. This is a destructive action that can
        cause loss of local data. 'check_dev' when set to True will not allow any destructive action to take place IFF
        the calling script is in a updation dev environment. 'message' is the commit message that will be used when
        changes are pushed up to the remote repo. If the remote repo is password protected you will need to provide the
        username and password so that the push does not fail.

        Args:
                force (bool):           Force pull flag.
                check_dev:   	        Flag to check development environment.
                message:   	            Message to show  during git push.
                username:   	        Username of the pushed repository.
                password:   	        Password of the pushed repository.
                verbose:   	            Verbosity flag about printing debug messages.
        """
        if force:
            self.push(force=force, check_dev=check_dev, message=message, username=username, password=password, verbose=verbose)
            self.__print(verbose, "Pushed any possible local changes")
            self.pull(force=force, check_dev=check_dev, verbose=verbose)
            self.__print(verbose, "Pulled any possible remote changes")
        else:
            self.pull(force=force, check_dev=check_dev, verbose=verbose)
            self.__print(verbose, "Pulled any possible remote changes")
            self.push(force=force, check_dev=check_dev, message=message, username=username, password=password, verbose=verbose)
            self.__print(verbose, "Pushed any possible local changes")

    def __print(self, verbose, msg):
        """Method to help assist in adding debug messages throughout the code. Print messages are formated as such:
        <name of calling function>:<line #> :: <msg>

        Args:
                verbose:   	            Verbosity flag about printing debug messages.
                msg:       	            The debug message that will be printed.
        """
        if not self.verbose and not verbose:
            return

        stack = inspect.stack()
        calling_func = stack[1][3]
        line = stack[1][2]
        msg.replace("\n", "\n           ".format(calling_func, line))

        logger.debug(f'{calling_func}():{line} :: {msg}')

    def __get_calling_file(self, verbose=False):
        """Method to go through the python call stack and find the script that originally called into this file.
        Returns a tuple where the first element is a string that is the folder containing the calling script,
        and the second element is the name of the file name of the calling script. If a file can not
        be found for some reason a LookupError is raised to indicate that an external script could not be found.

        Args:
                verbose:   	            Verbosity flag about printing debug messages.
        """
        stack = inspect.stack()
        this_file = stack[0][1]
        for i in range(1, len(stack)):
            if stack[i][1] != this_file:
                complete_path = os.path.normpath(os.getcwd() + "/" + stack[i][1])
                self.__print(verbose, "Module was called from: {}".format(complete_path))
                return os.path.split(complete_path)

        self.__print(verbose, "Module was not called by an external script.")
        raise LookupError("Module was not called by an external script.")

    def __find_repo(self, verbose=False):
        """Method to go figure out if the calling python script is inside a git repo, and if so, return a string that is the
        location of the base of the git repo. If the script is not, a LookupError is raised to indicate it could not find the repo.

        Args:
                verbose:   	            Verbosity flag about printing debug messages.
        """
        file_path, file_name = self.__get_calling_file()
        # walk up the file tree looking for a valid git repo, stop when we hit the base
        while True:
            if os.path.samefile(os.path.normpath(file_path), os.path.normpath("/")):
                self.__print(verbose, "Calling script is not in a valid git repo")
                raise LookupError("Calling script is not in a valid git repo")

            try:
                git.Repo(file_path)
                self.__print(verbose, "Found root of repo located at: {}".format(os.path.normpath(file_path)))
                return os.path.normpath(file_path)
            except git.exc.InvalidGitRepositoryError:
                file_path = os.path.normpath(file_path + "/..")

    def __find_current_branch(self, repo, verbose=False):
        """Method that returns the name of the current branch. If for some reason the function fails to find the current branch
        an IOError is raised to indicate something has gone wrong.

        Args:
                repo:   	            git.repo.base.Repo object.
                verbose:   	            Verbosity flag about printing debug messages.
        """
        assert type(repo) is git.repo.base.Repo, "Passed in repo needs to be of type 'git.repo.base.Repo'"
        branches = str(repo.git.branch()).splitlines()
        for branch in branches:
            # asterix represents current branch, search for it
            if branch[0] == "*":
                self.__print(verbose, "Found current branch to be: {}".format(branch[2:]))
                return branch[2:]
        self.__print(verbose, "Failed to find current branch")
        raise IOError("Failed to find current branch")

    def __is_dev_env(self, directory, suppress_errors=False, verbose=False):
        """Method to return 'True' if the git repo is setup to be a updation development environment. This indicates that
        functions that perform destructive file manipulation will be limited in scope as to not cause the script to complicate
        development efforts when using the updation module. A updation development environment is configured by placing
        an empty file in the root directory of the repo simply named '.devenv'. This file must also be included in the .gitignore
        or a EnvironmentError will be raised. This is to avoid the propagation of the development environment file to the main
        repo and any other local repositories that would then pull this file down and turn themselves into development
        environments. This error can be suppressed by setting the argument 'suppress_errors' to 'True' when calling is_dev_env().
        Suppressing this error can cause remote repos that rely on updation to no longer update successfully without direct
        user input. You have been warned!

        Args:
                directory:   	        Directory of the update environment.
                suppress_errors:   	    The flag for suppressing errors.
                verbose:   	            Verbosity flag about printing debug messages.
        """

        directory = os.path.normpath(directory)
        # see if the .devenv file even exists
        if os.path.isfile(directory + "/.devenv"):
            # it exists, so make sure a .gitignore exists and it includes .devenv
            if os.path.isfile(directory + "/.gitignore"):
                with open(directory + "/.gitignore", 'r') as gitignore:
                    for line in gitignore.readlines():
                        if ".devenv" in line:
                            self.__print(verbose, "Found valid development environment")
                            return True
            # raise error here
            self.__print(verbose, "'.devenv' found but not included in '.gitignore'.")
            if not suppress_errors:
                raise EnvironmentError("'.devenv' found but not included in '.gitignore'.")
        else:
            self.__print(verbose, "No '.devenv' file found in the root directory of the repo")

        return False

    def __get_file_conflicts(self, repo, verbose=False):
        """Method that takes in pointer to the repo and returns a list of files that have conflicts with the remote repo.

        Args:
                repo:   	            git.repo.base.Repo object.
                verbose:   	            Verbosity flag about printing debug messages.
        """

        assert type(repo) is git.repo.base.Repo, "Passed in repo needs to be of type 'git.repo.base.Repo'"
        diff = str(repo.git.diff("--name-only", "--diff-filter=U")).splitlines()
        if len(diff) == 0:
            self.__print(verbose, "No diff conflicts found")
        else:
            msg = "Found {} conflicts in files:".format(len(diff))
            for conflict in diff:
                msg += "\n  {}".format(conflict)
            self.__print(verbose, msg)
        return diff

    def __get_file_diffs(self, repo, verbose=False):
        """Method that takes in a pointer to the repo and returns a list of files that contain changes between the remote and local repo.

        Args:
                repo:   	            git.repo.base.Repo object.
                verbose:   	            Verbosity flag about printing debug messages.
        """

        assert type(repo) is git.repo.base.Repo, "Passed in repo needs to be of type 'git.repo.base.Repo'"
        diff = str(repo.git.diff("--name-only")).splitlines()
        if len(diff) == 0:
            self.__print(verbose, "No diff found")
        else:
            msg = "Found {} diffs in files:".format(len(diff))
            for conflict in diff:
                msg += "\n  {}".format(conflict)
            self.__print(verbose, msg)
        return diff


class Installer:
    """Class to define an installer of tracking system itself.

    This class provides necessary initiations and functions named :func:`t_system.updation.Installer.install`
    as the install point for the changed install scripts and named :func:`t_system.updation.Installer.__get_hash_of`
    for creating SHA-256 hash of the given file.
    """

    def __init__(self, editable, verbose):
        """Initialization method of :class:`t_system.updation.Installer` class.

        Args:
            editable:   	        Editable updation mode flag.
            verbose:   	            Verbosity flag about printing debug messages.
        """
        self.editable = editable
        self.verbose = verbose

        self.install_dev_sh = f'{T_SYSTEM_PATH}/../install-dev.sh'
        self.install_sh = f'{T_SYSTEM_PATH}/../install.sh'

        if self.editable:
            self.last_hash = self.__get_hash_of(self.install_dev_sh)
        else:
            self.last_hash = self.__get_hash_of(self.install_sh)

    def install(self):
        """Method to install the dependencies after git updation. It creates the sha-256 hash of the changed install scripts.
        Then compares them with the scripts those has hash when the Installer instance generates. If there is a difference between old and new install scripts, starts reinstallation.
        otherwise, terminates.
        """

        if self.editable:
            current_hash = self.__get_hash_of(self.install_dev_sh)
            if current_hash == self.last_hash:
                return

            install_sh = self.install_dev_sh
        else:
            current_hash = self.__get_hash_of(self.install_sh)
            if current_hash == self.last_hash:
                return

            install_sh = self.install_sh

        elevate(show_console=False, graphical=False)
        subprocess.call(install_sh, shell=True)

    @staticmethod
    def __get_hash_of(filename):
        """Method to send SHA-256 hash of the given file.

        Args:
                filename:   	        Name of the file that will hashed with sha-256.
        """
        # make a hash object
        h = hashlib.sha256()
        # open file for reading in binary mode
        with open(filename, 'rb') as file:
            # loop till the end of the file
            chunk = 0
            while chunk != b'':
                # read only 1024 bytes at a time
                chunk = file.read(1024)
                h.update(chunk)
        # return the hex representation of digest
        return h.hexdigest()
