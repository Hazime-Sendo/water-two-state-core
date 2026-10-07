#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Hazime Sendo
# Regenerate results/verification_results.json and results/verification_stdout.txt.
set -euo pipefail
cd "$(dirname "$0")/.."
python src/verify_model.py --out-dir results 2>/dev/null | tee results/verification_stdout.txt
