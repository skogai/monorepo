#!/usr/bin/env python3
"""Local T3 picker. Database reads only; mutations go through the T3 CLI."""
import os
import sqlite3
import subprocess
import sys
from pathlib import Path


def clean(value):
    return ''.join(c if c.isprintable() else ' ' for c in str(value or ''))


def pick(header, options):
    # Ordinals distinguish duplicate titles without exposing IDs to the user.
    labels = {f'{i + 1}. {clean(label)}': value
              for i, (label, value) in enumerate(options)}
    result = subprocess.run(
        ['gum', 'filter', '--header', header, '--placeholder', 'Type to search…'],
        input='\n'.join(labels) + '\n', text=True, stdout=subprocess.PIPE)
    if result.returncode:
        return None
    return labels.get(result.stdout.strip())


def query(base, sql, args=()):
    uri = (base / 'userdata/statev2.sqlite').as_uri() + '?mode=ro'
    with sqlite3.connect(uri, uri=True) as db:
        db.row_factory = sqlite3.Row
        return db.execute(sql, args).fetchall()


def compose(base, target, action):
    result = subprocess.run(['gum', 'write', '--header',
        'Write your message · Enter submits · Ctrl+J newline · Ctrl+E editor'],
        text=True, stdout=subprocess.PIPE)
    if result.returncode or not result.stdout.strip():
        return
    if subprocess.run(['gum', 'confirm', 'Send this message to the agent?']).returncode:
        return
    subprocess.run(['t3', 'thread', action, '--base-dir', str(base), target, '-'],
                   input=result.stdout, text=True, check=True)


def browse_project(base, project):
    while True:
        threads = query(base, '''SELECT thread_id, title, archived_at
            FROM orchestration_v2_projection_threads
            WHERE project_id = ? AND deleted_at IS NULL
            ORDER BY updated_at DESC''', (project['project_id'],))
        options = [('Start a new thread', ('new', None))]
        options += [(f"{t['title']}" + (' [archived]' if t['archived_at'] else ''),
                     ('thread', t)) for t in threads]
        options.append(('Back to projects', ('back', None)))
        selected = pick(clean(project['title']) +
                        (' · No threads yet' if not threads else ' · Choose a thread'), options)
        if selected is None or selected[0] == 'back':
            return
        kind, thread = selected
        if kind == 'new':
            compose(base, project['project_id'], 'start')
            continue
        action = pick(clean(thread['title']), [('Read messages', 'read'),
                      ('Send a follow-up', 'send'), ('Back to threads', 'back')])
        if action == 'read':
            subprocess.run(['t3', 'thread', 'show', '--base-dir', str(base),
                            thread['thread_id'], '--messages', '20'], check=True)
            input('\nPress Enter to return to threads…')
        elif action == 'send':
            compose(base, thread['thread_id'], 'send')


def main():
    if not sys.stdin.isatty():
        raise RuntimeError('Open the picker in an interactive terminal.')
    base = Path(os.environ['T3CODE_HOME']).resolve()
    if not (base / 'userdata/statev2.sqlite').is_file():
        raise RuntimeError('Start the server with mise -E t3 run t3:serve, then run t3:init.')
    while True:
        projects = query(base, '''SELECT project_id, title, workspace_root
            FROM projection_projects WHERE deleted_at IS NULL ORDER BY title''')
        if not projects:
            print('No projects yet. Run mise -E t3 run t3:init to register this checkout.')
            return
        options = [(f"{p['title']} — {p['workspace_root']}", p) for p in projects]
        options.append(('Quit', None))
        project = pick('Local T3 · Choose a project', options)
        if project is None:
            return
        browse_project(base, project)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        pass
    except (RuntimeError, sqlite3.Error, OSError, subprocess.CalledProcessError) as exc:
        print(f'T3 picker: {exc}', file=sys.stderr)
        sys.exit(1)
