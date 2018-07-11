docker login -u openshift -p $(oc whoami -t) openshift-registry.web.cern.ch
docker tag python:3.6 openshift-registry.web.cern.ch/it-cda-dr-kpis/python
docker push openshift-registry.web.cern.ch/it-cda-dr-kpis/python



docker build --no-cache --network=host -t kpiit-image:v0.1 .
docker tag kpiit-image:v0.1 openshift-registry.web.cern.ch/it-cda-dr-kpis/kpiit-image:v0.1
docker push openshift-registry.web.cern.ch/it-cda-dr-kpis/kpiit-image


# TODO: Make it work on CentOS
oc new-build https://github.com/equadon/kpiit#deploy-test