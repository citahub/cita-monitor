#!/bin/bash
##
Get_osPlatform(){
    if (echo ${os}|grep centos) || (echo ${os}|grep 'Red Hat')
    then
        echo -e "\033[37;31;5m\t yum install -y git gcc gcc-c++ python36u python36u-pip python36u-devel dos2unix\033[39;49;0m"
        yum makecache fast
        yum install -y epel-release
        yum install https://centos7.iuscommunity.org/ius-release.rpm -y
        yum-config-manager --add-repo https://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
        yum install -y git gcc gcc-c++ python36u python36u-pip python36u-devel dos2unix
        ln -s /usr/bin/python3.6 /usr/bin/python3
        python3 -m pip install --upgrade pip
        service docker start
    elif (echo ${os}|grep Ubuntu)
    then
        echo -e "\033[37;31;5m\t apt install -y git gcc python3 python3-dev python3-pip dos2unix\033[39;49;0m"
        apt update
        apt install -y git gcc python3 python3-dev python3-pip dos2unix
        python3 -m pip install --upgrade pip
    else
        echo -e "\033[31m\t The host os version is not supported!\033[0m"
        exit
    fi
}
#
Check_ENV(){
    list=("python3" "pip3")
    for check_target in ${list[@]}
    do
        check=`which ${check_target}`
        if [[ -z "${check}" ]]
        then
                echo -e "\033[31m\t 未检测到 ${check_target} 命令，请手动更新 repo 源后，再次尝试执行安装脚本；\033[0m"
                exit
        else
                echo -e "\033[32m\t 已检测到 ${check_target} 命令，绝对路径 \"${check}\"\033[0m"
        fi
    done
}
#
Install_Python_libs(){
    cat << EOF > ./requirements.txt
requests
prometheus-client==0.5.0
flask
python-geohash
gevent
psutil
paramiko
cryptography==2.4.2
EOF
    echo -e "\033[37;31;5m\t pip3 install -r ./requirements.txt\033[39;49;0m"
    pip3 install -r ./requirements.txt
    if [ $? != 0 ]
    then
        echo -e "\033[31m\t python 依赖模块安装失败，请手动安装 requirements.txt 罗列的模块后再次执行安装过程；\033[0m"
        rm -rf ./requirements.txt
        exit
    fi
    rm -rf ./requirements.txt
}
#
Install_cita_tool(){
    scp $cur_dir/cita-cli /bin/cita-cli && chmod +x /bin/cita-cli
}
#
Install_AgentService(){
    if (echo ${os}|grep centos) || (echo ${os}|grep 'Red Hat')
    then
        cp -rf $cur_dir/cita-agent.py $work_dir
        cp -rf $cur_dir/cita-agentd /etc/init.d/
        dos2unix $work_dir/cita-agent.py
        dos2unix /etc/init.d/cita-agentd
        chmod +x /etc/init.d/cita-agentd
    elif (echo ${os}|grep Ubuntu)
    then
        cp -rf $cur_dir/cita-agent.py $work_dir
        cp -rf $cur_dir/cita-agentd.service /etc/systemd/system/
        dos2unix $work_dir/cita-agent.py
        dos2unix /etc/systemd/system/cita-agentd.service
        systemctl daemon-reload
        systemctl enable cita-agentd
    else
        echo -e "\033[31m\t Your os version is not supported!\033[0m"
    fi
}
#
END(){
    if (echo ${os}|grep centos) || (echo ${os}|grep 'Red Hat')
    then
        echo -e "\033[32m\t cita-agentd 安装成功，您可以使用 ' service cita-agentd start | restart | stop '或者' /etc/init.d/cita-agentd start | restart | stop '命令来进行服务起停操作；\n\t 手动测试：\"python3 $work_dir/cita-agent.py\"033[0m"
        rm -rf $cur_dir/git-test
    elif (echo ${os}|grep Ubuntu)
    then
        echo -e "\033[32m\t cita-agentd 安装成功，您可以使用 ' service cita-agentd start | restart | stop '命令来进行服务起停操作；\n\t 手动测试：\"python3 $work_dir/cita-agent.py\"033[0m"
        rm -rf $cur_dir/git-test
    else
        echo "\033[31m\t Your os version is not supported!\033[0m"
    fi
}
##
if [[ `whoami` = "root" ]];then
    Permission=1
else
    echo -e "\033[31m\t 当前账户权限不足，建议切换 root 账户后再次尝试；\033[0m"
    exit
fi
#
echo -e """\e[1;36m
执行脚本将会对本机器进行下列功能增加或修改：
1、安装 Python3 环境，安装 pip3 ；
2、安装基于 Prometheus agent 开发的 CITA agent 服务所需要的 python 模块，包括但不限于当前罗列的信息；
（prometheus_client、flask 、json、requests、os、platform、geohash、psutil、threading）
3、脚本执行完毕后会创建 cita-agent 服务，您可以使用 start|restart|stop 命令来控制服务启停；
\e[0m"""
read -p "如果你同意上述的信息，请输入 Y 进行确认(Y/N)?  :  " confirm
#
if [[ x"$confirm" = 'xY' ]] || [[ x"$confirm" = "xy" ]];then
    cur_dir=$(pwd)
    mkdir -p /opt/cita-agent
    work_dir='/opt/cita-agent'
    os=$(cat /proc/version)
    echo -e "\e[1;36msteup 1 : 操作系统检查并安装基础环境 \e[0m"
    Get_osPlatform
    echo -e "\e[1;36msteup 2 : 检查基础环境安装是否成功 \e[0m"
    Check_ENV
    echo -e "\e[1;36msteup 3 : 安装 python 环境所需软件库 \e[0m"
    Install_Python_libs
    echo -e "\e[1;36msteup 4 : 安装 cita-cli 工具 \e[0m"
    Install_cita_tool
    echo -e "\e[1;36msteup 5 : 安装 agentd 服务 \e[0m"
    Install_AgentService
    echo -e "\e[1;36msteup 6 : cita-agentd 安装完毕 \e[0m"
    END
else
    exit
fi
