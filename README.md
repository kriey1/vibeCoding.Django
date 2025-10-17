# vibeCoding.Django

Django 기반의 웹 프로젝트입니다.

## 주요 기능
- 사용자 인증 및 프로필
- 게시글 CRUD
- REST API 제공
- 관리자 페이지
- 테스트 코드 포함

## 개발 및 실행 방법
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 배포
- WSGI 기반 서버(Gunicorn, Nginx 등) 사용 가능
- staticfiles, media 경로 분리

## 테스트
```bash
python manage.py test core
```
