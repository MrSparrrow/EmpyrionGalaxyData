EmpyrionGalaxyData

#### How to build locally:
```text
You will need to setup a service account in GCP that you can authenticate with:
https://cloud.google.com/docs/authentication/production#create_service_account
As described in the guide, you will need to save your credentials.json locally and create an environment variable that maps to the path to the json
```
```shell
#Build the docker image
docker build . -t uvicorn

#run from cmd, not git bash
docker run -p 80:80/tcp -e GOOGLE_APPLICATION_CREDENTIALS=/keys/docker-creds.json -v $GOOGLE_APPLICATION_CREDENTIALS:/keys/docker-creds.json:ro uvicorn:latest
```

The App should be available on localhost:80 if Docker doesn't give any errors