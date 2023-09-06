docker build --tag teams_bot .
@REM docker run -d -p 80:80 teams_bot
docker tag teams_bot tandyy/teams_bot:latest
docker push tandyy/teams_bot:latest