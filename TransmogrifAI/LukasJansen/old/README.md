## Manueller Start

There was a quite annoying problem with the --packages Option provided jars not being loaded on the driver, now its fixed by starting it twice (first start downloads jars with Maven).

``` sh
mkdir resdir
sudo chown 1001:0 resdir
docker-compose up -d --build
sleep 60
docker-compose down
sudo cat ./resdir/run.log
```