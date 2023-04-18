import os, subprocess, patoolib, wget, sys
from cprint.cprint import cprint as pr
from time import sleep
from git import Repo

def runCommand(command: str, expectedOutput: bytes = b'') -> bool:
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as cmd:
        cmd.wait()
        output = cmd.communicate()
        pr.info("Shell command: " + command)
        pr.info("Output: " + b','.join(output).decode('utf-8'))
        pr.info("End Output")
        return expectedOutput in b''.join(output) and cmd.returncode == 0

def downloadFile(url: str, folder: str) -> str:
    pr.info("Downloading file from " + url)
    path = wget.download(url, folder)
    pr.info("Downloaded file to " + path)
    return path

def syncFolders(source: str, dest: str, print: bool = False, exclude: str = None):
    if exclude is None:
        exclude = ''
    if isinstance(exclude, list):
        exclude = ' '.join([f" --exclude '{x}' " for x in exclude])
    else:
        exclude = f"--exclude '{exclude}'"
    command = f'rsync -ah --no-i-r --info=progress2 {exclude} {source} {dest} | rsyncy'
    if print:
        with subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=sys.stdout) as cmd:
            cmd.wait()
    else:
        with subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE) as cmd:
            cmd.wait()
            print(cmd.communicate())
    return cmd.returncode == 0    
     

def unpackFile(path: str, destination: str):
    pr.info("Unpacking file " + path)
    patoolib.extract_archive(
        archive=path,
        verbosity=1,
        outdir=destination,
        interactive=False   
    )
    pr.info("Unpacked file to " + destination)

def getFromGit(url: str, destination: str):
    pr.info("Cloning GIT repo...")

    LOC = url.replace('git://', 'https://')
    LOC = LOC.split('@@')
    BRANCH = None
    if len(LOC) > 1:
        BRANCH = LOC[1]
    
    LOC = LOC[0]
    pr.info("Cloning from: " + LOC)
    gitrepo = Repo.clone_from(LOC, destination, progress=pr.info)
    if BRANCH and gitrepo.active_branch.name != BRANCH:
        pr.info("Cloned, switching branch to " + BRANCH)
        gitrepo.git.checkout(BRANCH)

def fromArchiveOrGit(url, path):
    if url[0:4] == 'http':
        pr.info("Retrieving from archive...")
        archive_path = downloadFile(url, '/tmp')
        pr.info("Unpacking archive...")
        unpackFile(archive_path, path)
        return True
    if url[0:3] == 'git':
        pr.info("Retrieving from GIT...")
        getFromGit(url, path)
        return True
    raise Exception(f"Invalid URL {url}")

def isConsideredFalse(test):
    if isinstance(test, str):
        return test.lower() in ['false', 'no', 'n', 'f', '0']
    if isinstance(test, int):
        return test == 0
    return test == False

def isConsideredTrue(test):
    return not isConsideredFalse(test)

if __name__ == '__main__':
    envv = dict(os.environ)
    pr.info("Running initialization...")
    
    if isConsideredTrue(envv.get('RUN_COMPOSER', False)):
        # Always get newest version of roots/bedrock
        if not runCommand(
            'composer create-project roots/bedrock --no-dev --no-interaction --no-audit /tmp/app', b'Generating optimized autoload'
        ):
            pr.err("Could not create project")
            exit(1)
        
        # Download and install newest version of site
        pr.ok("Project created, installing site")
        if isConsideredTrue(envv.get('INSTALL_SITE', False)):
            pr.info("Installing site from " + envv['INSTALL_SITE'])
            if not runCommand(
                f'cd /tmp/app && composer require {envv["INSTALL_SITE"]} --no-interaction', b'Generating optimized autoload'
            ):
                pr.err("Could not install site")
                exit(1)
            pr.info("Site installed")
    
        # Update the PV with the new site
        pr.info("Moving all updated data to PV")
        syncFolders('/tmp/app/', '/app/', True)
    
    if isConsideredTrue(envv.get('RUN_IMPORTS', False)):
        pr.ok("Importing content...")

        if isConsideredTrue(envv.get('IMPORT_CONTENT', False)):
            pr.info("Importing content from " + envv['IMPORT_CONTENT'])
            fromArchiveOrGit(envv["IMPORT_CONTENT"], "/tmp/imports")
            pr.info("Successfully downloaded and extracted content, syncing to PV...")
            syncFolders("/tmp/imports/", "/app/web/app/", True, ['plugins', 'themes', 'mu-plugins'])
            pr.info("Successfully imported data")

    if isConsideredTrue(envv.get('RUN_DATABASEIMPORTS', False)):
        pr.ok("Importing database if not already installed...")
        sql_file = ""
        
        if not runCommand('cd /app && wp core is-installed', b''):
            pr.info("Database is not installed, retrieving and installing...")
            try:
                sql_file = downloadFile(envv['IMPORT_DATABASE'], '/tmp')
            except:
                pr.info("Could not download database, testing if it is a path ...")
                sql_file = envv['IMPORT_DATABASE']
        
        elif isConsideredTrue(envv.get('FORCE_IMPORT_DB', False)):
            pr.err("Database is already installed, but FORCE_IMPORT_DB is set so database will be replaced")
            sql_file = downloadFile(envv['IMPORT_DATABASE'], '/tmp')
            
            pr.err("Resetting database...")
            if not runCommand(
                'cd /app && wp db reset --yes', b''
            ):
                pr.err('Could not reset database, skipping import...')
                sql_file = ""

        if sql_file != "":
            if not runCommand(f'cd /app && wp db import {sql_file}', b'Success'):
                pr.err('Error importing database')
                exit(1)

    if isConsideredTrue(envv.get('SET_THEME', False)):
        pr.info("Ensuring that theme is set correctly...")
        
        if envv.get("FORCE_THEME_NAME", "") != "":
            runCommand(
                f'cd /app/web/app/themes && mv {envv["SET_THEME"]} {envv["FORCE_THEME_NAME"]} && wp theme activate {envv["FORCE_THEME_NAME"]}',
                b''
            )
        else:
            runCommand(
                f'cd /app && wp theme activate {envv["SET_THEME"]}', b''
            )

    # Always recreate the environment file
    runCommand( 'cd /app && wp dotenv salts generate --force', b'' )

    pr.ok("Successfully finished importing site!")

