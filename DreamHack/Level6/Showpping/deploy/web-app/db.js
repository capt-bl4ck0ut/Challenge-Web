const sqlite = require("sqlite-async")

class Database {
  constructor(fileName) {
    this.fileName = fileName
    this.db = undefined
  }

  async connect() {
    this.db = await sqlite.open(this.fileName)
  }

  async init() {
    return this.db.exec(`
        DROP TABLE IF EXISTS users;

        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name       VARCHAR(128) NOT NULL UNIQUE,
            password   VARCHAR (128) NOT NULL,
            email      VARCHAR (128) NOT NULL,
            address    VARCHAR (255) NOT NULL,
            balance    DOUBLE NOT NULL,
            coupon     VARCHAR(128) NOT NULL,
            used       TINYINT NOT NULL
        );

        DROP TABLE IF EXISTS products;

        CREATE TABLE IF NOT EXISTS products (
            id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            product_name  VARCHAR(128) NOT NULL,
            img_path   VARCHAR(128) NOT NULL,
            price      DOUBLE NOT NULL,
            flag       TINYINT NOT NULL
        );

        DROP TABLE IF EXISTS coupons;

        CREATE TABLE IF NOT EXISTS COUPONS (
            id          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            coupon_id   VARCHAR(128) NOT NULL UNIQUE,
            coupon_name VARCHAR(128) NOT NULL,
            value       DOUBLE NOT NULL,
            admin       TINYINT NOT NULL
        );

        INSERT INTO USERS (name, password, email, address, balance, coupon, used) VALUES ("guest", "guest", "guest@dreamhack.io", "123 Maple Street Springfield, IL 62704 USA", 0, "", 0);

        INSERT INTO PRODUCTS (product_name, img_path, price, flag) VALUES ("FLAG", "../static/img/flag.png", 13377, 1);
        INSERT INTO PRODUCTS (product_name, img_path, price, flag) VALUES ("CANDY", "../static/img/candy.png", 0, 0);

        INSERT INTO COUPONS (coupon_id, coupon_name, value, admin) VALUES ("34a27d00d8bc51ac025df6033ef2927ef015161dbee2c15611ec6907be04bbcf", "welcome", 10, 1);
        
    `)
  }

  async checkUser(name, password) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "select * from users where name=? and password=?;"
        )
        resolve(await prepared.get(name, password))
      } catch (e) {
        reject(e)
      }
    })
  }

  async getUser(name) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "select * from users where name=?;"
        )
        resolve(await prepared.get(name))
      } catch (e) {
        reject(e)
      }
    })
  }

  async setUsedCoupon(name) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "update users set used=1 where name=?;"
        )
        resolve(await prepared.run(name))
      } catch (e) {
        reject(e)
      }
    })
  }

  async resetBCU(name) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          'update users set balance=0, coupon="", used=0 where name=?;'
        )
        resolve(await prepared.run(name))
      } catch (e) {
        reject(e)
      }
    })
  }

  async getProducts() {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare("SELECT * from products;")
        resolve(await prepared.all())
      } catch (e) {
        reject(e)
      }
    })
  }

  async getProduct(id) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "SELECT * from products where id=?;"
        )
        resolve(await prepared.get(id))
      } catch (e) {
        reject(e)
      }
    })
  }

  async addCoupon(coupon_id, coupon_name, value, admin) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "insert into coupons (coupon_id, coupon_name, value, admin) values (?,?,?,?);"
        )
        resolve(await prepared.run(coupon_id, coupon_name, value, admin))
      } catch (e) {
        console.log(e)
        reject(e)
      }
    })
  }

  async getCoupon(coupon_id) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "select * from coupons where coupon_id=?;"
        )
        resolve(await prepared.get(coupon_id))
      } catch (e) {
        reject(e)
      }
    })
  }

  async deleteCoupons() {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare("delete from coupons;")
        resolve(await prepared.run())
      } catch (e) {
        reject(e)
      }
    })
  }

  async setCoupon(name, coupon_id) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "update users set coupon=? where name=?;"
        )
        resolve(await prepared.run(coupon_id, name))
      } catch (e) {
        reject(e)
      }
    })
  }

  async setBalance(name, balance) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "update users set balance=? where name=?;"
        )
        resolve(await prepared.run(balance, name))
      } catch (e) {
        reject(e)
      }
    })
  }

  async addBalance(name, value) {
    return new Promise(async (resolve, reject) => {
      try {
        let prepared = await this.db.prepare(
          "update users set balance= balance + ? where name=?;"
        )
        resolve(await prepared.run(value, name))
      } catch (e) {
        reject(e)
      }
    })
  }
}

module.exports = Database
