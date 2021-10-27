#!/bin/zsh
# backup your files into iCloud directory
# crontab: 0 12,18 * * *  /bin/zsh backup_task.zsh


DEST_HOME="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Backup/backup_task/"

LOG="$HOME/.backup_task.log"

# ************************************************************

task_log(){
    local time=$(date +"%Y-%m-%d %H:%M:%S")
    echo "[$time] $*" >> $LOG
}


if [ $(ls -l $LOG | awk '{print $5}') -ge 1048576 ]; then
    rm $LOG
    task_log "Delete LOG"
fi

# ************************************************************

task_log "Starting backup"
task_log "Destnation: $DEST_HOME"

# backup user config
task_log "backup user config"
cp $HOME/.vimrc $DEST_HOME/vimrc
cp $HOME/.zshrc $DEST_HOME/zshrc

# backup key file
task_log "backup ssh key"
cp $HOME/.ssh/* $DEST_HOME/

task_log "Done ~"
