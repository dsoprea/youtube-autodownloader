#!/bin/sh

export GAA_GOOGLE_API_AUTHORIZATION_FILEPATH=/tmp/.google_api_auth

rm -f "${GAA_GOOGLE_API_AUTHORIZATION_FILEPATH}"

nosetests -s -v $*
