[toc]
# 1、使用NFS提供静态PV、动态PV
## （1）安装nfs
**NFS Server 环境为：**
 - IP地址：192.168.135.128
 - 存储目录：/nfs/data

**nfs server安装：**

    yum install nfs-utils rpcbind -y
    vim /etc/exports
    /nfs/data 192.168.135.0/24(rw)
    
    mkdir /nfs/data
    systemctl start rpcbind
    systemctl enable rpcbind
    systemctl start nfs
    systemctl enable nfs
    showmount -e  #查看是否可挂

**nfs client（k8s节点）:**  

    yum install nfs-utils -y

## （2）静态卷
**首先创建pv卷**  

    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: test-pv
      labels:
        pv: test-pv
    spec:
      capacity:
        storage: 5Gi
      accessModes:
        - ReadWriteOnce
      persistentVolumeReclaimPolicy: Recycle
      storageClassName: nfs
      nfs:
        path: /nfs/data
        server: 192.168.135.128    


    kubectl apply -f test_pv.yaml
    
    kubectl get pv #可以看到pv已经创建成功，处于available状态，可被PVC申请



**然后创建PVC： **  

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: nfs
  selector:
    matchLabels:
      pv: test-pv
```



**PVC创建成功：PVC bound状态：** 

```
kubectl apply -f test-pvc.yaml 
kubectl get pvc
```



## （3）动态卷

**NFS Provisioner** 是一个自动配置卷程序，它使用现有的和已配置的 NFS 服务器来支持通过持久卷声明动态配置 Kubernetes 持久卷。

基于StorageClass的动态存储供应整体过程如下图所示：

![img](C:\Users\ops\AppData\Local\YNote\data\m18677544058@163.com\dde0753958b3469f8700414e7c5721b1\clipboard.png)

1）集群管理员预先创建存储类（StorageClass）；

2）用户创建使用存储类的持久化存储声明(PVC：PersistentVolumeClaim)；

3）存储持久化声明通知系统，它需要一个持久化存储(PV: PersistentVolume)；

4）系统读取存储类的信息；

5）系统基于存储类的信息，在后台自动创建PVC需要的PV；

6）用户创建一个使用PVC的Pod；

7）Pod中的应用通过PVC进行数据的持久化；

8）而PVC使用PV进行数据的最终持久化处理。

nfs本身不像ceph或者glusterfs一样提供动态存储功能，所以需要安装nfs-client-provisioner：

这里使用helm安装：

```
helm install stable/nfs-client-provisioner --set nfs.server=192.168.135.128 --set nfs.path=/nfs/data
```

安装完可以看到nfs-client-provisioner这个pod已经起来了



```
helm list
```

![img](C:\Users\ops\AppData\Local\YNote\data\m18677544058@163.com\f54beb5003dc4283b97b4543365d3c78\clipboard.png)

测试：

1.可以创建一个新的存储类（storageclass），也可以使用默认创建的nfs-client这个storageclass

这里我创建一个叫my-storageclass的存储类：

注意provisioner：

```
[root@k8s-master ~]# cat storageclass.yaml 

apiVersion: storage.k8s.io/v1

kind: StorageClass

metadata:

  name: my-storageclass

provisioner: cluster.local/nfs-client-provisioner-1583481365
```

kubectl apply -f storageclass.yaml

kubectl get sc 可以看到my-storageclass

注意：这里的provisioner需要填写deployment中定义的env的PROVISIONER_NAME

可通过kubectl edit pod nfs-client-provisioner-1583481365-754f8f8496-gbb7x查看



2.创建pvc

```
[root@k8s-master ~]# cat test-pvc.yaml 

apiVersion: v1

kind: PersistentVolumeClaim

metadata:

  name: test-pvc2

  annotations:

​    volume.beta.kubernetes.io/storage-class: "my-storageclass"

spec:

  accessModes:

  - ReadWriteOnce

  resources:

​   requests:

​     storage: 1Gi
```

看看这个PVC是否是bound状态，如果不是，可以kubectl describe pvc pvcname排错，无法绑定成功多半是目录权限的问题



# 2、emptydir与hostpath

- emptydir是把pod的目录挂载到宿主机，其生命周期与pod一致，pod删除或重启，内容会丢失，适合把日志文件挂载出来进行收集，缺省情况下，EmptyDir 是使用主机磁盘进行存储的，也可以设置emptyDir.medium 字段的值为Memory，来提高运行速度，但是这种设置，对该卷的占用会消耗容器的内存份额。慎用！！！

​              

- hostpath是把宿主机的目录或文件挂载到容器，多用于比如以下的时区或者其他配置文件挂载场景

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx          
        ports:
        - containerPort: 80
        volumeMounts:
        - name: host-time
          mountPath: /etc/localtime
        - name: logs
          mountPath: /var/log/nginx/

      volumes:
      - name: host-time
        hostPath:
          path: /etc/localtime
      - name: logs
        emptyDir: {}
```

**emptydir:**

kubectl get pods -o wide 查看容器落在哪个node上



到pod所在的node上查看



可以看到挂载所在的目录会落在/var/lib/kubelet/pods/xxx/volumes/kubernetes.io~empty-dir/lvolume-name/路径上
