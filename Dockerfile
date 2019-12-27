FROM        jeonyh0924/deploy-igloo1226:base
# 전체 파일 복사
COPY        ./  /srv/project

# 명령을 실행할 디렉토리 지정
WORKDIR     /srv/project/app

RUN             python3 manage.py collectstatic --noinput

# 기존 Nginx 파일 삭제 및 새 Nginx 파일 복사
RUN         rm -rf /etc/nginx/sites-available/* && \
            rm -rf /etc/nginx/sites-enabled/* && \
            cp -f  /srv/project/.config/app.nginx \
                   /etc/nginx/sites-available/ && \
            ln -sf /etc/nginx/sites-available/app.nginx \
                   /etc/nginx/sites-enabled/app.nginx

# supervisor 파일 복사
RUN         cp -f /srv/project/.config/supervisord.conf \
                  /etc/supervisor/conf.d/

EXPOSE          80

# Command로 supervisor 실행
CMD             supervisord -n
