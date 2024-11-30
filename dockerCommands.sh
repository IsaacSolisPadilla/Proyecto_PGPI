docker build -t aura-arcana .
docker run -p 8000:8000 django-app

docker tag aura-arcana megamagolas/aura-arcana:latest
docker login
docker push megamagolas/aura-arcana:latest

