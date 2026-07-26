

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
#include "smoke/SimpleInterface.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using SimpleInterface = ::smoke::SimpleInterface;

class SimpleInterfaceTrampoline : public SimpleInterface {
public:
    using SimpleInterface::SimpleInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<SimpleInterface> m_impl;

    ::std::string get_string_value(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_string_value();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, SimpleInterface, get_string_value);
    }
    ::std::shared_ptr< ::smoke::SimpleInterface > use_simple_interface(
            const ::std::shared_ptr< ::smoke::SimpleInterface >& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->use_simple_interface(input);
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::SimpleInterface >, SimpleInterface, use_simple_interface, input);
    }
};

void register_smoke_SimpleInterface(py::module_& module) {
    py::class_<SimpleInterface, std::shared_ptr<SimpleInterface>, SimpleInterfaceTrampoline>(module, "smoke_SimpleInterface")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<SimpleInterface> native) {
            auto self = std::make_shared<SimpleInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("get_string_value", [](SimpleInterface& self) {
            return self.get_string_value();
        })
        .def("use_simple_interface", [](SimpleInterface& self, const ::std::shared_ptr< ::smoke::SimpleInterface >& input) {
            return self.use_simple_interface(input);
        }, py::arg("input"))
        ;
}

