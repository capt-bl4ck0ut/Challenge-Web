import sqlite3 from 'sqlite3';
import { open } from 'sqlite';

async function openDatabase() {
    return open({
      filename: './mydatabase.db',
      driver: sqlite3.Database
    });
  }


export {openDatabase};