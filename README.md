# Storing Work-Items in a database

Utilizing Robocorp's Control Room and work-items is a powerful solution for getting work done quickly. But for security or other reasons if you do not want to store the work-item data in Control Room you have the option to store them in a local database that your self-hosted worker can access.

**This tutorial provides you the Producer Consumer template for storing work-items on a local database**

This template leverages the new Python open-source framework [robo](https://github.com/robocorp/robo), and [libraries](https://github.com/robocorp/robo#libraries) from the same project. It provides a template for storing data locally. In this case, we are focusing on these highlights:

- Producer will store work-items in the database while storing a unique ID in Control Room for retrieval
- Consumer will get the unique ID from Control Room the query the database for the work-item data
- This example uses MySql but can easily be transitioned for any database following the API specification 2.0

## What you'll need

To complete this tutorial yourself, you'll need the following:

- A MySql database
- A Control Room account

## Steps to reproduce

Once all is installed, do the following (if you follow the names exactly, the code will work without changes):

1. You will need a working installation of MySql database

2. Create a table named `workitems` with the following fields:
  - `id`  (type: `int`)
  - `name` (type: `varchar(256)`)
  - `zip` (type: `varchar(256)`)
  - `items` (type: `varchar(256)`)

3. Link your development environment to the Robocorp Cloud and your workspace.

4. Create one [Robocorp Vault](https://robocorp.com/docs/development-guide/variables-and-secrets/vault) items that house your secrets:
  - Name it `mysql_data` which will contain the following items needed to connect to your database
  - - `database` that contains the name of the database you are connecting to
  - - `username` user that can access the database
  - - `password` user password
  - - `location` IP Address of the database you are connecting to


## Code explanation

### 1. Set up your dependencies in the [conda.yaml](conda.yaml) file and declare runnables

Because we are using MySql you have to add the `PyMySQL` pip package to the conda.yaml file.

```yaml
dependencies:
  - python=3.10.12
  - pip=23.2.1
  - robocorp-truststore=0.8.0
  - pip:
    - rpaframework==27.7.0
    - robocorp==1.2.4
    - robocorp-browser==2.2.1
    - PyMySQL==1.1.0
```

### 2. Changing the table

While in step 2 in the **Steps to Reproduce** section called for a table named `workitems` you can easily change the name, just make sure to change the global variable name in the code as well.

```python
   TABLE = "workitems"
```

## Going cloud ☁️

Now that all runs locally, time to go production-grade. In this section we'll do the following things: upload the project to the Control Room, create a process out of it, set up an email trigger and test it.

### 1. Deploy code to Control Room

While you can upload your project directly from VS Code to the Control Room (Command Palette - Robocorp: Upload Robot to the Control Room), the recommended way is to do it via the git repo. You may fork this repo to your own, or simply just use our example repo directly.

It's easy: Tasks tab under your Workspace, Add Task Package, give it a name, and paste the link to the repo. Done.

![create-tasks](https://github.com/robocorp/example-timescale-vector-loader/assets/40179958/95cf3b7f-6604-4f68-8455-bbef780ce954)

### 2. Create a Process

Next up, you'll need to create a Process. Tasks are reusable components that you can use to build sequences of actions. When creating a Process you'll map your chosen Tasks with the Worker runtimes.

Follow the UI again, as the video below shows. Processes, Create a new Process and add your details. Just note the video below is for a different process, so you should name your own process accordingly.

Once that's done, you'll have an opportunity to either set the scheduling, or create an email trigger. We'll choose the latter. In the last step, you can create alerts and callbacks to Slack, Email and as Webhook calls. In this example we set a Slack notification for both successfull and unsuccessful runs.

![create-process](https://github.com/robocorp/example-timescale-vector-loader/assets/40179958/32a67f01-05c6-4065-a6de-e67fe3a86e92)

### 3. Run it manually

Once the Proces is created, time to run it! Hit the Run Process button and choose Run with Input Data, and give a file as an input. Once the run starts, you'll see the producer creating new rows in your local database and then the consumer will use them! 🤞

<img width="1279" alt="run-process" src="https://github.com/robocorp/example-timescale-vector-loader/assets/40179958/fecb6904-4f5e-427a-aa72-140044bb7f00">

**Tip:** open the Process run for detailed log on the execution.

