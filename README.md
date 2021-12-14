## 目標
+ 設計一套系統，根據數據集的 features 生成合理的 labels。
+ 使用者的 input 能形成 feedback，幫助改善系統的準確度

## 技术栈
目前这个系统分为三个部分
+ 前端：采用 Vue 2 + Vuex + Vuetify
+ API：以 Flask 为主
+ 数据库：Mongodb
数据库运行在云服务器上的 docker，前端和 API 暂时部署在本地，待系统更成熟后会区分生产环境（在云服务器上运行）和开发环境（在本地运行）。

### 前端
按 npm / yarn 的方法安装好依赖后，以下列指令运行
```
cd ./panel && yarn serve
```

### API
安装好所需依赖后，以 python3 运行 `./api/api_v4.py`

### 数据库
目前服务器尚未开放端口，需要先使用 ssh 映射远程 27017 端口至本地 27018 端口
```
ssh -L 27018:localhost:27017 -i <key path> root@<server ip>
```
然后连接 `mongo://localhost:27018`。