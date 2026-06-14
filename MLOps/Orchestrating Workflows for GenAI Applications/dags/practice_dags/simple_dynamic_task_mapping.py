from airflow.sdk import dag, task


@dag
def simple_mapping():

    @task
    def get_numbers():
        import random

        return [_ for _ in range(random.randint(0, 3))]  # [0,1,2]

    _get_numbers = get_numbers()

    @task
    def mapped_task_one(my_constant_arg: int, my_changing_arg: int):
        return my_constant_arg + my_changing_arg

    _mapped_task_one = mapped_task_one.partial(my_constant_arg=10).expand(
        my_changing_arg=_get_numbers
    )

    @task
    def mapped_task_two(my_cookie_number: int):
        print(f"There are {my_cookie_number} cookies in the jar!")

    mapped_task_two.expand(my_cookie_number=_mapped_task_one)


simple_mapping()
