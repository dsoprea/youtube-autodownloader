#!/bin/sh

export GAA_GOOGLE_API_AUTHORIZATION_REPO_PATH=/tmp/google_api_authorizations

# rm -f "${GAA_GOOGLE_API_AUTHORIZATION_REPO_PATH}"

nosetests -s -v $*
