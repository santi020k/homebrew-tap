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
