

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
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentClassWithImports.h"
#include "cstdint"
#include "functional"
#include "memory"

using ParentClassWithImports = ::smoke::ParentClassWithImports;

class ParentClassWithImportsTrampoline : public ParentClassWithImports {
public:
    using ParentClassWithImports::ParentClassWithImports;

    // Holds an adopted native implementation returned by a factory. When non-null, the
    // trampoline forwards virtual calls to it instead of the pure-virtual stub. A Python
    // subclass is instantiated with no impl held, in which case the overrides fall back to
    // PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ParentClassWithImports> m_impl;

    ::std::shared_ptr< ::smoke::IncludableClass > root_method(
            const ::smoke::IncludableStruct& input1, const ::smoke::IncludableEnum input2 ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->root_method(input1, input2);
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::IncludableClass >, ParentClassWithImports, root_method, input1, input2);
    }
    ::std::function<void(const int64_t)> get_root_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_root_property();
        }
        PYBIND11_OVERRIDE_PURE(::std::function<void(const int64_t)>, ParentClassWithImports, get_root_property);
    }
    void set_root_property(const ::std::function<void(const int64_t)>& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_root_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ParentClassWithImports, set_root_property, value);
    }
};



void register_smoke_ParentClassWithImports(py::module_& module) {
auto cls_ParentClassWithImports = py::class_<ParentClassWithImports, std::shared_ptr<ParentClassWithImports>, ParentClassWithImportsTrampoline>(module, "smoke_ParentClassWithImports")
        .def("__gluecodium_id__", [](const ParentClassWithImports& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        // Adoption constructor: adopt an existing native instance returned by a factory into
        // the trampoline subclass and stash it in `m_impl` so virtual calls forward to the
        // real implementation instead of the pure-virtual stub. `init_alias` cannot be used
        // here because the returned instance is a foreign (non-trampoline) implementation;
        // instead we build a fresh trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ParentClassWithImports> native) {
            auto self = std::make_shared<ParentClassWithImportsTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("root_method", &ParentClassWithImports::root_method, py::arg("input1"), py::arg("input2"))
        .def_property("root_property", [](const ParentClassWithImports& self) {
            return self.get_root_property();
        }, [](ParentClassWithImports& self, const ::std::function<void(const int64_t)>& value) {
            self.set_root_property(value);
        })
        ;


}
