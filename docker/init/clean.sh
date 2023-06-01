#!/bin/bash
#
#

for i in xbook_nginx xbook xbook_mariadb xbook_redis xbook_client build-buildxbook-1;do echo $i;docker rm -f $i;done


docker network rm xbook

