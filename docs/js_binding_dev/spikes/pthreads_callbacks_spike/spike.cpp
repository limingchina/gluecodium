#include <emscripten/bind.h>

#include <exception>
#include <string>
#include <thread>

namespace {

emscripten::val invoke_from_worker(emscripten::val callback) {
    std::string result;
    std::string error;
    std::thread worker([callback = std::move(callback), &result, &error]() mutable {
        try {
            result = callback.call<std::string>("call", callback, std::string("worker"));
        } catch (const std::exception& exception) {
            error = exception.what();
        }
    });
    worker.join();

    auto response = emscripten::val::object();
    if (error.empty()) {
        response.set("value", result);
    } else {
        response.set("error", error);
    }
    return response;
}

}  // namespace

EMSCRIPTEN_BINDINGS(pthreads_callbacks_spike) {
    emscripten::function("invokeFromWorker", &invoke_from_worker);
}