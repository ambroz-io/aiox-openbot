"""Export a reviewed, explicit allowlist; never install or activate OpenBot."""
import argparse
import hashlib
import json
from pathlib import Path

ROLES = ('aiox-master', 'dev', 'qa', 'architect', 'analyst', 'pm', 'po',
         'sm', 'data-engineer', 'ux-design-expert', 'devops', 'squad-creator')
PREFIX = 'integrations/openbot/'
BASE = ('README.md', 'UPSTREAM.md', 'STORY.md', 'manifest.json', 'protocol.py',
        'schemas/delegation.json', 'workflows/story-development-cycle.md',
        'skills/aiox-openbot-team/SKILL.md',
        'skills/aiox-openbot-team/references/protocol.md',
        'tests/test_delegation_contract.py', 'tests/test_protocol.py',
        '261124-110000-exportar-pacote-openbot.py',
        '261124-110000-instalacao-portatil-openbot.md',
        'tests/261124-110000-testar-pacote-openbot.py')
ALLOWLIST = tuple(sorted(
    ['LICENSE', '.aiox-core/constitution.md']
    + ['.aiox-core/development/agents/' + role + '.md' for role in ROLES]
    + [PREFIX + name for name in BASE]
    + [PREFIX + 'agents/' + role + '.md' for role in ROLES]
    + [PREFIX + 'skills/aiox-openbot-team/references/roles/' + role + '.md'
       for role in ROLES]))
HASH_NAME = '261124-110000-manifesto-pacote-openbot.json'


def export(source, output):
    source = Path(source).resolve()
    output = Path(output).absolute()
    if output.exists() or output.is_symlink():
        raise ValueError('output must not exist')
    if output.resolve().is_relative_to(source):
        raise ValueError('output must be outside source checkout')
    payload = {}
    # Validate and snapshot every input before creating the destination.
    for name in ALLOWLIST:
        path = source / name
        if path.resolve() != path or not path.is_file():
            raise ValueError('missing or symlinked allowlist source: ' + name)
        payload[name] = path.read_bytes()
    hashes = {name: hashlib.sha256(data).hexdigest()
              for name, data in payload.items()}
    output.mkdir()  # exclusive; parent must already exist
    for name, data in payload.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
    with (output / HASH_NAME).open('x', encoding='utf-8') as stream:
        json.dump({'format_version': 1, 'sha256': hashes}, stream,
                  ensure_ascii=False, indent=2)
        stream.write('\n')
    return hashes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list', action='store_true', help='list exact paths; no writes')
    parser.add_argument('--output', type=Path, help='new directory outside checkout')
    args = parser.parse_args()
    if args.list:
        if args.output is not None:
            parser.error('--list and --output are mutually exclusive')
        print('\n'.join(ALLOWLIST))
        return
    if args.output is None:
        parser.error('--output is required unless --list is used')
    source = Path(__file__).resolve().parents[2]
    try:
        hashes = export(source, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, 'Export refused: ' + str(exc) + '\n')
    print('Exported ' + str(len(hashes)) + ' files plus SHA-256 manifest.')


if __name__ == '__main__':
    main()
