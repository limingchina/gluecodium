

// Wrapper cache: preserves referential equality across the C++ <-> Python boundary.
//
// When C++ returns a pointer/reference to an object that already has a Python wrapper, the same
// wrapper instance must be returned so that identity (``is``) is preserved. This mirrors the
// behaviour of Gluecodium's other language bindings (Dart InstanceCache, Swift WrapperCache).
//
// The cache is keyed on the C++ instance pointer. A Python wrapper is created lazily through the
// supplied factory and kept alive by the cache (so long as the C++ object is alive and the cache
// entry is not explicitly removed).

#pragma once

#include <pybind11/pybind11.h>

#include <cstddef>
#include <functional>
#include <mutex>
#include <unordered_map>

namespace gluecodium::python {

class WrapperCache {
public:
    // Return the existing Python wrapper for the given C++ pointer, or create one with
    // `creator` and store it. `cpp_ptr` must be a stable identity for the C++ instance
    // (typically the `this` pointer of the held `std::shared_ptr` target).
    pybind11::object get_or_create(const void* cpp_ptr, const std::function<pybind11::object()>& creator) {
        if (cpp_ptr == nullptr) {
            return pybind11::object();
        }
        std::lock_guard<std::mutex> lock(mutex_);
        auto it = cache_.find(cpp_ptr);
        if (it != cache_.end()) {
            return it->second;
        }
        pybind11::object obj = creator();
        cache_[cpp_ptr] = obj;
        return obj;
    }

    // Remove the cached wrapper for the given C++ pointer (call when the C++ object is destroyed).
    void remove(const void* cpp_ptr) {
        if (cpp_ptr == nullptr) {
            return;
        }
        std::lock_guard<std::mutex> lock(mutex_);
        cache_.erase(cpp_ptr);
    }

    static WrapperCache& instance() {
        static WrapperCache cache;
        return cache;
    }

private:
    WrapperCache() = default;
    WrapperCache(const WrapperCache&) = delete;
    WrapperCache& operator=(const WrapperCache&) = delete;

    std::mutex mutex_;
    std::unordered_map<const void*, pybind11::object> cache_;
};

}  // namespace gluecodium::python
