#!/bin/bash
set -e

# Configuration
ORG="logic-star-ai"
BENCHMARK_NAME="codetaste"
CSV_FILE="instances.csv"
DRY_RUN=${DRY_RUN:-true}

# --- NEW: VERSIONING ---
VERSION=${VERSION:-"v1.0.0"} 

# This is the exact repo the packages will be linked to
REPO_URL="https://github.com/logic-star-ai/codetaste"

echo "-------------------------------------------------------"
echo "🚀 Logic-Star-AI Benchmark Publisher"
echo "Version: $VERSION"
echo "Mode: $( [ "$DRY_RUN" = "true" ] && echo 'DRY RUN' || echo 'LIVE' )"
echo "Target Repo Link: $REPO_URL"
echo "-------------------------------------------------------"

# Helper function to inject the label and build the primary versioned image
apply_label_and_build() {
    local local_img=$1
    local target_img=$2
    
    local target_annotation
    target_annotation=$(podman inspect --format '{{if .Annotations}}{{index .Annotations "org.opencontainers.image.source"}}{{end}}' "$target_img" 2>/dev/null || true)

    if [ "$target_annotation" == "$REPO_URL" ]; then
        echo "  ⚡ Target image already has the OCI annotation. Skipping build."
        return 0
    fi

    # Edge case: Check if the local image already has the annotation too
    local local_annotation
    local_annotation=$(podman inspect --format '{{if .Annotations}}{{index .Annotations "org.opencontainers.image.source"}}{{end}}' "$local_img" 2>/dev/null || true)

    if [ "$local_annotation" == "$REPO_URL" ]; then
        echo "  ⚡ Local image already has the OCI annotation. Tagging instead of building."
        podman tag "$local_img" "$target_img"
        return 0
    fi

    echo "  🏗️ Building new layer to inject OCI annotation and label..."
    podman build \
        --no-cache \
        --annotation "org.opencontainers.image.source=$REPO_URL" \
        --label "org.opencontainers.image.source=$REPO_URL" \
        -t "$target_img" - <<EOF
FROM $local_img
EOF
}

# 1. Base Image
BASE_LOCAL="localhost/benchmark/benchmark-base-all:latest"
REMOTE_BASE_VER="ghcr.io/$ORG/$BENCHMARK_NAME/benchmark-base-all:$VERSION"
REMOTE_BASE_LATEST="ghcr.io/$ORG/$BENCHMARK_NAME/benchmark-base-all:latest"

echo "STEP 1: Handling Base Image..."
if [ "$DRY_RUN" = "false" ]; then
    # 1. Build the new labeled layer and tag with VERSION
    apply_label_and_build "$BASE_LOCAL" "$REMOTE_BASE_VER"
    # 2. Tag that new labeled image with LATEST
    podman tag "$REMOTE_BASE_VER" "$REMOTE_BASE_LATEST"
    
    # 3. Push both
    podman push --format oci "$REMOTE_BASE_VER"
    podman push --format oci "$REMOTE_BASE_LATEST"
else
    echo "[DRY RUN] Would inject label into $BASE_LOCAL -> $REMOTE_BASE_VER"
    echo "[DRY RUN] Would tag $REMOTE_BASE_VER -> $REMOTE_BASE_LATEST"
    echo "[DRY RUN] Would push both tags."
fi

# 2. Helper function to process images
process_images() {
    local suffix=$1
    echo "STEP 2 ($suffix): Processing benchmark instances..."

    while IFS=',' read -u 3 -r owner repo commit_hash rest || [ -n "$owner" ]; do
        OWNER_LOWER=$(echo "$owner" | tr '[:upper:]' '[:lower:]')
        REPO_LOWER=$(echo "$repo" | tr '[:upper:]' '[:lower:]')
        short_hash=${commit_hash:0:8}
        echo "DEBUG: Read line for $owner / $repo"
        # Define image names
        LOCAL_IMG="localhost/benchmark/${OWNER_LOWER}__${REPO_LOWER}-${short_hash}__${suffix}:latest"
        REMOTE_IMG_VER="ghcr.io/${ORG}/${BENCHMARK_NAME}/${OWNER_LOWER}__${REPO_LOWER}-${short_hash}__${suffix}:$VERSION"
        REMOTE_IMG_LATEST="ghcr.io/${ORG}/${BENCHMARK_NAME}/${OWNER_LOWER}__${REPO_LOWER}-${short_hash}__${suffix}:latest"

        echo "--- Processing: $OWNER_LOWER/$REPO_LOWER ($suffix) ---"
        
        if [ "$DRY_RUN" = "true" ]; then
            echo "[DRY RUN] Would inject label: $LOCAL_IMG -> $REMOTE_IMG_VER"
            echo "[DRY RUN] Would tag latest: $REMOTE_IMG_VER -> $REMOTE_IMG_LATEST"
            echo "[DRY RUN] Would push both tags."
        else
            if podman image exists "$LOCAL_IMG"; then
                # Build versioned image with the public repo label
                apply_label_and_build "$LOCAL_IMG" "$REMOTE_IMG_VER"
                
                # Tag the newly labeled image as latest
                podman tag "$REMOTE_IMG_VER" "$REMOTE_IMG_LATEST"
                
                # Push both
                podman push --format oci "$REMOTE_IMG_VER"
                podman push --format oci "$REMOTE_IMG_LATEST"
            else
                echo "❌ Error: Local image $LOCAL_IMG not found. Aborting."
                exit 1
            fi
        fi
    done 3< <(tail -n +2 "$CSV_FILE")
}

# Run for both setup and runtime
process_images "setup"
process_images "runtime"

echo "-------------------------------------------------------"
echo "✅ Done! Published version $VERSION linked to codetaste"