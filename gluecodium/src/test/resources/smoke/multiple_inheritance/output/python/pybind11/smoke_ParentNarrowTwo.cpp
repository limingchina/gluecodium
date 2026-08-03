

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
#include "smoke/ParentNarrowTwo.h"
#include "string"

using ParentNarrowTwo = ::smoke::ParentNarrowTwo;

class ParentNarrowTwoTrampoline : public ParentNarrowTwo {
public:
    using ParentNarrowTwo::ParentNarrowTwo;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentNarrowTwo> m_impl;

    void parent_function_two(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->parent_function_two();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentNarrowTwo, parent_function_two);
    }
    ::std::string get_parent_property_two() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_parent_property_two();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ParentNarrowTwo, get_parent_property_two);
    }
    void set_parent_property_two(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_parent_property_two(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentNarrowTwo, set_parent_property_two, value);
    }
};



void register_smoke_ParentNarrowTwo(py::module_& module) {
auto cls_ParentNarrowTwo = py::class_<ParentNarrowTwo, std::shared_ptr<ParentNarrowTwo>, ParentNarrowTwoTrampoline>(module, "smoke_ParentNarrowTwo")
        .def("__gluecodium_id__", [](const ParentNarrowTwo& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentNarrowTwo> native) {
            auto self = std::make_shared<ParentNarrowTwoTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("parent_function_two", [](ParentNarrowTwo& self) {
            return self.parent_function_two();
        })
        .def_property("parent_property_two", [](const ParentNarrowTwo& self) {
            return self.get_parent_property_two();
        }, [](ParentNarrowTwo& self, const ::std::string& value) {
            self.set_parent_property_two(value);
        })
        ;


}
