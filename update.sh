#!/usr/bin/env bash

if [ -n "$DEBUG" ]; then
	set -x
fi

set -o errexit
set -o nounset
set -o pipefail

copier -x template/** -x copier.yml -x *.py -x CHANGELOG.md \
  "$@" \
  -d generator=copier_python_base \
  -d nix=True \
  -d license=MIT \
  -d repo_url=https://your.repo.url.here \
  -d copyright_date=2023 \
  -a .generator.yml \
  update ./.
