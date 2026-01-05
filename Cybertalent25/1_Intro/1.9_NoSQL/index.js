const express = require('express');
const mysql = require('mysql2/promise');
const rateLimit = require('express-rate-limit');
const fs = require('fs');
const path = require('path');
const hljs = require('highlight.js');

const app = express();

function nosql(req, res, next) {
  let input = JSON.stringify(req.body || "").toLowerCase();

  let blacklist = [
	  'select',
	  'union',
	  'insert',
	  'update',
	  'delete',
	  'drop',
	  'alter',
	  'create',
	  'truncate',
	  'replace',
	  'rename',
	  'handler',
	  'load',
	  'limit',
	  'or',
	  'and',
	  'xor',
	  'like',
	  'regexp',
	  'sleep',
	  'benchmark',
	  'extractvalue',
	  'updatexml',
	  'information_schema',
	  'mysql',
	  'sys',
	  'version',
	  'pg_catalog',
	  'sqlite_master',
	  'case',
	  'when',
	  'then',
	  'end',
	  '--',
	  '#',
	  '/*',
	  '*/',
	  ';',
	  "'",
  ];

  if (blacklist.some(k => input.includes(k))) {
    return res.status(403).json({
      ok: false,
      error: "Hacking attempt detected! No SQL allowed!"
    });
  }

  next();
}

const ratelimiter = rateLimit({
  windowMs: 10 * 1000,
  max: 15,
  message: {
    ok: false,
    error: 'Hold that flag! You\'re capturing them faster than we can check them'
  }
});

app.use(express.static(path.join(__dirname, 'public'), {
  maxAge: '30d',
  immutable: true
}));
app.use('/validate', express.json());
app.use('/validate', nosql);
app.use('/validate', ratelimiter);

const {
  MYSQL_HOST,
  MYSQL_PORT,
  MYSQL_DATABASE,
  MYSQL_USER,
  MYSQL_PASSWORD,
  FLAG = 'FAKEFLAGFAKEFLAGFAKEFLAG',
  PORT = 80
} = process.env;

const db = mysql.createPool({
  host: MYSQL_HOST,
  port: MYSQL_PORT,
  user: MYSQL_USER,
  password: MYSQL_PASSWORD,
  database: MYSQL_DATABASE,
  waitForConnections: true,
  connectionLimit: 10,
  connectTimeout: 5000
});

async function initDb() {
  const createSql = `
    CREATE TABLE IF NOT EXISTS flags (
      id INT AUTO_INCREMENT PRIMARY KEY,
      flag TEXT NOT NULL
    ) ENGINE=InnoDB
  `;

  await db.query(createSql);

  if (!FLAG) return;

  const insertSql = `
    INSERT INTO flags (flag)
    SELECT ? FROM (SELECT 1) AS tmp
    WHERE NOT EXISTS (SELECT 1 FROM flags WHERE flag = ?)
    LIMIT 1
  `;

  await db.query(insertSql, [FLAG, FLAG]);
}

app.get('/source', (req, res) => {

  const filePath = path.join(__dirname, 'index.js');
  fs.readFile(filePath, 'utf8', (err, code) => {
    if (err) return res.status(500).send('Server error');
    const highlighted = hljs.highlight(code, { language: 'javascript' }).value;
    const html = `
      <!doctype html>
      <html>
        <head>
          <meta charset="utf-8">
          <link rel="stylesheet" href="/assets/theme.css">
	  <style>html, body { margin: 0; padding: 0; } pre { margin: 0; }</style>
        </head>
        <body>
          <pre><code class="hljs javascript">${highlighted}</code></pre>
        </body>
      </html>`;
    res.type('html').send(html);
  });
});

app.post('/validate', async (req, res) => {
  let { flag } = req.body;

  if (!flag)
    return res.status(400).json({ ok: false, error: "Can't check a missing flag." });

  let sql = 'SELECT flag FROM flags WHERE flag = ? LIMIT 1';

  try {
    let [rows] = await db.query(sql, [flag]);
    flag = rows.length ? rows[0].flag : null;
    if (!flag)
      return res.json({ ok: false, message: 'That flag is invalid!' });
    return res.json({ ok: true, message: `${flag} is a valid flag!` });
  } catch (err) {
    console.error('DB error:', err);
    return res.status(500).json({ ok: false, error: 'db error' });
  }
});

initDb()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`Server is running on http://localhost:${PORT}`);
    });
  })
  .catch(err => {
    console.error('Failed to initialize DB:', err);
    process.exit(1);
  });
