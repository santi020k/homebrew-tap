# Santi020k Homebrew Tap

Homebrew formulae for Santi020k developer tools.

## Install Santi020k Terminal

```sh
brew install santi020k/tap/santi020k-terminal
santi020k-terminal install
```

The formula installs the Santi020k terminal CLI, terminal color presets,
Starship configurations, curated Zsh setup, and their Homebrew dependencies.

## Install Coolstead

```sh
brew install --cask santi020k/tap/coolstead
```

Coolstead is a signed and notarized macOS thermal monitor and conservative fan
controller. Its cask uses the immutable, versioned DMG and exact SHA-256 digest
published in
[santi020k/coolstead-releases](https://github.com/santi020k/coolstead-releases).

## Upgrade

```sh
brew update
brew upgrade santi020k-terminal
brew upgrade --cask coolstead
santi020k-terminal update
```

## Development

Terminal product source, tests, and release archives live in
[santi020k/santi020k-theme](https://github.com/santi020k/santi020k-theme).
Coolstead source and release automation are maintained separately, while its
public binaries live in
[santi020k/coolstead-releases](https://github.com/santi020k/coolstead-releases).
This repository contains only Homebrew packaging metadata.

`Formula/santi020k-terminal.rb` and `Casks/coolstead.rb` are generated and
updated by their product release workflows. Do not duplicate product source in
this repository. Before proposing manual packaging changes, run `brew style`
and the relevant strict `brew audit` command.

## Security

Do not install a package whose downloaded archive does not match the formula or
cask SHA-256. Report suspected package-source, checksum, or update-channel
vulnerabilities through GitHub's private vulnerability reporting instead of a
public issue.

## Quality v2 validation

This tap is unversioned: tooling changes target `main` through the normal pull
request workflow, not a new application release. Quality is pinned to 2.0.0 in
`.quality-version`; the installer uses its immutable release revision.

Run `python3 -m unittest discover -s scripts -p 'test_*.py'` and
`python3 scripts/check_tap.py` locally, or run `quality check` with Quality 2.
Run `python3 scripts/quality_impact_test.py` with Quality 2 on `PATH` to exercise
the committed shadow policy.
The checks compile Ruby syntax without evaluating packaging code and enforce a
literal SHA-256 plus a matching, versioned Santiago-owned GitHub release asset
URL. They do not download archives, install software, verify notarization, or
replace the strict Homebrew audits required for packaging changes.

Pull requests validate only changed existing formula/cask files. Renames,
deletions, shared tooling, unknown inputs and missing history broaden to all
remaining packaging sources. README/license-only changes still run regression
fixtures. Pushes to main and manual validation always run the full tap check.
Independent files are checked with at most two concurrent Ruby processes; no
persistent cache can hide changed checksums or upstream metadata.

Quality's conservative impact graph records shadow plans alongside these
checks; it does not execute the graph or bypass the full publication gates.
The stable aggregate fails if either validation or planning fails, is cancelled,
or is skipped. Superseded validation is cancelled. Product release automation
continues to generate formulae and casks; this change publishes nothing.
To recover, revert the tooling change and rerun full packaging checks without
changing published asset identities or formula/cask versions.

### Commit hooks

The existing Quality-managed `commit-msg` hook delegates to
[`@santi020k/commitprompt`](https://www.npmjs.com/package/@santi020k/commitprompt)
1.1.0, using its standard Conventional Commit rules. Contributors who commit need
Node.js 22.18 or newer and `commitprompt` on `PATH` (for example,
`npm install --global @santi020k/commitprompt@1.1.0`); an existing installation is
sufficient. This is a developer CLI prerequisite, not an application dependency
or a new package-manager stack for the tap. The `pre-push` hook runs the complete
`quality check` gate. Missing tools and invalid commit messages fail explicitly;
never bypass the hooks. Ruby/Python validation itself does not require Node.js.
