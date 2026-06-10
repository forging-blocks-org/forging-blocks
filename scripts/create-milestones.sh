#!/bin/bash

# Script to create all milestones for ForgingBlocks v1.0.0 Roadmap GitHub project

# Calculate dates (assuming project starts today)
BASE_DATE="2026-01-28"

echo "Creating milestones..."

# Convert base date to seconds since epoch for date calculations
if command -v date >/dev/null 2>&1; then
    if date --version >/dev/null 2>&1; then
        # GNU date
        BASE_SECONDS=$(date -d "$BASE_DATE" +%s)
        MONTH=$((30 * 24 * 3600))

        # Helper function to add months
        add_months() {
            local months=$1
            local new_seconds=$((BASE_SECONDS + months * MONTH))
            date -d "@$new_seconds" +%Y-%m-%d
        }
    else
        # BSD date (macOS)
        add_months() {
            local months=$1
            date -j -v+${months}m -f "%Y-%m-%d" "$BASE_DATE" +%Y-%m-%d
        }
    fi
else
    # Fallback with hardcoded dates
    add_months() {
        case $1 in
            4) echo "2026-05-28" ;;
            7) echo "2026-08-28" ;;
            9) echo "2026-10-28" ;;
            11) echo "2026-12-28" ;;
            13) echo "2027-02-28" ;;
            15) echo "2027-04-28" ;;
            16) echo "2027-05-28" ;;
            17) echo "2027-06-28" ;;
            17.5) echo "2027-07-14" ;;
            18) echo "2027-07-28" ;;
            *) echo "2026-12-31" ;;
        esac
    }
fi

# Create milestones
gh milestone create "v0.4.0 - Core Completeness" \
    --due-date "$(add_months 4)" \
    --description "Complete foundational building blocks"

gh milestone create "v0.5.0 - Developer Experience" \
    --due-date "$(add_months 7)" \
    --description "Enhanced productivity and adoption tools"

gh milestone create "v0.6.0 - Plugin Ecosystem Foundation" \
    --due-date "$(add_months 9)" \
    --description "Plugin architecture and specifications"

gh milestone create "v0.7.0 - Performance & Testing" \
    --due-date "$(add_months 11)" \
    --description "Production performance and testing infrastructure"

gh milestone create "v0.8.0 - Resilience & Configuration" \
    --due-date "$(add_months 13)" \
    --description "Error handling and configuration management"

gh milestone create "v0.9.0 - Pre-Production Polish" \
    --due-date "$(add_months 15)" \
    --description "Final production readiness features"

gh milestone create "v0.10.0 - API Freeze" \
    --due-date "$(add_months 16)" \
    --description "API stabilization and documentation"

gh milestone create "v0.11.0 - Community Validation" \
    --due-date "$(add_months 17)" \
    --description "Real-world testing and feedback"

gh milestone create "v0.12.0 - Release Candidate" \
    --due-date "2027-07-14" \
    --description "Final preparation for v1.0.0"

gh milestone create "v1.0.0 - Production Release" \
    --due-date "$(add_months 18)" \
    --description "Stable, production-ready release"

echo "All milestones created successfully!"
