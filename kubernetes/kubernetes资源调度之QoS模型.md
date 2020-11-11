# kubernetes资源调度之QoS模型

## 一、QoS等级划分

-  **在k8s中CPU属于可压缩资源（compressible resources），当可压缩资源不足时，pod只会“饥饿”，不会退出，内存属于不可压缩资源，当不可压缩资源不足时，pod会因为oom（out-ofmemory）被内核kill掉。**

-  **而由于 Pod 可以由多个 Container 组成，所以 CPU 和内存资源的限额，是要配置在Container 的定义上的。这样，Pod 整体的资源配置，就由这些 Container 的配置值累加得到。**
- **Kubernetes 的 requests+limits 的做法，其实就是上述思路的一个简化版：用户在提交 Pod 时，可以声明一个相对较小的 requests 值供调度器使用，而 Kubernetes 真正设置给容器 Cgroups 的，则是相对较大的 limits 值。**

- **在 Kubernetes 中，不同的 requests 和 limits 的设置方式，其实会将这个 Pod 划分到不同的 QoS 级别当中，这几个级别分为：Guaranteed、Bursttable、BestEffort。**



1. 当 Pod 里的每一个 Container 都同时设置了 requests 和 limits，并且 requests 和 limits 值相等的时候，这个 Pod 就属于 Guaranteed 类别，比如以下列子：

   ```
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-web
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
       resources:
         requests:
           cpu: "100m"
           memory: "100Mi"
         limits:
           cpu: "100m"
           memory: "100Mi"
   ```

   当这个 Pod 创建之后，它的 qosClass 字段就会被 Kubernetes 自动设置为 Guaranteed。需要注意的是，当 Pod 仅设置了 limits 没有设置 requests 的时候，Kubernetes 会自动为它设置与 limits 相同的 requests 值，所以，这也属于 Guaranteed 情况。

2. 当pod不满足Guaranteed条件时，pod中至少有一个container设置了request，那么这个pod的QoS就会被列为Burstable类别，比如以下例子：

   ```
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-web
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
       resources:
         requests:
           memory: "100Mi"
         limits:
           memory: "200Mi"
   ```

3. 如果一个 Pod 既没有设置 requests，也没有设置 limits，那么它的 QoS 类别就是 BestEffort。

   ```
   apiVersion: v1
   kind: Pod
   metadata:
     name: my-web
   spec:
     containers:
     - name: nginx
       image: nginx
       ports:
       - containerPort: 80
   ```

## 当资源紧俏时，例如OOM，kubelet会根据QoS进行驱逐：

Best-Effort，最低优先级，第一个被kill；
Burstable，第二个被kill;
Guaranteed，最高优先级，最后kill。除非超过limit或者没有其他低优先级的Pod。


## 二、QoS应用场景

**QoS 划分的主要应用场景，是当宿主机资源紧张的时候，kubelet 对 Pod 进行 Eviction（即资源回收）时需要用到的。**

当 Kubernetes 所管理的宿主机上不可压缩资源短缺时，就有可能触发 Eviction。比如，可用内存（memory.available）、可用的宿主机磁盘空间（nodefs.available），以及容器运行时镜像存储空间（imagefs.available）等

Kubernetes 设置的 Eviction 的默认阈值如下所示：

memory.available<100Mi

nodefs.available<10%

nodefs.inodesFree<5%

imagefs.available<15%	

如果要修改以上阈值，可以在kubelet中这样配置：

```
kubelet --eviction-hard=imagefs.available<10%,memory.available<500Mi,nodefs.available<5%,nodefs.inodesFree<5% --eviction-soft=imagefs.available<30%,nodefs.available<10% --eviction-soft-grace-period=imagefs.available=2m,nodefs.available=2m --eviction-max-pod-grace-period=600
```





Eviction 阈值的数据来源，主要依赖于从 Cgroups 读取到的值，以及使用 cAdvisor 监控到的数据。

Eviction分为hard eviction和soft eviction这两种：

（1）hard eviction：宿主机的 Eviction 阈值达到后，立即触发eviction，就会进入 MemoryPressure 或者 DiskPressure 状态，从而避免新的 Pod 被调度到这台宿主机上，即该节点已经被打污点了。然后会挑选一些pod进行删除操作，首先是BestEffort类别的，其次是Burstable、并且是可压缩资源使用量超过request的pod，最后才是Guaranteed类别，并且是资源使用率超过limit，宿主机处于Memory Pressure状态的时候；

（2）soft eviction：允许你为 Eviction 过程设置一段“优雅时间”，比如上面例子里的 imagefs.available=2m，就意味着当 imagefs 不足的阈值达到 2 分钟之后，kubelet 才会开始 Eviction 的过程。

**QoS还有一个重要的应用场景就是：**

利用cpuset 把容器绑定到某个 CPU 的核上，减少上下文切换，提高性能，cpuset 方式，是生产环境里部署在线应用类型的 Pod 时，非常常用的一种方式。

设置方式非常简单， Pod 必须是 Guaranteed 的 QoS 类型，即request和limit相等即可

```
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        memory: "200Mi"
        cpu: "2"
      requests:
        memory: "200Mi"
        cpu: "2"
```

该 Pod 就会被绑定在 2 个独占的 CPU 核上。当然，具体是哪两个 CPU 核，是由 kubelet 为你分配的
