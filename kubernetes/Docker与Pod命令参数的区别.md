# Docker的ENTRYPOINT和CMD与Pod和command、args的区别

## 描述

| **描述**       | **Docker字段名称** | **Kubernetes字段名称** |
| -------------- | ------------------ | ---------------------- |
| 执行的命令     | ENTRYPOINT         | command                |
| 传给命令的参数 | CMD                | args                   |



## 用法

- Docker中的CMD有三种方式：

```
CMD <shell 命令> 
CMD ["executable(可执行文件或命令)","param1","param2",...] 
CMD ["param1","param2",...]  # 该写法是为 ENTRYPOINT 指令指定的程序提供默认参数
```

推荐使用第二种格式，执行过程比较明确。第一种格式实际上在运行的过程中也会自动转换成第二种格式运行，并且默认可执行文件是 sh，以”/bin/sh -c”的方法执行的命令



- Docker中的ENTRYPOINT 指令有两种使用方式:

```
ENTRYPOINT ["executable(可执行文件或命令)", "param1", "param2"]  // 这是 exec 模式的写法，注意需要使用双引号。
ENTRYPOINT command param1 param2          // 这是 shell 模式的写法。
```



- k8s的args与command用法：


```
    command: ["cmd",]
    或    
    command: ["cmd","param1"]
    或
    command: ["cmd"]
    args: ["param1"]
    或：
    command: ["/bin/sh"]
    args: ["-c","while true;do echo hello;sleep 1;done"]
    或：
    command: ["/bin/sh","-c","while true;do echo hello;sleep 1;done"]
    或：
    command：
    - sh
    - -c
    - "cmd"
```



## 区别

| **Docker镜像ENTRYPOINT** | **Docker镜像CMD** | **Pod command** | **Pod args** | **命令执行**    |
| ------------------------ | ----------------- | --------------- | ------------ | --------------- |
| p1                       | cmd1 param1       | not set         | not set      | p1 cmd1 param1  |
| p1                       | cmd1 param1       | p2              | not set      | p2              |
| p1                       | cmd1 param1       | not set         | cmd2 param2  | p1  cmd2 param2 |
| p1                       | cmd1 param1       | p2              | cmd2 param2  | p2 cmd2 param2  |

上述表格分为四个应用场景，其中docker镜像的Entrypoint和cmd参数都设置了的情况下：

- pod中没有设置command和args，那么使用的是docker镜像配置的命令和参数
- pod中只设置了command，没有args，那么就只执行pod的command而不带任何参数
- pod中只设置了args，没有command，那么就执行容器ENTRYPOINT+pod的args参数
- pod中command和args都设置了的情况下，那么就执行command+args

**通俗来讲就是，pod中的命令优先级高于docker镜像的命令，pod的参数优先级高于docker镜像的优先级，docker镜像的参数无法传给pod命令，pod的参数可以传给docker镜像中的命令**