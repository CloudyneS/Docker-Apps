import os, requests, subprocess, urllib, tempfile, patoolib, wget, sys
from cprint.cprint import cprint as pr
from time import sleep
from git import Repo

def runCommand(command: str, expectedOutput: bytes = b'') -> bool:
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as cmd:
        cmd.wait()
        output = cmd.communicate()
        pr.info("Shell command: " + command)
        pr.info("Output: " + b','.join(output).decode('utf-8'))

        return expectedOutput in output[1] and cmd.returncode == 0

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
    command = f'rsync -a --info=progress2 {exclude} {source} {dest}'
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
    gitrepo = Repo.clone_from(LOC, path, progress=pr.info)
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


if __name__ == '__main__':
    envv = dict(os.environ)
    pr.info("Running initialization...")
    pr.info("Creating project")
    
    if not runCommand(
        'composer create-project roots/bedrock --no-dev --no-interaction /tmp/app', b'No security vulnerability advisories found'
    ):
        pr.err("Could not create project")
        exit(1)
    
    pr.ok("Project created, installing site")
    if envv.get('INSTALL_SITE', False):
        pr.info("Installing site from " + envv['INSTALL_SITE'])
        if not runCommand(
            f'cd /tmp/app && composer require {envv["INSTALL_SITE"]} --no-interaction', b'No security vulnerability advisories found'
        ):
            pr.err("Could not install site")
            exit(1)
        pr.info("Site installed")
    
    pr.ok("Site installed, importing content...")
    if envv.get('IMPORT_CONTENT', False):
        if not os.path.isfile('/app/web/app/imported.txt'):
            pr.info("Importing content from " + envv['IMPORT_CONTENT'])
            fromArchiveOrGit(envv["IMPORT_CONTENT"], "/tmp/app/web/app")
            with open('/tmp/app/web/app/imported.txt', 'w') as f:
                f.write('Yes')
            pr.info("Successfully imported data")

    pr.info("Moving all data except PV")
    syncFolders('/tmp/app/', '/app/', True, 'web/app')
    
    pr.ok("Moving data to persistent volume...")
    syncFolders('/tmp/app/web/app/', '/app/web/app/', True, ['uploads', 'plugins'])

    pr.ok("Setting permissions...")
    runCommand('chown -R nobody:root /app || true')

    pr.ok('Finished files, checking database...')
    if envv.get('IMPORT_DATABASE', False):
        if not runCommand('cd /app && wp --allow-root core is-installed', b''):
            pr.info('Database is not installed')
            pr.info('Retrieving from ' + envv['IMPORT_DATABASE'])
            sql_file = downloadFile(envv['IMPORT_DATABASE'], '/tmp')
            
            if not runCommand(f'cd /app && ls -al && wp --allow-root db import {sql_file} && mv {sql_file} /backup/current.sql', b'Success'):
                pr.err('Error importing database')
                runCommand(f'cp -f {sql_file} /backup/current.sql && cp -f {sql_file} /app/import.sql')
                exit(1)
    
    pr.ok("Finished database, setting theme...")
    if envv.get('SET_THEME', False):
        pr.info("Setting theme to " + envv['SET_THEME'])
        runCommand(f'cd /app && wp --allow-root theme activate {envv["SET_THEME"]}', b'')
    
    pr.ok("Success!")

