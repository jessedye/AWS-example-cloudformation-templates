#!/bin/bash

aws cloudformation deploy \
  --template-file cloudformation_ecs_blue-green.yml \
  --stack-name payment-portal-codepipeline-stack \
  --parameter-overrides Environment=dev \
  --capabilities CAPABILITY_NAMED_IAM