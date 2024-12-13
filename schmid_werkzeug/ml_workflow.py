def get_sample_batches(n_samples: int, max_bs: int) -> list:
    # Use list comprehension to generate full batches and handle the remainder
    return [max_bs] * (n_samples // max_bs) + (
        [n_samples % max_bs] if n_samples % max_bs != 0 else []
    )
