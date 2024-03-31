VERSION=${VERSION:-latest}

debug=echo
#debug=

echo Update cluster to version=$VERSION

$debug kubectl set image deployment/wordle-deployment wordlebot=wordle_bot_ci:$VERSION
$debug kubectl set image cronjob/wordle-job wordlebot-job=wordle_bot_ci:$VERSION

# build angular part and push it to bucket
pushd wordle-ui/
ng build
cd dist/wordle-ui
gcloud storage cp * gs://wordle-ui/
popd
