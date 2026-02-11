#!/bin/bash
# setup_shell.sh - Shell environment setup for Hugo testing
# This script configures the environment and installs dependencies.
# Must be sourced: source /scripts/setup_shell.sh

set -e

cd /testbed

# Restore vendor.json if it was deleted
if [ ! -f "vendor/vendor.json" ]; then
    git checkout vendor/vendor.json 2>/dev/null || true
fi

# Export environment variables
export GOTOOLCHAIN=local
export GO111MODULE=auto

# Check if vendor directory is already populated
if [ ! -d "vendor/github.com/BurntSushi" ] || [ ! -f "go.mod" ]; then
    echo "Populating vendor directory from vendor.json..."

    # Create Python script to populate vendor
    python3 << 'PYEOF'
import json
import os
import subprocess
import sys

# Read vendor.json
with open('vendor/vendor.json') as f:
    vendor_data = json.load(f)

failed = []
for pkg in vendor_data['package']:
    path = pkg['path']
    revision = pkg['revision']

    # Skip if origin is set (vendored transitive dep)
    if 'origin' in pkg:
        continue

    # Create target directory
    target_dir = f"vendor/{path}"
    if os.path.exists(target_dir) and os.listdir(target_dir):
        continue  # Already populated

    os.makedirs(target_dir, exist_ok=True)

    # Clone into temp directory and checkout revision
    pkg_parts = path.split('/')
    if len(pkg_parts) >= 3:
        # Handle golang.org packages
        if pkg_parts[0] == 'golang.org' and pkg_parts[1] == 'x':
            repo_url = f"https://go.googlesource.com/{pkg_parts[2]}"
            subpath = '/'.join(pkg_parts[3:]) if len(pkg_parts) > 3 else ""
        else:
            repo_url = f"https://{'/'.join(pkg_parts[:3])}"
            subpath = '/'.join(pkg_parts[3:]) if len(pkg_parts) > 3 else ""

        temp_dir = f"/tmp/vendor_temp_{path.replace('/', '_')}"

        try:
            subprocess.run(['git', 'clone', '--quiet', repo_url, temp_dir],
                         check=True, capture_output=True, timeout=30)
            subprocess.run(['git', '-C', temp_dir, 'checkout', '--quiet', revision],
                         check=True, capture_output=True, timeout=10)

            source_path = os.path.join(temp_dir, subpath) if subpath else temp_dir

            # Copy files
            subprocess.run(['cp', '-r', f"{source_path}/.", target_dir], check=True)

            # Cleanup temp
            subprocess.run(['rm', '-rf', temp_dir], check=True)
        except Exception as e:
            failed.append(f"{path}: {e}")

# Clean .git directories from vendor
subprocess.run(['find', 'vendor', '-name', '.git', '-type', 'd', '-exec', 'rm', '-rf', '{}', '+'],
               capture_output=True)

if failed:
    print("Some packages failed to fetch (may already exist):", file=sys.stderr)
    for f in failed:
        print(f"  - {f}", file=sys.stderr)
PYEOF

    # Create minimal go.mod if it doesn't exist
    if [ ! -f "go.mod" ]; then
        cat > go.mod << 'EOF'
module github.com/spf13/hugo

go 1.16

require (
	github.com/BurntSushi/toml v0.3.1
	github.com/PuerkitoBio/purell v1.1.1
	github.com/PuerkitoBio/urlesc v0.0.0-20170810143723-de5bf2ad4578
	github.com/bep/gitmap v1.1.2
	github.com/bep/inflect v0.0.0-20160408190323-b896c45f5af9
	github.com/cpuguy83/go-md2man v1.0.10
	github.com/dchest/cssmin v0.0.0-20151210170030-fb8d9b44afdc
	github.com/eknkc/amber v0.0.0-20171010120322-cdade1c07385
	github.com/fortytw2/leaktest v1.3.0
	github.com/fsnotify/fsnotify v1.4.9
	github.com/gorilla/websocket v1.4.2
	github.com/hashicorp/hcl v1.0.0
	github.com/inconshreveable/mousetrap v1.0.0
	github.com/kardianos/osext v0.0.0-20190222173326-2bc1f35cddc0
	github.com/kr/fs v0.1.0
	github.com/kyokomi/emoji v2.2.4+incompatible
	github.com/magiconair/properties v1.8.1
	github.com/miekg/mmark v1.3.6
	github.com/mitchellh/mapstructure v1.4.1
	github.com/nicksnyder/go-i18n v1.10.1
	github.com/pelletier/go-buffruneio v0.3.0
	github.com/pelletier/go-toml v1.2.0
	github.com/pkg/errors v0.9.1
	github.com/pkg/sftp v1.11.0
	github.com/russross/blackfriday v1.6.0
	github.com/shurcooL/sanitized_anchor_name v1.0.0
	github.com/spf13/afero v1.6.0
	github.com/spf13/cast v1.3.1
	github.com/spf13/cobra v1.1.3
	github.com/spf13/fsync v0.9.0
	github.com/spf13/jwalterweatherman v1.1.0
	github.com/spf13/nitro v0.0.0-20131003134307-24d7ef30a12d
	github.com/spf13/pflag v1.0.5
	github.com/spf13/viper v1.7.1
	github.com/stretchr/testify v1.7.0
	github.com/yosssi/ace v0.0.5
	golang.org/x/crypto v0.0.0-20161221195553-f6b343c37ca8
	golang.org/x/net v0.0.0-20161216035930-45e771701b81
	golang.org/x/sys v0.0.0-20161214221506-d75a52659825
	golang.org/x/text v0.3.5
	gopkg.in/yaml.v2 v2.4.0
)
EOF
    fi

    # Create go.sum (empty or minimal is fine with vendor)
    touch go.sum

    # Create vendor/modules.txt to mark dependencies as explicit
    cat > vendor/modules.txt << 'MODEOF'
# github.com/BurntSushi/toml v0.3.1
## explicit
github.com/BurntSushi/toml
# github.com/PuerkitoBio/purell v1.1.1
## explicit
github.com/PuerkitoBio/purell
# github.com/PuerkitoBio/urlesc v0.0.0-20170810143723-de5bf2ad4578
## explicit
github.com/PuerkitoBio/urlesc
# github.com/bep/gitmap v1.1.2
## explicit
github.com/bep/gitmap
# github.com/bep/inflect v0.0.0-20160408190323-b896c45f5af9
## explicit
github.com/bep/inflect
# github.com/cpuguy83/go-md2man v1.0.10
## explicit
github.com/cpuguy83/go-md2man/md2man
# github.com/davecgh/go-spew v1.1.1
github.com/davecgh/go-spew/spew
# github.com/dchest/cssmin v0.0.0-20151210170030-fb8d9b44afdc
## explicit
github.com/dchest/cssmin
# github.com/eknkc/amber v0.0.0-20171010120322-cdade1c07385
## explicit
github.com/eknkc/amber
github.com/eknkc/amber/parser
# github.com/fortytw2/leaktest v1.3.0
## explicit
github.com/fortytw2/leaktest
# github.com/fsnotify/fsnotify v1.4.9
## explicit
github.com/fsnotify/fsnotify
# github.com/gorilla/websocket v1.4.2
## explicit
github.com/gorilla/websocket
# github.com/hashicorp/hcl v1.0.0
## explicit
github.com/hashicorp/hcl
github.com/hashicorp/hcl/hcl/ast
github.com/hashicorp/hcl/hcl/parser
github.com/hashicorp/hcl/hcl/scanner
github.com/hashicorp/hcl/hcl/strconv
github.com/hashicorp/hcl/hcl/token
github.com/hashicorp/hcl/json/parser
github.com/hashicorp/hcl/json/scanner
github.com/hashicorp/hcl/json/token
# github.com/inconshreveable/mousetrap v1.0.0
## explicit
github.com/inconshreveable/mousetrap
# github.com/kardianos/osext v0.0.0-20190222173326-2bc1f35cddc0
## explicit
github.com/kardianos/osext
# github.com/kr/fs v0.1.0
## explicit
github.com/kr/fs
# github.com/kyokomi/emoji v2.2.4+incompatible
## explicit
github.com/kyokomi/emoji
# github.com/magiconair/properties v1.8.1
## explicit
github.com/magiconair/properties
# github.com/miekg/mmark v1.3.6
## explicit
github.com/miekg/mmark
# github.com/mitchellh/mapstructure v1.4.1
## explicit
github.com/mitchellh/mapstructure
# github.com/nicksnyder/go-i18n v1.10.1
## explicit
github.com/nicksnyder/go-i18n/i18n/bundle
github.com/nicksnyder/go-i18n/i18n/language
github.com/nicksnyder/go-i18n/i18n/translation
# github.com/pelletier/go-buffruneio v0.3.0
## explicit
github.com/pelletier/go-buffruneio
# github.com/pelletier/go-toml v1.2.0
## explicit
github.com/pelletier/go-toml
# github.com/pkg/errors v0.9.1
## explicit
github.com/pkg/errors
# github.com/pkg/sftp v1.11.0
## explicit
github.com/pkg/sftp
# github.com/pmezard/go-difflib v1.0.0
github.com/pmezard/go-difflib/difflib
# github.com/russross/blackfriday v1.6.0
## explicit
github.com/russross/blackfriday
# github.com/shurcooL/sanitized_anchor_name v1.0.0
## explicit
github.com/shurcooL/sanitized_anchor_name
# github.com/spf13/afero v1.6.0
## explicit
github.com/spf13/afero
github.com/spf13/afero/mem
# github.com/spf13/cast v1.3.1
## explicit
github.com/spf13/cast
# github.com/spf13/cobra v1.1.3
## explicit
github.com/spf13/cobra
github.com/spf13/cobra/doc
# github.com/spf13/fsync v0.9.0
## explicit
github.com/spf13/fsync
# github.com/spf13/jwalterweatherman v1.1.0
## explicit
github.com/spf13/jwalterweatherman
# github.com/spf13/nitro v0.0.0-20131003134307-24d7ef30a12d
## explicit
github.com/spf13/nitro
# github.com/spf13/pflag v1.0.5
## explicit
github.com/spf13/pflag
# github.com/spf13/viper v1.7.1
## explicit
github.com/spf13/viper
# github.com/stretchr/testify v1.7.0
## explicit
github.com/stretchr/testify/assert
github.com/stretchr/testify/require
# github.com/yosssi/ace v0.0.5
## explicit
github.com/yosssi/ace
# golang.org/x/crypto v0.0.0-20161221195553-f6b343c37ca8
## explicit
golang.org/x/crypto/curve25519
golang.org/x/crypto/ed25519
golang.org/x/crypto/ed25519/internal/edwards25519
golang.org/x/crypto/ssh
# golang.org/x/net v0.0.0-20161216035930-45e771701b81
## explicit
golang.org/x/net/idna
# golang.org/x/sys v0.0.0-20161214221506-d75a52659825
## explicit
golang.org/x/sys/unix
# golang.org/x/text v0.3.5
## explicit
golang.org/x/text/cases
golang.org/x/text/internal
golang.org/x/text/internal/tag
golang.org/x/text/language
golang.org/x/text/runes
golang.org/x/text/secure/bidirule
golang.org/x/text/secure/precis
golang.org/x/text/transform
golang.org/x/text/unicode/bidi
golang.org/x/text/unicode/norm
golang.org/x/text/width
# gopkg.in/yaml.v2 v2.4.0
## explicit
gopkg.in/yaml.v2
# gopkg.in/yaml.v3 v3.0.0-20200313102051-9f266ea9e77c
gopkg.in/yaml.v3
MODEOF

    echo "Vendor directory populated."
fi

echo "Hugo build environment ready."
