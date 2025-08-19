#!/bin/bash
sqlite3 deploy/mydatabase.db < deploy/create.sql
cd deploy
npm run dev -- --host 0.0.0.0
