#!/bin/sh
VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Error: No version specified."
    echo "Usage: deploy-image.sh <version>"
    exit
fi

BUILD="docker build --no-cache --network=host -t kpiit-image:${VERSION} ."
echo "Building image: $BUILD"
$BUILD

TAG="docker tag kpiit-image:${VERSION} openshift-registry.web.cern.ch/it-cda-dr-kpis/kpiit-image:${VERSION}"
echo "Tagging image: $TAG"
$TAG

PUSH="docker push openshift-registry.web.cern.ch/it-cda-dr-kpis/kpiit-image"
echo "Pushing image to OpenShift: $PUSH"
$PUSH