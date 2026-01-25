# Installing as a Global Claude Code Skill

This guide shows how to install WeRead Exporter as a global skill that can be used from any directory.

## Prerequisites

1. Install Python dependencies:
```bash
pip3 install -e .
```

## Installation Methods

### Method 1: Install from Local Directory (Recommended)

```bash
# Install the skill globally
claude skill install .

# Or specify the skill.md file directly
claude skill install skill.md
```

### Method 2: Manual Installation

```bash
# Create the skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Copy the skill to the global skills directory
cp -r . ~/.claude/skills/weread-exporter

# Or just copy the skill.md file
cp skill.md ~/.claude/skills/weread-exporter.md
```

### Method 3: Symlink for Development

```bash
# Create the skills directory if it doesn't exist
mkdir -p ~/.claude/skills

# Create a symlink to the local directory
ln -s "$(pwd)" ~/.claude/skills/weread-exporter
```

## Verification

After installation, verify the skill is available:

```bash
claude skill list
```

You should see `weread-exporter` in the list.

## Usage

Once installed globally, you can use the skill from any directory:

```
Export the WeRead book 08232ac0720befa90825d88 to epub
```

Claude will automatically use the installed skill to export the book.

## Troubleshooting

### Skill not found

If the skill is not found:
1. Check if the skill is installed: `claude skill list`
2. Restart Claude Code
3. Check the installation path: `ls -la ~/.claude/skills/`

### Module not found error

If you get "Module not found" error:
```bash
# Make sure the package is installed in development mode
pip3 install -e .
```

### Permission errors

If you get permission errors:
```bash
# Use user install
pip3 install -e . --user
```

## Uninstallation

To remove the globally installed skill:

```bash
claude skill uninstall weread-exporter

# Or manually remove
rm -rf ~/.claude/skills/weread-exporter
rm -f ~/.claude/skills/weread-exporter.md
```
