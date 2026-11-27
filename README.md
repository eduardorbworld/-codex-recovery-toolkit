# Codex Recovery Toolkit

**Diagnose. Backup. Recover.**

Experimental, independent Windows utility for the ChatGPT/Codex startup error `attempt to write a readonly database`. Not affiliated with OpenAI.

## Quick start

Requires Python 3.11+ (standard library only). Download the source, extract it and open PowerShell in the extracted directory.

1. Close all ChatGPT and Codex processes.
2. Run `python recovery.py` to inspect free space and journal presence.
3. Choose an existing private backup directory on a drive with enough free space.
4. Run `python recovery.py --backup-dir D:\ --closed` to back up and check an isolated copy.
5. If successful, run `python recovery.py --backup-dir D:\ --closed --apply` to attempt recovery on the original.
6. Restart the application.

GUI: `python gui.py`. Select the database and backup destination when prompted.

The default target is `%USERPROFILE%\.codex\.codex-global-state.sqlite`. This tool checks backup hashes, tests a separate copy, and never intentionally deletes original files. SQLite may alter journals during recovery. Close all related processes; the tool cannot guarantee exclusive access. It does not fix disk space, ACLs or structural corruption automatically. Keep private backups; never publish them.

## Português

Ferramenta experimental e independente para Windows. Feche ChatGPT e Codex, libere espaço em disco e escolha uma pasta privada de backup. Execute `python recovery.py` para diagnóstico ou `python gui.py` para a interface gráfica. A opção de testar a cópia preserva o original; a recuperação original exige confirmação e backup verificado. Não há garantia de recuperação. Não publique bancos, logs ou credenciais.

## Development

Run `python -m unittest discover -s tests -v`. Tests use synthetic databases. See [case study](docs/case-study.md) and [security](SECURITY.md).

Status: initial experimental source release; Windows GUI and automated recovery require validation before production use.
