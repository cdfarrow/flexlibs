# Future testing ideas

Notes for expanding beyond the current smoke tests now that Windows CI can
install FieldWorks, seed a sample project (Sena 2), and run the NuGet overlay.

## Current coverage

- `test_FLExInit` — initialize / cleanup
- `test_FLExProject` — list projects, open first project, walk headwords
- `test_CustomFields` — write/read a named entry custom field (skipped in CI;
  needs a fixture project with that field)

CI runs `make test-nuget -k "not CustomFields"` against the Sena 2 sample.

## Suggested next steps (priority order)

### 1. Project-shape read-only test

Promote the checks in `flexlibs/examples/demo_openproject.py` into pytest:

- parts of speech (non-empty list of strings)
- writing systems and default vernacular / analysis WS
- custom field discovery (entry / sense lists are iterable)
- lexicon entry count and text count are non-negative integers

Use the sample project (or `FLEXLIBS_TEST_PROJECT`). Fully CI-friendly; no writes.

### 2. Deeper lexicon field access

Extend beyond “headword is a string”. For the first N entries (or a few known
ones), call and type-check:

- lexeme / citation form
- sense gloss and POS
- semantic domains (may be empty)
- example text when present

Still read-only. Catches writing-system and LCM regressions that the headword
smoke test misses.

### 3. Write round-trip on a project copy

Do not mutate the cached Sena 2 tree in place. In CI:

1. Copy the project folder to a temp projects path
2. Open write-enabled
3. Set a gloss (or lexeme), read it back, clear it
4. Close and discard the copy

Exercises the real write path without requiring `__flexlibs_testing` /
`EntryFlags`. Keep `test_CustomFields` as an optional local fixture.

### 4. NuGet overlay load assertion

When `FLEXLIBS_ASSEMBLY_DIR` is set, assert that `SIL.LCModel` (and optionally
`SIL.Core`) loaded from a path under that directory. Turns “overlay actually
applied” into a failing test instead of a log-only check.

### 5. Optional matrices (later)

- Python 3.9 and 3.12
- Job without overlay (install DLLs only) vs with NuGet overlay
- Pinned LCM version vs floating `*-*` latest

Useful for separating “new SIL beta broke us” from “our wrapper is wrong.”

## Lower priority / skip for now

- Deep custom-field and list-field coverage in CI (fixture-heavy)
- Text corpus, reversal indexes, publications (interesting later, lower ROI)
- Mocking LCM — wrong layer; this library needs real interop tests

## Practical first PR

Implement (1), (2), and (4) together: still fully read-only on Sena 2, then
add (3) once that suite is stable.
