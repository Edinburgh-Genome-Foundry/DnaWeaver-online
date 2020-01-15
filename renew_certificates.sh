docker-compose stop
certbot renew
cp /etc/letsencrypt/live/dnaweaver.genomefoundry.org/*.pem /cert/
systemctl stop nginx
pkill nginx
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up