# Orchestrating Workflows for GenAI Applications

## Why Orchestration Is Used

Notebooks are commonly used during development. For production, pipelines are used to provide:

- Automated code execution
- Observability of workflow runs and results
- Reliable and repeatable execution
- Failure handling and notifications

Python-based notebooks can be converted into automated pipelines.

## Apache Airflow

Apache Airflow is used in this course. It is a standard tool for programmatic workflow orchestration. It is highly extensible and tool-agnostic.

### Main Terms

- **DAG:** A workflow in which tasks and their dependencies are defined.
- **Task:** A single unit of work in a DAG.
- **Airflow UI:** An interface in which current and previous pipeline runs are displayed.
- **Scheduler:** A component through which tasks are scheduled when their dependencies are met.
- **Worker:** A component by which scheduled tasks are executed.
- **Connection:** External system credentials and connection details stored in Airflow.
- **Hook:** A Python interface through which an external system is accessed.

### Airflow Execution

1. DAG files are stored in the `dags` folder.
2. DAGs are parsed by the DAG processor.
3. Task dependencies are checked by the scheduler.
4. Ready tasks are added to a queue.
5. Tasks are executed by workers.
6. Results and task states are stored in the Airflow metadata database.
7. Workflow information is displayed in the Airflow UI.

### TaskFlow API

DAGs and tasks are defined with Python decorators:

```python
from airflow.sdk import dag, task


@dag
def example_dag():
    @task
    def first_task():
        return "data"

    @task
    def second_task(value):
        print(value)

    second_task(first_task())


example_dag()
```

When the output of one task is passed to another task, a dependency is created automatically.

## GenAI Pipelines

The following GenAI workflows can be orchestrated:

- Retrieval-Augmented Generation (RAG)
- Inference
- Batch inference
- Model training and retraining
- Fine-tuning

## Workflow Used in the Labs

The course is based on a RAG book recommendation system. The workflow is developed in the following order:

1. A RAG prototype is created in a notebook.
2. The notebook is converted into Airflow DAGs.
3. Time-based and data-aware scheduling are added.
4. Tasks are processed in parallel through dynamic task mapping.
5. Retries, trigger rules, and failure callbacks are configured.

## RAG Prototype

Book descriptions are read from text files. Each record contains a title, author, and description.

The following process is used:

1. Book data is extracted from local files.
2. Description embeddings are created with `fastembed`.
3. Embeddings and book metadata are stored in Weaviate.
4. A user query is converted into an embedding.
5. Semantic search is performed in Weaviate.
6. The closest book recommendation is returned.

The following embedding model is used:

```text
BAAI/bge-small-en-v1.5
```

## Converting the Prototype into DAGs

The notebook workflow is separated into two DAGs.

### `fetch_data`

The vector database is prepared through the following tasks:

1. The `Books` collection is created if it does not exist.
2. Book description files are listed.
3. Book data is extracted from each file.
4. Description embeddings are created.
5. Book data and embeddings are loaded into Weaviate.

### `query_data`

A book recommendation is produced through the following steps:

1. A query is received.
2. A query embedding is created.
3. A vector search is performed in Weaviate.
4. The closest book is returned.

### Weaviate Connection

Weaviate is accessed through an Airflow Connection and `WeaviateHook`:

```python
hook = WeaviateHook("my_weaviate_conn")
client = hook.get_conn()
```

Connection details are therefore kept outside the DAG code.

## Scheduling

### Time-Based Scheduling

The `fetch_data` DAG is scheduled to run every hour:

```python
@dag(
    start_date=datetime(2025, 6, 1),
    schedule="@hourly",
)
```

### Data-Aware Scheduling

An Airflow Asset is updated after embeddings are loaded:

```python
@task(outlets=[Asset("my_book_vector_data")])
```

The `query_data` DAG is triggered when this asset is updated:

```python
@dag(schedule=[Asset("my_book_vector_data")])
```

In this way, the query workflow is run after new vector data has been prepared.

### DAG Parameters

The search query is provided as a DAG parameter instead of being hardcoded:

```python
@dag(params={"query_str": "A philosophical book"})
```

The parameter is accessed from the Airflow context:

```python
query_str = context["params"]["query_str"]
```

## Dynamic Task Mapping

Originally, all book files were processed inside one task. If one file caused a failure, every file had to be processed again.

With dynamic task mapping, one task instance is created for each file:

```python
transform_book_description_files.expand(
    book_description_file=book_description_files
)
```

The following benefits are provided:

- Files are processed in parallel.
- Failures are isolated to individual files.
- The number of task instances is based on the number of input files.
- Successful file processing does not need to be repeated.

## Failure Handling

### Retries

Retries are used for temporary failures:

```python
default_args={
    "retries": 1,
    "retry_delay": duration(seconds=10),
}
```

Different retry settings can be assigned to individual tasks.

### Trigger Rules

Trigger rules define whether a task should run based on upstream task states.

```python
@task(trigger_rule="all_done")
```

With `all_done`, a task is run after all upstream tasks have finished, including failed tasks.

### Failure Callbacks

An `on_failure_callback` is executed when a task or DAG fails. Failure details can be logged or sent to a notification service.

## Pipeline Design Practices

### Atomicity

Each task should perform one specific unit of work.

### Idempotency

The same task should be executable multiple times without producing unintended changes.

### Software Development Practices

Standard software development practices should be applied to pipeline code, including clear structure, testing, logging, and version control.

## Main Course Concepts

- Notebook workflows can be converted into automated DAGs.
- Tasks are defined and connected through the TaskFlow API.
- External systems are accessed through Connections and Hooks.
- DAGs can be triggered by time schedules or data updates.
- Runtime values can be supplied through DAG parameters.
- Dynamic task mapping can be used for parallel processing.
- Retries, trigger rules, and callbacks can be used for failure handling.
