

## CLI

Based on: https://docs.transmogrif.ai/en/stable/examples/Bootstrap-Your-First-Project.html

```sh
git clone -b 0.7.0 https://github.com/salesforce/TransmogrifAI.git 
cd ./TransmogrifAI
./gradlew cli:shadowJar
java -cp cli/build/libs/transmogrifai-0.7.0-all.jar com.salesforce.op.cli.CLI
```

