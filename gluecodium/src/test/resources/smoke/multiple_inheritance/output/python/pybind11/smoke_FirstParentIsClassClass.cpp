

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
#include "smoke/FirstParentIsClassClass.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsClassClass = ::smoke::FirstParentIsClassClass;

class FirstParentIsClassClassTrampoline : public FirstParentIsClassClass {
public:
    using FirstParentIsClassClass::FirstParentIsClassClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FirstParentIsClassClass> m_impl;

    void child_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, child_function);
    }
    ::std::string get_child_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_child_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsClassClass, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_child_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, set_child_property, value);
    }
    void parent_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, parent_function);
    }
    void parent_function_one(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, parent_function_one);
    }
    ::std::string get_parent_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsClassClass, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, set_parent_property, value);
    }
    ::std::string get_parent_property_one() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsClassClass, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsClassClass, set_parent_property_one, value);
    }
};

void register_smoke_FirstParentIsClassClass(py::module_& module) {
    py::class_<FirstParentIsClassClass, ::smoke::ParentClass, ::smoke::ParentNarrowOne, std::shared_ptr<FirstParentIsClassClass>, FirstParentIsClassClassTrampoline>(module, "smoke_FirstParentIsClassClass", py::multiple_inheritance())
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<FirstParentIsClassClass> native) {
            auto self = std::make_shared<FirstParentIsClassClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_function", &FirstParentIsClassClass::child_function)
        .def_property("child_property", py::overload_cast<>(&FirstParentIsClassClass::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsClassClass::set_child_property))
        .def("parent_function", &FirstParentIsClassClass::parent_function)
        .def("parent_function_one", [](FirstParentIsClassClass& self) {
            return self.parent_function_one();
        })
        .def_property("parent_property", py::overload_cast<>(&FirstParentIsClassClass::get_parent_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsClassClass::set_parent_property))
        .def_property("parent_property_one", [](const FirstParentIsClassClass& self) {
            return self.get_parent_property_one();
        }, [](FirstParentIsClassClass& self, const ::std::string& value) {
            self.set_parent_property_one(value);
        })
        ;
}

