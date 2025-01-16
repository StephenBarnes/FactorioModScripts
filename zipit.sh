#!/bin/bash

find . -maxdepth 1 -name "*.zip" -type f -delete

folder=$1

# Check thumbnail
if [ ! -f "$folder/thumbnail.png" ]; then
  echo "WARNING: $folder missing thumbnail.png"
fi

# Check changelog
if [ ! -f "$folder/changelog.txt" ]; then
  echo "WARNING: $folder missing changelog.txt"
fi

# Grab version from info.json
version=$(grep -oP '"version"\s*:\s*"\K[^"]*' "$folder/info.json")
if [ -z "$version" ]; then
  echo "No version found in info.json"
  exit 1
fi

# Check first Version line in changelog
first_version_line=$(grep -m1 '^Version:' "$folder/changelog.txt")
if [ -z "$first_version_line" ]; then
  echo "WARNING: No 'Version:' line in changelog"
else
  changelog_version=$(echo "$first_version_line" | grep -oP '(?<=Version:\s).*')
  if [ "$changelog_version" != "$version" ]; then
    echo "Version mismatch: info.json has $version but changelog has $changelog_version"
    exit 1
  fi
fi

archive="${folder%/}_$version.zip"

echo "Zipping to $archive..."
zip -rq "$archive" "$folder" -x "*/.git*" -x "*/.vscode*" -x "*/notes*" -x "*/modportal*"

echo "Created $archive"
