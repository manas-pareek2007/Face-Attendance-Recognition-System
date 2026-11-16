# Attendly - Face Recognition Attendance

A small Django application for employee/student registration, face enrollment, webcam attendance scans, attendance history, and an admin attendance view.

## What it does

- Registers an account with name, email, phone, role, department, password, and a camera-captured face template.
- Provides a public `/kiosk/` page for continuous camera attendance. Employees enroll once, then walk up to the kiosk without signing in. The admin dashboard still requires admin login.
- Allows an enrolled person to be scanned one at a time, as the specification's quality gate requires exactly one face per frame.
- Signs users in with their registered email and password when they need to view their own attendance.
- Starts the webcam only after the user clicks **Start face scan**. The browser submits still frames to Django; the server checks for exactly one adequately sized face, acceptable brightness and sharpness, then compares its 128-value encoding with enrolled templates.
- Marks one attendance record per person per local date. A match distance up to 0.50 is accepted; scans after 09:30 are marked late.
- Keeps unknown and low-quality attempts in the recognition log without marking attendance.
- Provides a staff dashboard with employee/date filters and an employee’s own attendance history.
- Uses SQLite by default for a quick local setup. MySQL can be selected through environment variables.

Face data is sensitive biometric information. This starter stores only the face encoding in the database, not the captured enrollment image. Use HTTPS in deployment and restrict access to the database and admin account.

## Requirements

Python 3.14 (64-bit on Windows), a webcam, and the dependencies in `requirements.txt`. Face matching uses dlib directly with its 128-value face descriptor. The `dlib-bin` package supplies a prebuilt dlib wheel for CPython 3.14 on Windows x64, avoiding a local C++ build. PyMySQL provides the MySQL database adapter.

## Run locally

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000. Webcam access is allowed on localhost. Create regular user accounts from **Create account**. Sign in with the superuser credentials to see the admin attendance log and use Django's `/admin/` for data administration.

## MySQL configuration

Install a MySQL server, then set these environment variables before running migrations:

```powershell
$env:DB_ENGINE = "mysql"
$env:DB_NAME = "attendance"
$env:DB_USER = "root"
$env:DB_PASSWORD = "your-password"
$env:DB_HOST = "127.0.0.1"
$env:DB_PORT = "3306"
python manage.py migrate
```

Set `DJANGO_SECRET_KEY` to a private random value and `DJANGO_DEBUG=0` for deployment. Configure `DJANGO_ALLOWED_HOSTS` as a comma-separated host list.

## Recognition notes

The specification mixes `/api/attendance/scan` with `/api/recognise/`; this implementation uses `/api/attendance/scan/` as described in the activity and sequence flows. It also suggests storing enrollment images and includes unrelated bandwidth/network configuration actions in the admin use cases. This starter omits those unrelated controls and avoids retaining raw face images. Face detection and matching use dlib plus models from `face-recognition-models`; OpenCV alone can detect faces but cannot identify them. Without these model dependencies the registration and scan screens return a clear setup message instead of claiming a successful match.
