# Runlet_runners_py

**Runlet_runners_py** is a system for test students code solutions. It provides interface to retrieve data for running code tests and returning result data.

---

- [Install](#️-install)
- [Quickstart](#-quickstart)
- [Usage](#-usage)
- [Stack](#-stack)

---

## ⚙️ Install


Before running the app, set the following environment variables using .env file in build/prod. Examples of variables are in `build/prod/.example.env`.

---

To start:

```bash
make runlet.runners.prod.build.start
```
---

## 📦 Usage

When you started app, runner gateway starts listen **test_solutions** queue in RabbitMQ, that should be started at gateway start moment. The main service([Runlet_py](https://github.com/TheAppleKingy/Runlet_py)) will send messages using specified format to broker and this app will get needed data to test students code. Using **celery** runner gateway starts(and build if need) docker container builded from image that resolves using given data. At this moment service support running code of following programming languages:
- Python
- Go
- JavaScript
- C#
- C++

So flexible system was created to add runners for new programming languages. Main options should be specified in config. Must to define relative path to config in **.env**.

---
## 📌 Config

The center of all this app is a config. In this repository config represented by **.yaml** file placed in root. So next will be explained **config.yaml** content.

### runners

**runners** is a section containing data of runners containers for current available programming languages.

- **image** - docker image with desired programming language.
- **mem_limit** - memory limitation for running runner container
- **cpu_cores** - CPU limitation
- **env** - environment variables that should be provided into running runner container. Optional field
- **compile_args** - args of command that will compile binary from source code. If programming language is interpreted specify '[]'. This field required!
- **run_args** - args for command that will run code. If programming language is compiled provide only plaeholder for bin files. Also requred field
- **run_timeout** - timeout for run of one test(one input)

So in **compile_args** and **run_args** you can see "{bin}" and "{src}". These are placeholders for source code path and path to compiled binary. If you want to change placeholders dont remember change also **src_placeholder** and **bin_placeholder** in config.yaml. These points help runner to know which placeholders need to find in provided compile and run args to replace by source code path and compiled binary path. Also remember: when you add or delete supporting languages check for `gateway.domain.types.CodeName` because it using to setup configs when app starts.

---
Next config points after **running** section:

- **context_path** - context path for runners images
- **dockerfiles_path** - path to dockerfiles for runner and programming language
- **runner_dockerfile_name** - name of dockerfile where runner binary will be placed.
- **shared_dockerfile_name** - name of dockerfile with compiling binary that will run students code providing inputs from given data. Shared image
- **runner_image_name_pattern** - pattern for name of building image for runners. Inserting short code name(see in **runners** section of config)
- **shared_image_name** - standart name of shared image.
- **volume_name** - name of named volume that will be used for providing code run data to runners containers. Be careful on **build/prod/compose.yaml!!!**
- **runner_mountpoint** - place of mounting named volume in runner container.
- **gateway_source_data_dir** - dir where gateway will create temp files with code run data. Named volume should be mounted here in **build/prod/compose.yaml!!! When code will be retrieved for testing runner can get code run data only from this volume mountpoint!!!**
- **tmpfs** - directory that will be as tmpfs parameter when runner container will be started. Need to write files with source code to provide to interpretators or compile and run binary. The only directory with these permissions.

---

## 🧰 Stack

- **FastAPI** – web framework  
- **PostgreSQL** – database  
- **SQLAlchemy** – ORM  
- **Alembic** – DB migrations  
- **Docker** – containerization
- **RabbitMQ**, **[ploomby](https://pypi.org/project/ploomby/)** - messaging
- **Golang** - code runner implementation