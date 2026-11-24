'use strict';

/**
 * Publish Safety Gate Tests (Story INS-4.10)
 *
 * Tests validate-publish.js behavior via source analysis and
 * behavioral verification with mocked filesystem/child_process.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SCRIPT_PATH = path.join(__dirname, '..', '..', 'bin', 'utils', 'validate-publish.js');

// The behavioral test shells out with a 330s pack timeout; keep Jest's outer budget higher.
jest.setTimeout(360000);

describe('Publish Safety Gate (Story INS-4.10 / PRO-13.5)', () => {
  let scriptSource;

  beforeAll(() => {
    scriptSource = fs.readFileSync(SCRIPT_PATH, 'utf8');
  });

  describe('PRO-13.5: Public tarball boundary', () => {
    test('script blocks pro/ paths in npm pack output', () => {
      expect(scriptSource).toContain('PRO_PATH_PATTERN');
      expect(scriptSource).toContain('Public package includes');
      expect(scriptSource).toContain('Public package excludes pro/ content');
    });

    test('legacy npm notice parser strips size prefixes before path checks', () => {
      expect(scriptSource).toContain('npm notice\\s+[\\d.]+[kMG]?B?\\s+(.+)');
    });

    test('script exits with code 1 on failure', () => {
      expect(scriptSource).toContain('process.exit(1)');
    });

    test('script exits with code 0 on success', () => {
      expect(scriptSource).toContain('process.exit(0)');
    });
  });

  describe('AC1: File count threshold', () => {
    test('minimum threshold is >= 50', () => {
      expect(scriptSource).toContain('MIN_FILE_COUNT = 50');
    });

    test('uses npm pack --dry-run for file counting', () => {
      expect(scriptSource).toContain('npm pack --dry-run');
    });

    test('error message includes file count on failure', () => {
      expect(scriptSource).toMatch(/Package has only.*files, expected >= /);
    });
  });

  describe('AC4: Standalone script design', () => {
    test('script has shebang for standalone execution', () => {
      expect(scriptSource.startsWith('#!/usr/bin/env node')).toBe(true);
    });

    test('script uses only Node.js builtins (fs, path, child_process)', () => {
      // Should not require any external packages
      const requires = scriptSource.match(/require\(['"]([^'"]+)['"]\)/g) || [];
      const modules = requires.map((r) => r.match(/require\(['"]([^'"]+)['"]\)/)[1]);
      const builtins = ['fs', 'path', 'child_process'];
      modules.forEach((mod) => {
        expect(builtins).toContain(mod);
      });
    });

    test('script resolves PROJECT_ROOT from __dirname', () => {
      expect(scriptSource).toContain("path.join(__dirname, '..', '..')");
    });
  });

  describe('AC3: CI integration', () => {
    test('npm-publish.yml includes publish safety gate step', () => {
      const workflowPath = path.join(
        __dirname,
        '..',
        '..',
        '.github',
        'workflows',
        'npm-publish.yml',
      );
      const workflow = fs.readFileSync(workflowPath, 'utf8');
      expect(workflow).toContain('Publish safety gate (INS-4.10)');
      expect(workflow).toContain('node bin/utils/validate-publish.js');
    });
  });

  describe('AC1/AC3: prepublishOnly wiring', () => {
    test('package.json prepublishOnly calls validate-publish.js first', () => {
      const pkgPath = path.join(__dirname, '..', '..', 'package.json');
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      expect(pkg.scripts.prepublishOnly).toMatch(/^node bin\/utils\/validate-publish\.js && /);
    });

    test('package.json has standalone validate:publish script', () => {
      const pkgPath = path.join(__dirname, '..', '..', 'package.json');
      const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
      expect(pkg.scripts['validate:publish']).toBe('node bin/utils/validate-publish.js');
    });
  });

  describe('AC5: Behavioral validation (real execution)', () => {
    test('script runs successfully and proves public package excludes pro/', () => {
      const result = execSync(`node "${SCRIPT_PATH}" 2>&1`, {
        encoding: 'utf8',
        cwd: path.join(__dirname, '..', '..'),
        timeout: 330000,
      });
      expect(result).toContain('PUBLISH SAFETY GATE: PASS');
      expect(result).toContain('PASS: Public package excludes pro/ content');
    });

    test('script produces human-readable output with pass/fail indicators', () => {
      expect(scriptSource).toContain('PASS:');
      expect(scriptSource).toContain('FAIL:');
      expect(scriptSource).toContain('PUBLISH SAFETY GATE: PASS');
      expect(scriptSource).toContain('PUBLISH SAFETY GATE: FAIL');
    });
  });
});


describe('pack output parsing regression', () => {
  let parse;
  beforeAll(() => {
    const source = fs.readFileSync(SCRIPT_PATH, 'utf8');
    const body = source.slice(source.indexOf('function parsePackedFiles('), source.indexOf('// Check 1/2:'));
    parse = require('vm').runInNewContext(body + '; parsePackedFiles');
  });
  const files = Array.from({ length: 50 }, (_, i) => ({ path: `bin/file-${i}.js` }));
  test.each(['HUSKY=0 skip install', '', '> prepare\n> husky\nhusky - install command is DEPRECATED\n', '[hook] preparing\n'])('reads package JSON after lifecycle prefix %p', (prefix) => {
    expect(Array.from(parse(prefix + JSON.stringify([{ files }], null, 2)))).toEqual(files.map(f => f.path));
  });
  test('retains pro paths for rejection even with lifecycle chatter', () => {
    expect(Array.from(parse('prepare hook\n' + JSON.stringify([{ files: [...files, { path: 'pro/private.js' }] }])))).toContain('pro/private.js');
  });
  test('malformed JSON cannot produce a successful package count', () => {
    expect(Array.from(parse('hook\n[{"files": ['))).toEqual([]);
  });
  test.each(['', 'HUSKY=0 skip install', '[hook] preparing\n'])('rejects truncated outer package array after %p', (prefix) => {
    expect(Array.from(parse(prefix + JSON.stringify([{ files }]).slice(0, -1)))).toEqual([]);
  });
  test.each(['', 'HUSKY=0 skip install', '[hook] preparing\n'])('does not salvage last object and lose pro path after %p', (prefix) => {
    const payload = JSON.stringify([{ files: [{ path: 'pro/private.js' }] }, { files }]).slice(0, -1);
    expect(Array.from(parse(prefix + payload))).toEqual([]);
  });
  test('retains pro path from a complete multi-package payload', () => {
    expect(Array.from(parse(JSON.stringify([{ files: [{ path: 'pro/private.js' }] }, { files }])))).toContain('pro/private.js');
  });
  test('supports a complete object payload', () => {
    expect(Array.from(parse(JSON.stringify({ files })))).toEqual(files.map(f => f.path));
  });
  test('does not fall back to notices when JSON is truncated', () => {
    expect(Array.from(parse('npm notice 1.2kB bin/safe.js\n' + JSON.stringify([{ files }]).slice(0, -1)))).toEqual([]);
  });
  test.each(['bin/[id].js', 'bin/{id}.js', 'pro/[id].js', 'pro/{id}.js'])('retains delimiters in legacy notice path %p', (filePath) => {
    expect(Array.from(parse(`npm notice 1.2kB ${filePath}`))).toEqual([filePath]);
    expect(Array.from(parse(`npm notice 1.2kB ${filePath}\r\n`))).toEqual([filePath]);
    expect(Array.from(parse(`[hook] npm notice 1.2kB ${filePath}`))).toEqual([filePath]);
  });
  test('ignores notice filename delimiters before a complete JSON payload', () => {
    const output = 'npm notice 1.2kB bin/[id].js\n' + JSON.stringify([{ files: [...files, { path: 'pro/private.js' }] }]);
    expect(Array.from(parse(output))).toContain('pro/private.js');
  });
  test.each(['bin/[id].js', 'bin/{id}.js'])('rejects truncated JSON even after misleading legacy record %p', (filePath) => {
    const output = `npm notice 1.2kB ${filePath}\n` + JSON.stringify([{ files: [{ path: 'pro/private.js' }] }, { files }]).slice(0, -1);
    expect(Array.from(parse(output))).toEqual([]);
  });
  test('does not remove notice-like text from inside a malformed JSON payload', () => {
    const output = '[\nnpm notice 1.2kB bin/[id].js\n' + JSON.stringify({ files }) + ']';
    expect(Array.from(parse(output))).toEqual([]);
  });
  test('keeps legacy npm notice support', () => {
    expect(Array.from(parse('npm notice 1.2kB pro/private.js'))).toEqual(['pro/private.js']);
  });
});
