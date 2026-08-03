

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/fooListener.h"
#include "string"

using fooListener = ::smoke::fooListener;

class QuxListenerTrampoline : public fooListener {
public:
    using fooListener::fooListener;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<fooListener> m_impl;

    void FooMethod(
            const ::std::string& qux_parameter ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->FooMethod(qux_parameter);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, fooListener, FooMethod, qux_parameter);
    }
};



void register_smoke_QuxListener(py::module_& module) {
auto cls_QuxListener = py::class_<fooListener, std::shared_ptr<fooListener>, QuxListenerTrampoline>(module, "smoke_QuxListener")
        .def("__gluecodium_id__", [](const fooListener& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<fooListener> native) {
            auto self = std::make_shared<QuxListenerTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("qux_method", [](fooListener& self, const ::std::string& qux_parameter) {
            return self.FooMethod(qux_parameter);
        }, py::arg("qux_parameter"))
        ;


}
