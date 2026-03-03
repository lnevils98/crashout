const object = {
    "message": {
        "model": "llama3.2",
        "created_at": "2026-03-03T13:11:44.424767505Z",
        "done": true,
        "done_reason": "stop",
        "total_duration": 8920201754,
        "load_duration": 1899518918,
        "prompt_eval_count": 32,
        "prompt_eval_duration": 1706756959,
        "eval_count": 8,
        "eval_duration": 5308895837,
        "message": {
            "role": "assistant",
            "content": "The capital of France is Paris.",
            "thinking": null,
            "images": null,
            "tool_name": null,
            "tool_calls": null
        },
        "logprobs": null
    }
};

console.log(object.message.message.content); // Output: The capital of France is Paris.