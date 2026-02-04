___

> Guía comandos/acciones a realizar para ejecutar un SAST con SonarQube

```bash
$ sudo apt update && sudo apt install -y openjdk-17-jdk
```

```bash
$ wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-6.2.1.4610-linux-x64.zip
```

```bash
$ unzip sonar-scanner-cli-6.2.1.4610-linux-x64.zip
```

```bash
$ sudo mv sonar-scanner-6.2.1.4610-linux-x64  /opt/
```

```bash
$ echo 'export PATH=$PATH:/opt/sonar-scanner-6.2.1.4610-linux-x64/bin' >> ~/.bashrc
```

```bash
$ source ~/.bashrc
```

```bash
$ sonar-scanner -v
```

```bash
$ git clone https://github.com/fmoha04/SneakerShop.git
```

```bash
$ docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest
```

```bash
$ firefox localhost:9000 # seguir pasos que se muestran en la carpeta assets
```

```bash
$ cd SneakerShop/
```

```bash
$ sonar-scanner \
  -Dsonar.projectKey=SneakerShop_GrupoA7 \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.token=<token_sonar_qube>
```

___
