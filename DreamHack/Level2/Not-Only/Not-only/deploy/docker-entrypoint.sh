#!/bin/bash
mongod & sleep 5 && cat /app/db.sql | mongo && node app.js