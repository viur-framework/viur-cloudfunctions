#!/usr/bin/env bash
gcloud functions deploy imagerenderer --runtime python39 --trigger-http --entry-point main --memory=1024MB --region=europe-west3 --env-vars-file env.yaml

