Title FAQ BOT Presentation Server

echo "FAQ BOT Presentation Starting"

cd /d %~dp0\presentation\faqbot && dir

python manage.py runserver

Pause