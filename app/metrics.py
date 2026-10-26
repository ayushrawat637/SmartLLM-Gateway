
metrics = {
    "cache_hits": 0,
    "cache_misses": 0,
    "lightweight_model_requests": 0,
    "advanced_model_requests": 0,
    "fallback_events": 0
}


def increment_metric(name: str) -> None:
    if name not in metrics:
        raise ValueError(f"Unknown metric: {name}")

    metrics[name] += 1


def get_metrics() -> dict:
    return metrics.copy()
