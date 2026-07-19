

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ListenerInterface.h"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ListenerInterface = ::smoke::ListenerInterface;

class ListenerInterfaceTrampoline : public ListenerInterface {
public:
    using ListenerInterface::ListenerInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ListenerInterface> m_impl;

    void notify(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->notify();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerInterface, notify);
    }
};

void register_ListenerInterface(py::module_& module) {
    py::class_<ListenerInterface, std::shared_ptr<ListenerInterface>, ListenerInterfaceTrampoline>(module, "ListenerInterface")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ListenerInterface> native) {
            auto self = std::make_shared<ListenerInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("notify", [](ListenerInterface& self) {
            return self.notify();
        })

        ;
}

