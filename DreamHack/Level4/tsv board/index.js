const fs = require('fs');
const express = require('express');

const app = express();
app.use(express.urlencoded({ extended: false }));

const FLAG = fs.readFileSync('./flag.txt', 'utf8');
const SECRET = Buffer.from(crypto.getRandomValues(new Uint8Array(32))).toString('hex');

// title | content | password
let tsv = `
delete me\tdelete me to see the flag :)\t${SECRET}
hi there\tfollow me on github! :D    https://github.com/Xvezda\tspam
`.trim();

function escape(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/'/g, '&#x27;')
    .replace(/"/g, '&quot;');
}

function isDeleted(id) {
  const rows = tsv.split('\n');
  return id in rows && !rows[id].includes('\t');
}

app.get('/', (_req, res) => {
  const rows = tsv.split('\n');

  if (isDeleted(0)) {
    res.send(`<pre>good job! here is your flag\n\n${FLAG}</pre>`);
    return;
  }

  res.send(`
    <h1>tsv board</h1>
    <ul>
      ${rows.map((row, i) => {
        if (isDeleted(i)) {
          return `<li><i>[DELETED]</i></li>`;
        }
        const [title] = row.split('\t');
        return `
          <li><a href="/articles/${i}">${escape(title)}</a></li>
        `;
      }).join('')}
    </ul>
    <a href="/editor">write</a>
  `);
});

app.get('/editor', (req, res) => {
  const rows = tsv.split('\n');
  if ('id' in req.query) {
    if (req.query.id in rows) {
      const { id } = req.query;
      const [title, content = ''] = rows[id].split('\t');
      res.send(`
        <h1>edit #${id}</h1>
        <form action="/actions" method="post">
          <input type="hidden" name="id" value="${id}">
          <input type="hidden" name="mode" value="edit">
          <div>
            <input name="title" placeholder="title" value="${escape(title)}" required>
          </div>
          <div>
            <textarea name="content" cols="80" rows="25" placeholder="content">${escape(content).replaceAll('  ', '\n')}</textarea>
          </div>
          <input type="password" name="password" placeholder="password">
          <button type="submit">submit</button>
        </form>
      `);
      return;
    }
    res.status(404).send('Not Found');
    return;
  }

  res.send(`
    <h1>write</h1>
    <form action="/actions" method="post">
      <input type="hidden" name="mode" value="write">
      <div>
        <input name="title" placeholder="title" required>
      </div>
      <div>
        <textarea name="content" cols="80" rows="25" placeholder="content"></textarea>
      </div>
      <input type="password" name="password" placeholder="password">
      <button type="submit">submit</button>
    </form>
  `);
});

app.get('/articles/:id(\\d+)', (req, res) => {
  const { id } = req.params;
  const rows = tsv.split('\n');

  if (id in rows) {
    if ('delete' in req.query) {
      res.send(`
        <h1>delete #${id}</h1>
        <form action="/actions" method="post">
          <input type="hidden" name="id" value="${id}">
          <input type="hidden" name="mode" value="delete">
          <input type="password" name="password" placeholder="password">
          <button type="submit">delete</button>
        </form>
      `);
      return;
    }

    if (rows[id].includes('\t')) {
      const [title, content = ''] = rows[id].split('\t');

      res.send(`
        <h1>${escape(title)}</h1>
        <pre>${escape(content).replaceAll('  ', '\n')}</pre>
        <a href="/editor?id=${id}">edit</a>
        <a href="/articles/${id}?delete">delete</a>
      `);
      return;
    }
  }
  res.status(404).send('Not Found');
});

app.post('/actions', (req, res) => {
  const filter = (fields) => fields
    .map((field) => field.replace(/\n/g, '  ').replace(/[\r\t]/g, ''));

  const { mode, id, title = '', content = '', password = '' } = req.body;

  const rows = tsv.split('\n');
  const article = rows[id];
  const [, , secret = ''] = filter(article?.split?.('\t') ?? []);

  if (mode === 'write' && title.length) {
    rows.push(filter([title, content, password]).join('\t'));
  } else if (mode === 'edit' && title.length && secret === password) {
    rows[id] = filter([title, content, password]).join('\t');
  } else if (mode === 'delete' && secret === password) {
    delete rows[id];
  } else {
    return res.status(403).send('Forbidden');
  }
  tsv = rows.join('\n');

  return res.redirect('/');
});

const port = 8000;
app.listen(port, () => {
  console.log(`listening on port ${port}`);
});
