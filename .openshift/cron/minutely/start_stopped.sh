cd $OPENSHIFT_REPO_DIR
nohup python main.py start_stopped cron-minutely > $OPENSHIFT_DIY_LOG_DIR/server.log 2>&1 &
