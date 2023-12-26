#!/bin/sh
#
# 备份mac重要文件
#

BACKUP_HOME=~/Documents/backup/
SCRIPT_NAME=backup_mac.sh
BACKUP_CRON="0 17 * * *"
KEEP_BACKUP_NUM=3
BACKUP_ITEM=(
    ~/.vimrc
    ~/.zshrc
    ~/.config/clash
    ~/.config/pip
    ~/.ssh/id_rsa
    ~/.ssh/id_rsa.pub
)

TIME=$(date +'%Y%m%d%H%M%S')
BACKUP_DESTINATION=${BACKUP_HOME}${TIME}/
BACKUP_SCRIPT=${BACKUP_HOME}${SCRIPT_NAME}


function log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')]: $@"
}

function backup_mac_task() {
    if [[ ! -d ${BACKUP_DESTINATION} ]]; then
        log "create backup destination ${BACKUP_DESTINATION}"
        mkdir -p ${BACKUP_DESTINATION}
    fi
    log "backup ${BACKUP_ITEM[@]}"
    for item in ${BACKUP_ITEM[@]}; do
        cp -r ${item} ${BACKUP_DESTINATION}
    done
    log "backup done"
    backup_num=$(ls -l ${BACKUP_HOME} | grep "^d" | wc -l)
    if [[ ${backup_num} -gt ${KEEP_BACKUP_NUM} ]]; then
        for old_item in $(ls -ltr ${BACKUP_HOME}|awk '/^d/ {print $NF}'); do
            old_item=${BACKUP_HOME}${old_item}
            log "remove earlier backup: ${old_item}"
            rm -rf ${old_item}
            backup_num=$(ls -l ${BACKUP_HOME} | grep "^d" | wc -l)
            if [[ ${backup_num} -le ${KEEP_BACKUP_NUM} ]]; then
                break
            fi
        done
    fi
}

function set_crontab() {
    remove_crontab
    log "install ${SCRIPT_NAME} to crontab"
    if [[ ! -d ${BACKUP_HOME} ]]; then
        log "create backup home ${BACKUP_HOME}"
        mkdir -p ${BACKUP_HOME}
    fi
    cp $0 ${BACKUP_SCRIPT}
    chmod +x ${BACKUP_SCRIPT}
    (crontab -l; echo "${BACKUP_CRON} ${BACKUP_SCRIPT} run >> ${BACKUP_SCRIPT}.log") | crontab -
}

function remove_crontab() {
    log "remove ${SCRIPT_NAME} from crontab"
    (crontab -l | grep -v ${SCRIPT_NAME}) | crontab -
    log "remove backup script ${BACKUP_SCRIPT}"
    rm ${BACKUP_SCRIPT}
}

function main() {
    case $1 in
        run)
            backup_mac_task
            ;;
        install)
            set_crontab $0
            ;;
        remove)
            remove_crontab
            ;;
        *)
            log "error command line"
            ;;
    esac
}

########## START ############

main $@
