

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
#include "smoke/ChildClassWithBool.h"

using ChildClassWithBool = ::smoke::ChildClassWithBool;

class ChildClassWithBoolTrampoline : public ChildClassWithBool {
public:
    using ChildClassWithBool::ChildClassWithBool;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ChildClassWithBool> m_impl;

    void root_method(
            bool input1 ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->root_method(input1);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ChildClassWithBool, root_method, input1);
    }
};



void register_smoke_ChildClassWithBool(py::module_& module) {
auto cls_ChildClassWithBool = py::class_<ChildClassWithBool, ::smoke::ParentInterfaceWithBool, std::shared_ptr<ChildClassWithBool>, ChildClassWithBoolTrampoline>(module, "smoke_ChildClassWithBool")
        .def("__gluecodium_id__", [](const ChildClassWithBool& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ChildClassWithBool> native) {
            auto self = std::make_shared<ChildClassWithBoolTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("root_method", [](ChildClassWithBool& self, const bool input1) {
            return self.root_method(input1);
        }, py::arg("input1"))
        ;


}
