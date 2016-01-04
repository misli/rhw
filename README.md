Red Hack Week Management Application
====================================

Install dependencies
--------------------

```shell
dnf install $(<requires)
```

Install rhw
-----------

```shell
python3 setup.py install
```

Post installation steps
-----------------------

```shell
rhw-manage collectstatic --noinput
rhw-manage migrate
rhw-manage postinst
for service in {httpd,memcached,sendmail}.service; do
    systemctl enable $service;
    systemctl start $service;
done
```

