#!/bin/bash
bucket=$1
curl -sL http://www.cs.cmu.edu/~dbamman/data/booksummaries.tar.gz | tar xz
mv booksummaries/ data/
aws s3 cp --recursive data/booksummaries $bucket
