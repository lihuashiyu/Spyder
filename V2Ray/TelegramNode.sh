#!/usr/bin/env bash

# ==================================================================================================
#    FileName      ：  node.sh
#    CreateTime    ：  2024-08-10 09:05:26
#    ModifiedTime  ：  2024-08-10 09:06:09
#    Author        ：  lihua shiyu
#    Email         ：  lihuashiyu@github.com
#    Description   ：  互联网节点获取
# ==================================================================================================
    
    
SERVICE_DIR=$(dirname "$(readlink -e "$0")")                                   # 项目目录
SERVICE_NAME="telegram-node"                                                   # 项目名称
LOG_FILE="${SERVICE_NAME}-$(date "+%Y-%m-%d-%H").log"                          # 操作日志文件
GIT_PROJECT_DIR=$(cd "${SERVICE_DIR}/../" || exit; pwd)                        # git 项目目录
    
remote_host="1.1.1.1"                                                          # 需要远程同步的 主机名
remote_port="22"                                                               # 需要远程同步的 scp 端口号
remote_user="root"                                                             # 需要远程同步的 用户名
remote_password="111111"                                                       # 需要远程同步的 用户密码
remote_path="${HOME}"                                                          # 需要远程同步的 文件路径
   

# 刷新环境变量
function flush_env()
{
    local back_data                                                            # 定义局部变量
    
    export -A REMOTE_MAP=(["host"]="${remote_host}"  ["port"]="${remote_port}"           \
                          ["user"]="${remote_user}"  ["password"]="${remote_password}"   \
                          ["path"]="${remote_path}")                           # 远程节点参数
    
    echo "    ************************** 刷新环境变量 **************************    "
    source "/etc/profile"                                                      # 系统环境变量文件路径
    
    # 判断用户环境变量文件是否存在
    if [ -e "${HOME}/.bash_profile" ]; then
        source "${HOME}/.bash_profile"                                         # RedHat 用户环境变量文件
    elif [ -e "${HOME}/.bashrc" ]; then
        source "${HOME}/.bashrc"                                               # Debian、RedHat 用户环境变量文件
    fi
    
    echo "    **************************** 备份数据 ****************************    "
    if [ -e "${SERVICE_DIR}/data" ]; then
        back_data=$(date -d "1 hour ago" +"%Y-%m-%d-%H")                       # 获取一小时前的时间
        mv  "${SERVICE_DIR}/data" "${SERVICE_DIR}/${back_data}"                # 备份数据
    fi
    
    cd "${SERVICE_DIR}"  || exit                                               # 切换到项目目录
    mkdir -p  "${SERVICE_DIR}/data" "${SERVICE_DIR}/logs"                      # 创建存储数据和日志目录
    
    echo "    *************************** 删除旧数据 ***************************    "    
    find  "${SERVICE_DIR}"      -maxdepth 1 -mtime +1  -type d -name "*"     -exec rm -rf {} \;    # 删除超过 一 天的数据
    find  "${SERVICE_DIR}/logs" -maxdepth 1 -mtime +10 -type f -name "*.log" -exec rm -f  {} \;    # 删除超过 10 天的日志
}
    

# 更新 git 项目
function update_git_project()
{
    echo "    ************************* 更新 git 项目 **************************    "
    
    cd "${GIT_PROJECT_DIR}"  || exit                                           # 切换到 git 项目目录
    {
        git fetch --all                                                        # 获取修改位置
        git reset --hard                                                       # 重置所有更改
        git pull                                                               # 拉去最新代码
    } >> "${SERVICE_DIR}/logs/${LOG_FILE}" 2>&1
    
    cd "${SERVICE_DIR}"  || exit                                               # 切换到项目目录
    cp -fpr "${GIT_PROJECT_DIR}/V2Ray/TelegramNode.py"  "${SERVICE_DIR}/TelegramNode.py" # 复制爬虫文件
}
    

# 启动爬虫，处理数据
function spider_run()
{
    echo "    **************************** 运行爬虫 ****************************    "
    
    cd "${SERVICE_DIR}"  || exit                                               # 切换到项目目录
    python3 "${SERVICE_DIR}/TelegramNode.py"  >> "${SERVICE_DIR}/logs/${LOG_FILE}" 2>&1
    sleep 3
    
    echo "    **************************** 同步数据 ****************************    "
    sshpass -p "${REMOTE_MAP["password"]}"                                          \
        scp -P "${REMOTE_MAP["port"]}" "  ${SERVICE_DIR}/data/v2ray-node.txt"       \
               "${REMOTE_MAP["user"]}@${REMOTE_MAP["host"]}:${REMOTE_MAP["path"]}"
}
    

# 处理输入参数
function deal_args()
{
    local argument value                                                       # 定义局部变量
    
    for argument in "$@"
    do
        value=$(echo "${argument}" | awk -F '=' '{print $2}' | awk '{gsub(/^\s+|\s+$/, ""); print}')
        case "${argument}" in
            -h=* | --host=*)                                                   # 匹配 主机
                REMOTE_MAP["host"]=${value}
            ;;
            
            -p=* | --port=*)                                                   # 匹配 端口
                REMOTE_MAP["port"]=${value}
            ;;
            
            -u=* | --user=*)                                                   # 匹配 用户
                REMOTE_MAP["user"]=${value}
            ;;
            
            -d=* | --password=*)                                               # 匹配 密码
                REMOTE_MAP["password"]=${value}
            ;;
            
            -s=* | --path=*)                                                   # 匹配 路径
                REMOTE_MAP["path"]=${value}
            ;;
            
            *)                                                                 # 错误参数
                usage
                exit 1
            ;;
        esac
        
        shift 1                                                                # 移动标尺
    done
}
    

# 使用说明
function usage()
{
    local file_name                                                            # 定义局部变量
    file_name=$(echo "$0" | awk -F '/' '{ print $NF }')                        # 获取文件名
    
    echo "    usage： ${SERVICE_DIR}/${file_name} --arg=value    "
    echo "        --host=[HOST]           default ${remote_host}"
    echo "        --port=[PORT]           default ${remote_port}"
    echo "        --user=[USER]           default ${remote_user}"
    echo "        --password=[PASSWORD]   default ${remote_password}"
    echo "        --path=[PATH]           default ${remote_path}"
}
    

flush_env                                                                      # 刷新环境变量
deal_args "$@"                                                                 # 处理参数
update_git_project                                                             # 更新 git 项目
spider_run                                                                     # 启动爬虫
exit 0
