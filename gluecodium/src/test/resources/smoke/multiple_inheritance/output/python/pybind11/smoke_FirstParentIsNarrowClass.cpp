

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FirstParentIsNarrowClass.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsNarrowClass = ::smoke::FirstParentIsNarrowClass;

class FirstParentIsNarrowClassTrampoline : public FirstParentIsNarrowClass {
public:
    using FirstParentIsNarrowClass::FirstParentIsNarrowClass;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FirstParentIsNarrowClass> m_impl;

    void child_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowClass, child_function);
    }
    ::std::string get_child_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_child_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsNarrowClass, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_child_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowClass, set_child_property, value);
    }
    void parent_function_one(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowClass, parent_function_one);
    }
    void parent_function_two(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_two();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowClass, parent_function_two);
    }
    ::std::string get_parent_property_one() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsNarrowClass, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowClass, set_parent_property_one, value);
    }
    ::std::string get_parent_property_two() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_two();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsNarrowClass, get_parent_property_two);
    }
    void set_parent_property_two(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_two(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowClass, set_parent_property_two, value);
    }
};

void register_FirstParentIsNarrowClass(py::module_& module) {
    py::class_<FirstParentIsNarrowClass, ::smoke::ParentNarrowOne, ::smoke::ParentNarrowTwo, std::shared_ptr<FirstParentIsNarrowClass>, FirstParentIsNarrowClassTrampoline>(module, "FirstParentIsNarrowClass", py::multiple_inheritance())
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<FirstParentIsNarrowClass> native) {
            auto self = std::make_shared<FirstParentIsNarrowClassTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_function", &FirstParentIsNarrowClass::child_function)

        .def_property("child_property", py::overload_cast<>(&FirstParentIsNarrowClass::get_child_property, py::const_), py::overload_cast<const ::std::string&>(&FirstParentIsNarrowClass::set_child_property))
        .def("parent_function_one", [](FirstParentIsNarrowClass& self) {
            return self.parent_function_one();
        })

        .def("parent_function_two", [](FirstParentIsNarrowClass& self) {
            return self.parent_function_two();
        })

        .def_property("parent_property_one", [](const FirstParentIsNarrowClass& self) {
            return self.get_parent_property_one();
        }, [](FirstParentIsNarrowClass& self, const ::std::string& value) {
            self.set_parent_property_one(value);
        })
        .def_property("parent_property_two", [](const FirstParentIsNarrowClass& self) {
            return self.get_parent_property_two();
        }, [](FirstParentIsNarrowClass& self, const ::std::string& value) {
            self.set_parent_property_two(value);
        })
        ;
}

