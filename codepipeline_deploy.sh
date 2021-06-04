#!/bin/bash

aws cloudformation deploy \
  --template-file cloudformation_codepipeline_bitbucket.yml \
  --stack-name payment-portal-codepipeline-stack \
  --parameter-overrides Environment=dev Branch=codebuild Repo=username/repo \
  Image=aws/codebuild/standard:5.0 \
  --capabilities CAPABILITY_NAMED_IAM