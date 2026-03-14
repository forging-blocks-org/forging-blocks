#!/bin/bash

# Script to create all labels for ForgingBlocks v1.0.0 Roadmap GitHub project

# Epic Labels
echo "Creating epic labels..."
gh label create "epic:1.1:messaging" --color "FF6B6B" --description "Epic 1.1: Message/Event System"
gh label create "epic:1.2:repository" --color "4ECDC4" --description "Epic 1.2: Repository Pattern"
gh label create "epic:1.3:application" --color "45B7D1" --description "Epic 1.3: Application Services"
gh label create "epic:1.4:infrastructure" --color "96CEB4" --description "Epic 1.4: Infrastructure Adapters"
gh label create "epic:2.1:cli" --color "FFEAA7" --description "Epic 2.1: CLI/Scaffolding Tools"
gh label create "epic:2.2:docs" --color "DDA0DD" --description "Epic 2.2: Enhanced Documentation"
gh label create "epic:2.3:ide" --color "98D8C8" --description "Epic 2.3: IDE Integration"
gh label create "epic:3.1:plugin-arch" --color "F7DC6F" --description "Epic 3.1: Plugin Architecture"
gh label create "epic:3.2:plugin-specs" --color "BB8FCE" --description "Epic 3.2: Plugin Specifications"
gh label create "epic:3.3:observability" --color "85C1E9" --description "Epic 3.3: Observability"
gh label create "epic:4.1:performance" --color "F8C471" --description "Epic 4.1: Performance Optimization"
gh label create "epic:4.2:testing" --color "82E0AA" --description "Epic 4.2: Testing Infrastructure"
gh label create "epic:4.3:resilience" --color "F1948A" --description "Epic 4.3: Error Handling & Resilience"
gh label create "epic:4.4:configuration" --color "85C1E9" --description "Epic 4.4: Configuration Management"
gh label create "epic:5.1:api-stability" --color "D2B4DE" --description "Epic 5.1: API Stability"
gh label create "epic:5.2:community" --color "AED6F1" --description "Epic 5.2: Community Adoption"
gh label create "epic:5.3:examples" --color "A3E4D7" --description "Epic 5.3: Example Applications"
gh label create "epic:5.4:plugin-ecosystem" --color "F9E79F" --description "Epic 5.4: Plugin Ecosystem Maturation"

# Phase Labels
echo "Creating phase labels..."
gh label create "phase:1:core-completeness" --color "E74C3C" --description "Phase 1: Core Completeness"
gh label create "phase:2:developer-experience" --color "F39C12" --description "Phase 2: Developer Experience"
gh label create "phase:3:plugin-ecosystem" --color "F1C40F" --description "Phase 3: Plugin Ecosystem"
gh label create "phase:4:production-readiness" --color "27AE60" --description "Phase 4: Production Readiness"
gh label create "phase:5:api-stabilization" --color "3498DB" --description "Phase 5: API Stabilization"
gh label create "phase:6:v1.0.0-release" --color "9B59B6" --description "Phase 6: v1.0.0 Release"

# Type Labels
echo "Creating type labels..."
gh label create "type:epic" --color "0052CC" --description "Epic issue"
gh label create "type:task" --color "0052CC" --description "Task issue"
gh label create "type:bug" --color "D73A49" --description "Bug issue"
gh label create "type:documentation" --color "0075CA" --description "Documentation issue"
gh label create "type:enhancement" --color "A2EEEF" --description "Enhancement issue"
gh label create "type:research" --color "D4EDDA" --description "Research issue"

# Priority Labels
echo "Creating priority labels..."
gh label create "priority:p0:critical" --color "B60205" --description "P0: Critical Path"
gh label create "priority:p1:high" --color "D73A49" --description "P1: High Priority"
gh label create "priority:p2:medium" --color "FBCA04" --description "P2: Medium Priority"
gh label create "priority:p3:low" --color "0E8A16" --description "P3: Low Priority"

echo "All labels created successfully!"
