const filter = (check) => {
  const html = /\<|\>|\"|\'|\%|\;|\(|\)|\&|\+|\-/g;
  if (check.match(html, "") !== null) {
    return true;
  }
};

module.exports = (checkInput) => {
  try {
    for (let check in checkInput) {
      if (filter(checkInput[String(check)].toLowerCase())) {
        return true;
      }
    }
  } catch (e) {}
};
