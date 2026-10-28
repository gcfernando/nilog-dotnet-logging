"""Check repository metadata without importing or executing application code."""

from pathlib import Path
import re
import sys

REQUIRED = (
    'README.md', 'documentation.md', 'CONTRIBUTING.md', 'SECURITY.md',
    'REPOSITORY_STANDARDS.md', '.editorconfig', '.gitattributes', '.gitignore',
    '.github/ISSUE_TEMPLATE/config.yml', '.github/ISSUE_TEMPLATE/bug-report.yml',
    '.github/pull_request_template.md', '.github/dependabot.yml',
    '.github/workflows/repository-standards.yml', '.github/scripts/check_repository.py',
)


def prose_lines(text):
    """Ignore fenced examples so code comments are not treated as headings."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        match = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not line[match.end():].strip():
                fence = None
            continue
        if fence is None:
            yield number, line


def check(root):
    root = Path(root).resolve()
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f'{name}: required file is missing')
    if not any(p.name == 'README.md' for p in root.iterdir()):
        errors.append('README.md: filename must use this exact case')

    # Deliberately limited to root documentation and repository administration.
    # Existing application, generated, imported and vendored files are not linted.
    paths = {p for p in root.glob('*.md') if p.is_file()}
    paths.update(root / name for name in ('.editorconfig', '.gitattributes', '.gitignore', '_config.yml'))
    github = root / '.github'
    if github.exists():
        paths.update(p for p in github.rglob('*') if p.is_file() and p.suffix in ('.md', '.yml', '.yaml', '.py')
                     and 'legacy-workflows' not in p.relative_to(github).parts)
    for path in sorted(paths):
        if not path.is_file():
            continue
        name = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            errors.append(f'{name}: expected UTF-8')
            continue
        if text.startswith('\ufeff'):
            errors.append(f'{name}: remove the UTF-8 byte order mark')
        if b'\r' in raw:
            errors.append(f'{name}: expected LF line endings')
        if raw and not raw.endswith(b'\n'):
            errors.append(f'{name}: missing final newline')
        if path.suffix == '.md':
            prose = list(prose_lines(text))
            if name in ('README.md', 'documentation.md', 'CONTRIBUTING.md', 'SECURITY.md', 'REPOSITORY_STANDARDS.md'):
                if sum(bool(re.match(r'^#\s+\S', line)) for _, line in prose) != 1:
                    errors.append(f'{name}: expected one level-one title outside code fences')
            for number, line in prose:
                trailing = line[len(line.rstrip(' \t')):]
                if trailing and (not line.strip() or trailing != '  '):
                    errors.append(f'{name}:{number}: trailing whitespace; use exactly two spaces for a Markdown hard break')
                if re.match(r'^#{1,6}\s+\S', line):
                    following = text.splitlines()[number:number + 1]
                    if following and following[0].strip():
                        errors.append(f'{name}:{number}: add a blank line after the heading')

    for path in sorted((github / 'workflows').glob('*.y*ml')):
        text = path.read_text(encoding='utf-8')
        name = path.relative_to(root).as_posix()
        if not re.search(r'^permissions:\n  contents: read\s*$', text, re.M):
            errors.append(f'{name}: default contents permission must be read; elevate individual jobs')
        for action in re.findall(r'^\s*(?:-\s+)?uses:\s*([^\s#]+)', text, re.M):
            if action.startswith('./'):
                continue
            if not re.fullmatch(r'[^@]+@[0-9a-f]{40}', action):
                errors.append(f'{name}: pin action to a full commit SHA: {action}')
        if '\njobs:\n' in '\n' + text:
            jobs = ('\n' + text).split('\njobs:\n', 1)[1]
            for match in re.finditer(r'^  ([\w-]+):\s*\n(.*?)(?=^  [\w-]+:|\Z)', jobs, re.M | re.S):
                job, body = match.groups()
                if re.search(r'^    runs-on:', body, re.M) and not re.search(r'^    timeout-minutes: [1-9][0-9]*\s*$', body, re.M):
                    errors.append(f'{name}: job {job} needs an explicit timeout')

    # Only administration paths are required links; project-specific link and
    # build checks remain in the existing toolchain described in CONTRIBUTING.
    for name in ('CONTRIBUTING.md', 'SECURITY.md', 'REPOSITORY_STANDARDS.md', '.github/pull_request_template.md'):
        path = root / name
        if not path.is_file():
            continue
        for url in re.findall(r'\]\(([^\s)]+)\)', path.read_text(encoding='utf-8')):
            if re.match(r'^(?:[a-zA-Z][\w+.-]*:|#|/)', url):
                continue
            target = (path.parent / url.split('#', 1)[0]).resolve()
            if not target.exists():
                errors.append(f'{name}: missing relative link {url}')
    return errors


def main():
    root = Path(__file__).resolve().parents[2]
    errors = check(root)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('PASS: repository structure, metadata formatting and workflow conventions')
    return 0


if __name__ == '__main__':
    sys.exit(main())
