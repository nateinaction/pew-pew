#!/usr/bin/env bash

SVN_URL=${1}
VERSION=${2}
USERNAME=${3}
PASSWORD=${4}
SVN_DIR="${APP_DIR}/svn"

# Checkout the SVN repo
rm -rf ${SVN_DIR}
svn co -q "${SVN_URL}" ${SVN_DIR}

# Remove old trunk, sync and tag current trunk
rm -rf ${SVN_DIR}/trunk/
rsync -r . ${SVN_DIR}/trunk/
svn cp ${SVN_DIR}/trunk/ ${SVN_DIR}/tags/${VERSION}/

# Publish to SVN
svn ci --no-auth-cache --username ${USERNAME} --password ${PASSWORD} ${SVN_DIR} -m "Deploy version ${VERSION}"
