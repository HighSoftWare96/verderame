#!/bin/bash
branch="$VERDERAME_BRANCH"

if [[ -z $branch ]]; then
  branch="main"
fi

echo "🐳 Pulling new modifications from branch $branch..."
git fetch -a
git checkout "$branch"
git pull

echo "🤖 Restarting service with new modifications..."
sudo systemctl restart verderamen.service
echo "✅ Service updated and restarted correctly!"

