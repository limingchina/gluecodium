

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/FirstParentIsNarrowInterface.h"
#include "smoke/ParentNarrowOne.h"
#include "smoke/ParentNarrowTwo.h"
#include "string"

using FirstParentIsNarrowInterface = ::smoke::FirstParentIsNarrowInterface;

class FirstParentIsNarrowInterfaceTrampoline : public FirstParentIsNarrowInterface {
public:
    using FirstParentIsNarrowInterface::FirstParentIsNarrowInterface;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<FirstParentIsNarrowInterface> m_impl;

    void child_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->child_function();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowInterface, child_function);
    }
    ::std::string get_child_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_child_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsNarrowInterface, get_child_property);
    }
    void set_child_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_child_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowInterface, set_child_property, value);
    }
    void parent_function_one(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_one();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowInterface, parent_function_one);
    }
    void parent_function_two(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_two();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowInterface, parent_function_two);
    }
    ::std::string get_parent_property_one() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_one();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsNarrowInterface, get_parent_property_one);
    }
    void set_parent_property_one(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_one(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowInterface, set_parent_property_one, value);
    }
    ::std::string get_parent_property_two() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_two();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, FirstParentIsNarrowInterface, get_parent_property_two);
    }
    void set_parent_property_two(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_two(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, FirstParentIsNarrowInterface, set_parent_property_two, value);
    }
};



void register_smoke_FirstParentIsNarrowInterface(py::module_& module) {
auto cls_FirstParentIsNarrowInterface = py::class_<FirstParentIsNarrowInterface, ::smoke::ParentNarrowOne, ::smoke::ParentNarrowTwo, std::shared_ptr<FirstParentIsNarrowInterface>, FirstParentIsNarrowInterfaceTrampoline>(module, "smoke_FirstParentIsNarrowInterface", py::multiple_inheritance())
        .def("__gluecodium_id__", [](const FirstParentIsNarrowInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<FirstParentIsNarrowInterface> native) {
            auto self = std::make_shared<FirstParentIsNarrowInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("child_function", [](FirstParentIsNarrowInterface& self) {
            return self.child_function();
        })
        .def_property("child_property", [](const FirstParentIsNarrowInterface& self) {
            return self.get_child_property();
        }, [](FirstParentIsNarrowInterface& self, const ::std::string& value) {
            self.set_child_property(value);
        })
        .def("parent_function_one", [](FirstParentIsNarrowInterface& self) {
            return self.parent_function_one();
        })
        .def("parent_function_two", [](FirstParentIsNarrowInterface& self) {
            return self.parent_function_two();
        })
        .def_property("parent_property_one", [](const FirstParentIsNarrowInterface& self) {
            return self.get_parent_property_one();
        }, [](FirstParentIsNarrowInterface& self, const ::std::string& value) {
            self.set_parent_property_one(value);
        })
        .def_property("parent_property_two", [](const FirstParentIsNarrowInterface& self) {
            return self.get_parent_property_two();
        }, [](FirstParentIsNarrowInterface& self, const ::std::string& value) {
            self.set_parent_property_two(value);
        })
        ;


}
