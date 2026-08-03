

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
#include "smoke/ParentClass.h"
#include "string"

using ParentClass = ::smoke::ParentClass;

class ParentClassTrampoline : public ParentClass {
public:
    using ParentClass::ParentClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentClass> m_impl;

    void root_method(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->root_method();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, root_method);
    }
    ::std::string get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ParentClass, get_root_property);
    }
    void set_root_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClass, set_root_property, value);
    }
};



void register_smoke_ParentClass(py::module_& module) {
auto cls_ParentClass = py::class_<ParentClass, std::shared_ptr<ParentClass>, ParentClassTrampoline>(module, "smoke_ParentClass")
        .def("__gluecodium_id__", [](const ParentClass& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentClass> native) {
            auto self = std::make_shared<ParentClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("root_method", &ParentClass::root_method)
        .def_property("root_property", py::overload_cast<>(&ParentClass::get_root_property, py::const_), py::overload_cast<const ::std::string&>(&ParentClass::set_root_property))
        ;


}
