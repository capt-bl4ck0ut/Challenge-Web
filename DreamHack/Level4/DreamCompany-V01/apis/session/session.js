const crypto = require("crypto");

const session = {
  guest: "84983c60f7daadc1cb8698621f802c0d9f9a3c3c295c810748fb048115c186ec",
  manager: "[**SECRET**]",
  fake: "[**SECRET**]",
};

const log = {};

const getTime = () => {
  let today = new Date();
  let hours = today.getHours();
  let minutes = today.getMinutes();
  let seconds = today.getSeconds();
  let milliseconds = today.getMilliseconds();
  return (
    String(hours) + String(minutes) + String(seconds) + String(milliseconds)
  );
};

const encoding = (input) => {
  return crypto.createHash("sha256").update(input).digest("hex");
};

const login = (id, pw) => {
  const sessionPW = session[id !== null ? id : "fake"];
  if (encoding(pw) === sessionPW) {
    log["user_log"] = "login to user, time : " + getTime();
    return true;
  } else {
    return false;
  }
};

const adminInit = () => {
  const time = getTime();
  session["admin"] = encoding("[**SECRET**]" + time);
  setTimeout(() => {
    log["admin_add_log"] = "[**SECRET**]";
  }, 1000);
};

const checkAdmin = (id, pw) => {
  if (String(id["admin_id"]).indexOf("admin") === -1) {
    return false;
  } else {
    const time = id["time"] ? id["time"] : getTime();
    const adminPW = encoding(pw + time);
    if (adminPW === session["admin"]) {
      log["admin_log"] = "login to admin, time : " + getTime();
      return true;
    } else {
      return false;
    }
  }
};

const addSession = (id, pw) => {
  try {
    const isOverlap = overlapSession(id);
    if (isOverlap) return false;
    session[/(guest[0-9]*)\w/g.test(id) === false ? "guest1" : id] =
      encoding(pw);
    log["user_add_log"] = "added to user, time : " + getTime();
    return true;
  } catch (e) {
    return false;
  }
};

const overlapSession = (id) => {
  if (session[id] != null) {
    return true;
  }
};

const checkSession = (id, pw) => {
  try {
    if (typeof id === "object") {
      isAdmin = checkAdmin(id, pw) === true ? "ADMIN" : login(id, pw);
      return isAdmin;
    } else {
      return login(id, pw);
    }
  } catch (e) {
    return false;
  }
};

module.exports.add = addSession;
module.exports.check = checkSession;
module.exports.overlap = overlapSession;
module.exports.adminInit = adminInit;
module.exports.all_session = {
  login_session: session,
  login_log: log,
};
