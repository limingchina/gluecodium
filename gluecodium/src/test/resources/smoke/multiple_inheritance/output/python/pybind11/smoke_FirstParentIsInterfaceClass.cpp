

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "another/SomeCoolClassType.h"
#include "smoke/FirstParentIsInterfaceClass.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsInterfaceClass = ::smoke::FirstParentIsInterfaceClass;

class FirstParentIsInterfaceClassTrampoline : public FirstParentIsInterfaceClass {
public:
    using FirstParentIsInterfaceClass::FirstParentIsInterfaceClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FirstParentIsInterfaceClass> m_impl;

    void child_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, child_function);
    }
    ::std::string get_child_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_child_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceClass, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_child_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, set_child_property, value);
    }
    void parent_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, parent_function);
    }
    void some_function_that_uses_type_from_another_package(
            const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->some_function_that_uses_type_from_another_package(some_param);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, some_function_that_uses_type_from_another_package, some_param);
    }
    void parent_function_one(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, parent_function_one);
    }
    ::std::string get_parent_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceClass, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, set_parent_property, value);
    }
    ::std::string get_parent_property_one() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceClass, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceClass, set_parent_property_one, value);
    }
};

void register_FirstParentIsInterfaceClass(py::module_& module) {
    py::class_<FirstParentIsInterfaceClass, std::shared_ptr<FirstParentIsInterfaceClass>, FirstParentIsInterfaceClassTrampoline>(module, "FirstParentIsInterfaceClass")
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<FirstParentIsInterfaceClass> native) {
            auto self = std::make_shared<FirstParentIsInterfaceClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_function", &FirstParentIsInterfaceClass::child_function)

        .def_property("child_property", py::overload_cast<>(&FirstParentIsInterfaceClass::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsInterfaceClass::set_child_property))
        ;
}

