#include <emscripten/bind.h>
#include <emscripten/threading.h>

#include <exception>
#include <memory>
#include <string>
#include <thread>

namespace {

struct CallbackState {
    emscripten::val callback;
    emscripten::val resolve;
    emscripten::val reject;
    std::string result;
    std::string error;

    CallbackState(emscripten::val callback, emscripten::val resolve, emscripten::val reject)
        : callback(std::move(callback)), resolve(std::move(resolve)), reject(std::move(reject)) {}
};

void invoke_and_settle_on_runtime_thread(void* argument) {
    std::unique_ptr<CallbackState> state(static_cast<CallbackState*>(argument));
    try {
        const auto callbackResult = state->callback.call<emscripten::val>(
            "call", state->callback, std::string("worker"));
        if (callbackResult["ok"].as<bool>()) {
            state->result = callbackResult["value"].as<std::string>();
            state->resolve.call<void>("call", state->resolve, state->result);
        } else {
            state->error = callbackResult["error"].as<std::string>();
            state->reject.call<void>("call", state->reject, state->error);
        }
    } catch (const std::exception& exception) {
        state->reject.call<void>("call", state->reject, std::string(exception.what()));
    }
}

void start_worker_proxy(CallbackState* state) {
    emscripten_async_run_in_main_runtime_thread(EM_FUNC_SIG_VI, invoke_and_settle_on_runtime_thread, state);
}

void invoke_from_worker_async(emscripten::val callback, emscripten::val resolve, emscripten::val reject) {
    auto state = std::make_unique<CallbackState>(std::move(callback), std::move(resolve), std::move(reject));
    std::thread worker([state = state.release()] {
        start_worker_proxy(state);
    });
    worker.detach();
}

void pump_runtime_queue() {
    emscripten_current_thread_process_queued_calls();
}

}  // namespace

EMSCRIPTEN_BINDINGS(pthreads_callbacks_spike) {
    emscripten::function("invokeFromWorkerAsync", &invoke_from_worker_async);
    emscripten::function("pumpRuntimeQueue", &pump_runtime_queue);
}