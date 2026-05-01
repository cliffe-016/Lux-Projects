# Setting up Airflow 3.0+ for production

After installation and main directory setup:

## 1. Database Configuration
Navigate to `~/airflow/airflow.cfg` and find:
```
[database]
sql_alchemy_conn = my_conn_string
```
Replace 'my_conn_string' with your preferred database's connection string. Ensure the database and user exist in the database.

## 2. Remove test dags
Find:
```
[core]
load_examples = True
```
Replace `True` with `False`.

## 3. Postgres Configuration
If you're using postgres, navigate to `/etc/postgresql/[version]/main/pg_hba.conf` and add the following at the bottom:
```
# TYPE  DATABASE             USER                 ADDRESS                 METHOD
host    your_airflow_db      your_airflow_user    127.0.0.1/32            md5
```
If Airflow is running in Docker or on a separate node, replace the IP with the specific IP address or CIDR range of the Airflow server.
Reload the postgres service:
```
sudo systemctl restart postgresql
```
---

# User Creation

In Airflow 3.x, user management is handled through the **FAB Auth Manager**. If it’s not configured correctly, the `airflow users create` command won’t work or authentication will fail.

This guide shows you how to correctly configure Airflow so you can create users, manage roles, and log into the UI securely.

---

## 1. Install Required Dependencies

Inside your Airflow virtual environment:

```bash
pip install --upgrade pip setuptools flask_appbuilder
pip install apache-airflow-providers-fab
pip install apache-airflow-providers-fab
```

### Why this matters

- `flask_appbuilder` → provides user management UI + RBAC
- `apache-airflow-providers-fab` → connects Airflow 3.x auth system to FAB

---

## 2. Set the Correct Auth Manager

Open your `airflow.cfg`:

```bash
nano ~/airflow/airflow.cfg
```

Find or add:

```
[core]
auth_manager = airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager
```

### Important

Without this, Airflow will not use the FAB authentication system → user creation breaks or is ignored.

---

## 3. Generate Security Keys

Airflow 3.x requires strong secrets for authentication and CSRF protection.

Run:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Do this **twice** (generate two keys):

---

## Add to `airflow.cfg`

### JWT Secret

```
[api]
jwt_secret = YOUR_JWT_SECRET_HERE
```

### Flask/FAB Secret (CSRF protection)

```
[webserver]
secret_key = YOUR_SECOND_SECRET_HERE
```

---

## 4. Initialize / Migrate Database

Run:

```bash
airflow db migrate
```

---

## 5. Create an Admin User

Now user creation will work properly:

```bash
airflow users create \
  --username admin \
  --firstname Peter \
  --lastname Parker \
  --role Admin \
  --email spiderman@superhero.org \

```

### Roles you can use:

- Admin → full access
- User → normal access
- Viewer → read-only
- Op → DAG execution only

---

## 6. Start Airflow Webserver

```bash
airflow webserver --port 8080
```

Then in another terminal:

```bash
airflow scheduler
```

Now open:

```
http://localhost:8080
```

Login with your admin credentials.

---

## 7. Verify User System Works

Inside Airflow:

- Go to **Security → List Users**
- You should see your admin user
- Try creating another user from CLI or UI

---

## 8. Common Issues & Fixes

### “No module fab_auth_manager”

✔ Fix:

```bash
pip install apache-airflow-providers-fab
```

---

### Login page loop / session errors

✔ Fix:

- Ensure `secret_key` is set
- Restart webserver

---

### Users created but cannot log in

✔ Fix:

- Ensure you are using **FAB Auth Manager**
- Check DB migrated properly

---

## 9. Recommended Production Setup (Important)

For real deployment:

- Use **PostgreSQL instead of SQLite**
- Store secrets in environment variables (not airflow.cfg)
- Use systemd or Docker for services
- Enable RBAC (already default in FAB)

---

## Final Checklist

To initialize Airflow 3.x in production:

✔ Edit the database connection string in the airflow configuration file

✔ Remove test dags

✔ Add airflow user and database to the postgres configuration file

✔ Reload postgres service

✔ Install FAB provider

✔ Set `FabAuthManager` in config

✔ Generate JWT + secret_key

✔ Run DB migration

✔ Create users with CLI

---
