

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/AttributesInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using AttributesInterface = ::smoke::AttributesInterface;

class AttributesInterfaceTrampoline : public AttributesInterface {
public:
    using AttributesInterface::AttributesInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<AttributesInterface> m_impl;

    void very_fun(
            const ::std::string& param ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->very_fun(param);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, AttributesInterface, very_fun, param);
    }
    ::std::string get_prop() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_prop();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, AttributesInterface, get_prop);
    }
    void set_prop(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_prop(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, AttributesInterface, set_prop, value);
    }
};

void register_smoke_AttributesInterface(py::module_& module) {
    py::class_<AttributesInterface, std::shared_ptr<AttributesInterface>, AttributesInterfaceTrampoline>(module, "AttributesInterface")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<AttributesInterface> native) {
            auto self = std::make_shared<AttributesInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def_property("prop", [](const AttributesInterface& self) {
            return self.get_prop();
        }, [](AttributesInterface& self, const ::std::string& value) {
            self.set_prop(value);
        })
        ;
}

