# ForgingBlocks v1.0.0 Roadmap - GitHub Project Setup

This directory contains scripts and templates to set up the complete GitHub project for tracking the ForgingBlocks v1.0.0 roadmap.

## Quick Start

1. **Authenticate with GitHub CLI** (if not already done):
   ```bash
   gh auth login
   ```

2. **Run the master setup script**:
   ```bash
   cd /project
   ./scripts/setup-github-project.sh
   ```

## What Gets Created

### 🏷️ Repository Labels

#### Epic Labels (18 total)
- `epic:1.1:messaging` - Message/Event System
- `epic:1.2:repository` - Repository Pattern
- `epic:1.3:application` - Application Services
- `epic:1.4:infrastructure` - Infrastructure Adapters
- `epic:2.1:cli` - CLI/Scaffolding Tools
- `epic:2.2:docs` - Enhanced Documentation
- `epic:2.3:ide` - IDE Integration
- `epic:3.1:plugin-arch` - Plugin Architecture
- `epic:3.2:plugin-specs` - Plugin Specifications
- `epic:3.3:observability` - Observability
- `epic:4.1:performance` - Performance Optimization
- `epic:4.2:testing` - Testing Infrastructure
- `epic:4.3:resilience` - Error Handling & Resilience
- `epic:4.4:configuration` - Configuration Management
- `epic:5.1:api-stability` - API Stability
- `epic:5.2:community` - Community Adoption
- `epic:5.3:examples` - Example Applications
- `epic:5.4:plugin-ecosystem` - Plugin Ecosystem Maturation

#### Phase Labels (6 total)
- `phase:1:core-completeness`
- `phase:2:developer-experience`
- `phase:3:plugin-ecosystem`
- `phase:4:production-readiness`
- `phase:5:api-stabilization`
- `phase:6:v1.0.0-release`

#### Type Labels (6 total)
- `type:epic`, `type:task`, `type:bug`, `type:documentation`, `type:enhancement`, `type:research`

#### Priority Labels (4 total)
- `priority:p0:critical`, `priority:p1:high`, `priority:p2:medium`, `priority:p3:low`

### 🎯 Milestones (10 total)

1. **v0.4.0 - Core Completeness** (4 months)
2. **v0.5.0 - Developer Experience** (7 months)
3. **v0.6.0 - Plugin Ecosystem Foundation** (9 months)
4. **v0.7.0 - Performance & Testing** (11 months)
5. **v0.8.0 - Resilience & Configuration** (13 months)
6. **v0.9.0 - Pre-Production Polish** (15 months)
7. **v0.10.0 - API Freeze** (16 months)
8. **v0.11.0 - Community Validation** (17 months)
9. **v0.12.0 - Release Candidate** (17.5 months)
10. **v1.0.0 - Production Release** (18 months)

### 📋 GitHub Project

- **Name**: "ForgingBlocks v1.0.0 Roadmap"
- **Description**: "Track progress from v0.3.10 to v1.0.0 production release"

### 📝 Issue Templates

- **Epic Template** (`.github/ISSUE_TEMPLATE/epic.md`)
- **Task Template** (`.github/ISSUE_TEMPLATE/task.md`)

## Manual Configuration Required

After running the scripts, you'll need to configure the following in the GitHub web interface:

### 1. Add Custom Fields to Project

In the GitHub project settings, add these custom fields:

1. **Phase** (Single select):
   - Phase 1: Core Completeness (v0.4.0)
   - Phase 2: Developer Experience (v0.5.0)
   - Phase 3: Plugin Ecosystem (v0.6.0)
   - Phase 4: Production Readiness (v0.7.0-v0.9.x)
   - Phase 5: API Stabilization (v0.10.0-v0.12.x)
   - Final: v1.0.0 Release

2. **Epic** (Single select):
   - All 18 epic options (1.1-5.4)

3. **Priority** (Single select):
   - P0: Critical Path, P1: High Priority, P2: Medium Priority, P3: Low Priority

4. **Effort** (Number):
   - 1-10 scale for estimated days

5. **Target Version** (Single select):
   - v0.4.0 through v1.0.0

### 2. Create Project Views

Configure these views in the project:

1. **Roadmap Overview** (Board view)
   - Columns: Backlog, Sprint Ready, In Progress, In Review, Done
   - Group by Phase

2. **Current Sprint** (Table view)
   - Columns: Title, Assignee, Epic, Priority, Effort, Status
   - Filter: Status = "Sprint Ready" OR "In Progress"

3. **Epic Progress** (Board view)
   - Group by Epic
   - Show completion percentage

4. **Phase Timeline** (Table view)
   - Columns: Title, Phase, Target Version, Priority, Status, Assignee
   - Sort: Phase, then Priority

### 3. Configure Automation

Set up these automation rules:

1. **Sprint Planning**:
   - Auto-move to "Sprint Ready" when dependencies complete
   - Auto-assign milestones based on target version

2. **Progress Tracking**:
   - Auto-move to "In Progress" when PR created
   - Auto-move to "In Review" when PR ready for review
   - Auto-move to "Done" when PR merged

3. **Epic Management**:
   - Auto-close epic when all tasks complete
   - Auto-update phase progress

## Individual Scripts

You can also run individual scripts:

```bash
# Create only labels
./scripts/create-labels.sh

# Create only milestones
./scripts/create-milestones.sh
```

## Troubleshooting

### Authentication Issues
```bash
# Check authentication status
gh auth status

# Re-authenticate if needed
gh auth logout
gh auth login
```

### Project Already Exists
If the project already exists, the script will continue with labels and milestones creation.

### Permission Issues
Make sure you have admin access to the repository and organization (if applicable).

## Next Steps

1. Run the setup script
2. Configure custom fields and views manually
3. Create epic issues using the epic template
4. Break down epics into tasks using the task template
5. Start tracking progress!

For detailed implementation guidance, refer to the main `GITHUB_PROJECT_SETUP.md` file.
