#!/bin/bash
# $Id: build.sh,v 1.1 2014/06/18 19:20:11 bob Exp $
PKG=ggpiod
VERSION=$(grep ^Version: ${PKG} | awk '{print $2}')
ARCH=$(grep ^Architecture: ${PKG} | awk '{print $2}')
DEBPKG=${PKG}_${VERSION}_${ARCH}.deb

echo "Building package ${PKG} version ${VERSION}"
equivs-build ${PKG}
if [[ $? -ne 0 ]]; then
	exit 1
fi

echo -n "Check using Lintian y/n: "
read ans
if [[ ${ans} == 'y' ]]; then
	echo "Checking package ${DEBPKG} with lintian"
	lintian ${DEBPKG}
	if [[ $? = 0 ]]
	then
	    dpkg -c ${DEBPKG}
	    echo "Package ${DEBPKG} OK"
	else
	    echo "Package ${DEBPKG} has errors"
	fi
fi

# End of build script
