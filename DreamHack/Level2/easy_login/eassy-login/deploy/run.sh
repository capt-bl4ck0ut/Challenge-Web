#!/bin/bash

export FLAG="test"
&>/dev/null /usr/sbin/apachectl -DFOREGROUND -k start