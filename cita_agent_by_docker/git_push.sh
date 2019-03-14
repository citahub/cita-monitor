#!/bin/bash
#

git add *
read -p "请输入你希望提交的描述信息: \n" description
git commit -m "${description}"
git push
