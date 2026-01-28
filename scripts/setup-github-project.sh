#!/bin/bash

# Master setup script for ForgingBlocks v1.0.0 Roadmap GitHub project
# Run this script after authenticating with GitHub CLI

set -e

echo "🚀 Setting up ForgingBlocks v1.0.0 Roadmap GitHub Project"
echo "============================================================"

# Check if gh CLI is authenticated
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ Please authenticate with GitHub CLI first:"
    echo "   gh auth login"
    exit 1
fi

echo "✅ GitHub CLI authenticated"

# Create the GitHub project
echo "📋 Creating GitHub project..."
gh project create "ForgingBlocks v1.0.0 Roadmap" \
    --body "Track progress from v0.3.10 to v1.0.0 production release" || {
    echo "⚠️  Project creation failed. It might already exist."
}

# Create labels
echo "🏷️  Creating repository labels..."
bash ./scripts/create-labels.sh || echo "⚠️  Some labels may already exist"

# Create milestones
echo "🎯 Creating milestones..."
bash ./scripts/create-milestones.sh || echo "⚠️  Some milestones may already exist"

echo ""
echo "✅ Basic project setup completed!"
echo ""
echo "📝 Next steps (to be done manually in GitHub web interface):"
echo "   1. Add custom fields to the project:"
echo "      - Phase (Single select): Phase 1-6 options"
echo "      - Epic (Single select): Epic 1.1-5.4 options"
echo "      - Priority (Single select): P0-P3 options"
echo "      - Effort (Number): 1-10 scale"
echo "      - Target Version (Single select): v0.4.0-v1.0.0"
echo ""
echo "   2. Create project views:"
echo "      - Roadmap Overview (Board view)"
echo "      - Current Sprint (Table view)"
echo "      - Epic Progress (Board view)"
echo "      - Phase Timeline (Table view)"
echo ""
echo "   3. Configure project automation rules"
echo ""
echo "🎊 Project foundation is ready!"
