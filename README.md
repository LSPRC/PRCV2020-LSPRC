### PRCV2020-LSPRC
该工程为“[PRCV2020大规模行人检索竞赛（LSPRC）](https://lsprc.github.io/)”提供必要的基础代码，包括以下内容。

#### 算法模块接口定义

* python接口 - interfaces/isee_interfaces.py
* c++接口 - interfaces/isee_interfaces.h
* 说明：
  - 模型调用代码支持C/C++和python两种语言，请务必基于提供的接口设计，并给出调用样例。
  - 支持Pytorch、TensorFlow(Keras)、Mxnet深度学习框架。
  - 使用python请指明requirements及版本要求（仅支持python3）。
  - C/C++代码请确保无内存泄漏问题，建议使用valgrind检查。
  - 仅支持linux系统。
 
#### 性能评估代码

* PR-A-RAP - evaluate_PR_A.py
* PR-ID-RAP - evaluate_PR_ID.py

#### 数据加载代码

* PR-A - load_rap_attributes_data_mat.py
* PR-ID - load_rap_reid_data_mat.py
