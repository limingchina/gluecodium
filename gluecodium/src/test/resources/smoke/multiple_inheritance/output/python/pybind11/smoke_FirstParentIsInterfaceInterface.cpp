

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FirstParentIsInterfaceInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using FirstParentIsInterfaceInterface = ::smoke::FirstParentIsInterfaceInterface;

class FirstParentIsInterfaceInterfaceTrampoline : public FirstParentIsInterfaceInterface {
public:
    using FirstParentIsInterfaceInterface::FirstParentIsInterfaceInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FirstParentIsInterfaceInterface> m_impl;

    void child_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, child_function);
    }
    ::std::string get_child_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_child_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceInterface, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_child_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, set_child_property, value);
    }
    void parent_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, parent_function);
    }
    void some_function_that_uses_type_from_another_package(
            const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->some_function_that_uses_type_from_another_package(some_param);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, some_function_that_uses_type_from_another_package, some_param);
    }
    void parent_function_one(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, parent_function_one);
    }
    ::std::string get_parent_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceInterface, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, set_parent_property, value);
    }
    ::std::string get_parent_property_one() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsInterfaceInterface, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsInterfaceInterface, set_parent_property_one, value);
    }
};

void register_FirstParentIsInterfaceInterface(py::module_& module) {
    py::class_<FirstParentIsInterfaceInterface, ::smoke::ParentInterface, ::smoke::ParentNarrowOne, std::shared_ptr<FirstParentIsInterfaceInterface>, FirstParentIsInterfaceInterfaceTrampoline>(module, "FirstParentIsInterfaceInterface", py::multiple_inheritance())
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<FirstParentIsInterfaceInterface> native) {
            auto self = std::make_shared<FirstParentIsInterfaceInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_function", [](FirstParentIsInterfaceInterface& self) {
            return self.child_function();
        })

        .def_property("child_property", [](const FirstParentIsInterfaceInterface& self) {
            return self.get_child_property();
        }, [](FirstParentIsInterfaceInterface& self, const ::std::string& value) {
            self.set_child_property(value);
        })
        .def("parent_function", [](FirstParentIsInterfaceInterface& self) {
            return self.parent_function();
        })

        .def("some_function_that_uses_type_from_another_package", [](FirstParentIsInterfaceInterface& self, const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param) {
            return self.some_function_that_uses_type_from_another_package(some_param);
        }, py::arg("some_param"))

        .def("parent_function_one", [](FirstParentIsInterfaceInterface& self) {
            return self.parent_function_one();
        })

        .def_property("parent_property", [](const FirstParentIsInterfaceInterface& self) {
            return self.get_parent_property();
        }, [](FirstParentIsInterfaceInterface& self, const ::std::string& value) {
            self.set_parent_property(value);
        })
        .def_property("parent_property_one", [](const FirstParentIsInterfaceInterface& self) {
            return self.get_parent_property_one();
        }, [](FirstParentIsInterfaceInterface& self, const ::std::string& value) {
            self.set_parent_property_one(value);
        })
        ;
}

