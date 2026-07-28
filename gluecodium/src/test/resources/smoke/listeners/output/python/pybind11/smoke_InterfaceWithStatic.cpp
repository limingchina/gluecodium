

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
#include "smoke/InterfaceWithStatic.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InterfaceWithStatic = ::smoke::InterfaceWithStatic;

class InterfaceWithStaticTrampoline : public InterfaceWithStatic {
public:
    using InterfaceWithStatic::InterfaceWithStatic;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InterfaceWithStatic> m_impl;

    ::std::string regular_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->regular_function();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InterfaceWithStatic, regular_function);
    }
    ::std::string get_regular_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_regular_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InterfaceWithStatic, get_regular_property);
    }
    void set_regular_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_regular_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, InterfaceWithStatic, set_regular_property, value);
    }
};

void register_smoke_InterfaceWithStatic(py::module_& module) {
    py::class_<InterfaceWithStatic, std::shared_ptr<InterfaceWithStatic>, InterfaceWithStaticTrampoline>(module, "smoke_InterfaceWithStatic")
        .def("__gluecodium_id__", [](const InterfaceWithStatic& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InterfaceWithStatic> native) {
            auto self = std::make_shared<InterfaceWithStaticTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("regular_function", [](InterfaceWithStatic& self) {
            return self.regular_function();
        })
        .def_static("static_function", &InterfaceWithStatic::static_function)
        .def_property("regular_property", [](const InterfaceWithStatic& self) {
            return self.get_regular_property();
        }, [](InterfaceWithStatic& self, const ::std::string& value) {
            self.set_regular_property(value);
        })
        .def_static("static_property", &InterfaceWithStatic::get_static_property)
        .def_static("static_property_set", &InterfaceWithStatic::set_static_property)
        ;
}

