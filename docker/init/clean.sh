#!/bin/bash
#
#

for i in nginx xbook mariadb redis xbook_client build-buildxbook-1;do echo $i;docker rm -f $i;done


docker network rm xbook

