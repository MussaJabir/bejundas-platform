# Database Guide — MySQL

This project uses **MySQL 8 / MariaDB** for both development and production. SQLite is **not** supported.

---

## Why MySQL everywhere

cPanel only supports MySQL/MariaDB. PostgreSQL is unavailable. Using SQLite locally and MySQL in production creates surprises:

- Charset behaviour (utf8 vs utf8mb4)
- Case sensitivity in identifiers and string comparisons
- Index size limits (varchar(255) hits the 767-byte limit on utf8mb3)
- JSONField behaviour
- Transaction isolation levels
- `ALTER TABLE` performance and locking

These all bite at deploy time. Match production locally to avoid the surprise.

---

## Production database (cPanel)

| Setting | Value |
|---|---|
| Engine | MySQL 8 / MariaDB (whichever cPanel provides) |
| Database name | `bejundas_db` (cPanel may prefix with username, e.g. `bejundas_bejundas_db`) |
| User | `bejundas_dbuser` |
| Host | `localhost` |
| Port | `3306` |
| Charset | `utf8mb4` |
| Collation | `utf8mb4_unicode_ci` |

Created via cPanel home > **MySQL Databases**. Grant ALL PRIVILEGES to the user on the database.

Verify charset and collation after creation:

```sql
SELECT default_character_set_name, default_collation_name
FROM information_schema.SCHEMATA
WHERE schema_name = 'bejundas_db';
```

If charset is wrong, recreate the DB or run:

```sql
ALTER DATABASE bejundas_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

---

## Local development database

### Install MySQL on Ubuntu

```bash
sudo apt update
sudo apt install mysql-server libmysqlclient-dev pkg-config
sudo mysql_secure_installation
```

### Create local database

```bash
sudo mysql
```

```sql
CREATE DATABASE bejundas_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bejundas_dbuser'@'localhost' IDENTIFIED BY 'devpassword';
GRANT ALL PRIVILEGES ON bejundas_db.* TO 'bejundas_dbuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Configure `.env`

```env
DB_NAME=bejundas_db
DB_USER=bejundas_dbuser
DB_PASS=devpassword
DB_HOST=localhost
DB_PORT=3306
```

### Verify

```bash
python manage.py dbshell
```

You should land in a MySQL prompt connected to `bejundas_db`.

---

## Settings configuration

In `config/settings/base.py`:

```python
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     env('DB_NAME'),
        'USER':     env('DB_USER'),
        'PASSWORD': env('DB_PASS'),
        'HOST':     env('DB_HOST'),
        'PORT':     env('DB_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

`STRICT_TRANS_TABLES` ensures invalid data raises errors instead of being silently truncated.

---

## Migrations

### Rules

- **Never** delete a migration file
- **Never** edit a migration that has already been applied to production
- **Never** run `migrate --fake` without a code comment explaining why
- Always run `python manage.py makemigrations` before pushing model changes
- Always run `python manage.py migrate --plan` to preview before applying in production

### Creating migrations

```bash
python manage.py makemigrations apps.hub
python manage.py migrate
```

### Renaming a model field (the safe way)

Don't:
```python
old_name = models.CharField(...)  # delete this
new_name = models.CharField(...)  # add this
```

That generates a `RemoveField` + `AddField` pair, which **drops data**.

Do (across multiple migrations):

1. Migration 1 — add new field, leave old field:
   ```python
   old_name = models.CharField(...)
   new_name = models.CharField(blank=True, default='')
   ```

2. Migration 2 — data migration (`RunPython`) to copy `old_name` -> `new_name`.

3. Deploy this state to production. Verify.

4. Migration 3 — remove old field:
   ```python
   new_name = models.CharField(...)
   ```

This pattern avoids data loss and avoids long table locks on large tables.

### Squashing migrations

After many migrations accumulate on a stable model, squash:
```bash
python manage.py squashmigrations apps.hub 0001 0015
```

Only do this when the squashed range has been fully deployed. Never squash unapplied migrations.

---

## Backups

### Production

Configure cPanel automated backups (cPanel > **Backup Wizard**).

For application-level backups, run via cron:

```bash
mysqldump --single-transaction --quick --lock-tables=false \
  -u bejundas_dbuser -p'<password>' bejundas_db \
  | gzip > /home/bejundas/backups/bejundas_db_$(date +\%Y\%m\%d).sql.gz
```

Retain 7 daily + 4 weekly backups. Rotate older ones.

### Restore

```bash
gunzip < bejundas_db_20260510.sql.gz | mysql -u bejundas_dbuser -p bejundas_db
```

---

## Common issues

| Symptom | Likely cause | Fix |
|---|---|---|
| `OperationalError: (1045, "Access denied")` | Wrong password or user not granted privileges | Verify `.env` matches cPanel; re-grant privileges |
| `OperationalError: (1071, "Specified key was too long")` | Index on `varchar(255)` with `utf8mb3` charset | Confirm DB is `utf8mb4`; reduce field length to `varchar(191)` if stuck on utf8mb3 |
| `Incorrect string value` on save | Charset mismatch (likely utf8mb3) | `ALTER TABLE ... CONVERT TO CHARACTER SET utf8mb4` |
| Migrations hang on production | Long-running `ALTER TABLE` on big table | Use `pt-online-schema-change` (Percona Toolkit) for big tables |
| `1366, "Incorrect integer value"` | `STRICT_TRANS_TABLES` rejecting bad data | Fix the code that's writing wrong data |
| Slow queries on production | Missing index | Use `EXPLAIN`, add index in a migration |

---

## utf8mb4 — what and why

- `utf8mb3` (Django 5+ calls it just `utf8`) is **3 bytes per character** and **cannot store emoji** or many non-BMP characters
- `utf8mb4` is **4 bytes per character** and stores any Unicode codepoint
- Always use `utf8mb4` for new databases. Never use `utf8mb3`
- If you inherit a `utf8mb3` database, plan a migration to `utf8mb4` before users complain about emoji corruption
