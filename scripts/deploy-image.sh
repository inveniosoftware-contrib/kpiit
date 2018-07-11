#!/bin/sh
VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Error: No version specified."
    echo "Usage: deploy-image.sh <version>"
    exit
fi

# Ensure the user is authenticated with oc
who_ret=$(oc whoami)
if [ -z "$who_ret" ]; then
    echo "Error: Please login with oc login before running the script."
    exit 1
fi

# Login to Docker
docker_login_ret=`docker login -u openshift -p $(oc whoami -t) openshift-registry.web.cern.ch`
if [ "$docker_login_ret" != "Login Succeeded" ]; then
    echo "Error: Failed to login to Docker."
    exit 1
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